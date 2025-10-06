import asyncio
import logging
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio

from api_tests.client import ApiClient
from api_tests.config import Settings
from api_tests.logging_config import setup_logging
from api_tests.models import PostCreate


@pytest.fixture(scope="session", autouse=True)
def _setup_logging() -> None:
	setup_logging()


@pytest.fixture(scope="session")
def settings() -> Settings:
	return Settings.from_env()


@pytest_asyncio.fixture(scope="function")
async def client(settings: Settings) -> AsyncGenerator[ApiClient, None]:
	async with ApiClient(settings) as c:
		yield c


@pytest.mark.asyncio
async def test_get_post(client: ApiClient):
	post = await client.get_post(1)
	assert post.id == 1
	assert post.title
	assert post.body
	assert post.userId >= 1


@pytest.mark.asyncio
async def test_create_post(client: ApiClient):
	payload = PostCreate(title="Hello", body="World", userId=1)
	post = await client.create_post(payload)
	assert post.title == payload.title
	assert post.body == payload.body
	assert post.userId == payload.userId
	assert post.id is not None


@pytest.mark.asyncio
async def test_update_post(client: ApiClient):
	payload = PostCreate(title="Updated", body="Content", userId=1)
	post = await client.update_post(1, payload)
	assert post.title == payload.title
	assert post.body == payload.body
	assert post.userId == payload.userId


@pytest.mark.asyncio
async def test_delete_post(client: ApiClient):
	resp = await client.delete_post(1)
	assert isinstance(resp, dict)
