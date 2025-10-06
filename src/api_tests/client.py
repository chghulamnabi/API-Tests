from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Optional

import httpx
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from .config import Settings
from .models import Post, PostCreate

logger = logging.getLogger(__name__)


class ApiClient:
	def __init__(self, settings: Settings) -> None:
		self._settings = settings
		self._client: Optional[httpx.AsyncClient] = None

	async def __aenter__(self) -> "ApiClient":
		await self.start()
		return self

	async def __aexit__(self, exc_type, exc, tb) -> None:
		await self.close()

	async def start(self) -> None:
		if self._client is None:
			timeouts = httpx.Timeout(
				connect=self._settings.timeouts.connect,
				read=self._settings.timeouts.read,
				write=self._settings.timeouts.write,
				pool=self._settings.timeouts.read,
			)
			limits = httpx.Limits(max_keepalive_connections=self._settings.pool_limit, max_connections=self._settings.pool_limit)
			self._client = httpx.AsyncClient(base_url=self._settings.base_url, timeout=timeouts, limits=limits)

	async def close(self) -> None:
		if self._client is not None:
			await self._client.aclose()
			self._client = None

	async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
		assert self._client is not None, "Client not started"
		retry = AsyncRetrying(
			stop=stop_after_attempt(self._settings.retry.attempts),
			wait=wait_exponential_jitter(
				initial=self._settings.retry.backoff,
				exp_base=2,
				max=3,
			),
			retry=retry_if_exception_type((httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError)),
			reraise=True,
		)
		async for attempt in retry:
			with attempt:
				response = await self._client.request(method, url, **kwargs)
				response.raise_for_status()
				return response

	# CRUD for Posts
	async def get_post(self, post_id: int) -> Post:
		resp = await self._request("GET", f"/posts/{post_id}")
		return Post(**resp.json())

	async def create_post(self, payload: PostCreate) -> Post:
		resp = await self._request("POST", "/posts", json=payload.dict())
		return Post(**resp.json())

	async def update_post(self, post_id: int, payload: PostCreate) -> Post:
		resp = await self._request("PUT", f"/posts/{post_id}", json=payload.dict())
		return Post(**resp.json())

	async def delete_post(self, post_id: int) -> Dict[str, Any]:
		resp = await self._request("DELETE", f"/posts/{post_id}")
		# JSONPlaceholder returns an empty object {}
		return resp.json() if resp.content else {}
