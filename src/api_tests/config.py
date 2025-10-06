from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class HttpTimeouts:
	connect: float
	read: float
	write: float


@dataclass(frozen=True)
class RetryConfig:
	attempts: int
	backoff: float


@dataclass(frozen=True)
class Settings:
	base_url: str
	timeouts: HttpTimeouts
	pool_limit: int
	retry: RetryConfig

	@staticmethod
	def from_env(env: Optional[dict[str, str]] = None) -> "Settings":
		load_dotenv(override=False)
		e = os.environ if env is None else env
		base_url = e.get("API_BASE_URL", "https://jsonplaceholder.typicode.com").rstrip("/")
		connect = float(e.get("API_CONNECT_TIMEOUT", "5"))
		read = float(e.get("API_READ_TIMEOUT", "15"))
		write = float(e.get("API_WRITE_TIMEOUT", "15"))
		pool_limit = int(e.get("API_POOL_LIMIT", "100"))
		attempts = int(e.get("API_RETRY_ATTEMPTS", "3"))
		backoff = float(e.get("API_RETRY_BACKOFF", "0.2"))
		return Settings(
			base_url=base_url,
			timeouts=HttpTimeouts(connect=connect, read=read, write=write),
			pool_limit=pool_limit,
			retry=RetryConfig(attempts=attempts, backoff=backoff),
		)
