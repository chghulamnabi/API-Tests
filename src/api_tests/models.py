from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, validator


class PostCreate(BaseModel):
	title: str = Field(..., min_length=1)
	body: str = Field(..., min_length=1)
	userId: int = Field(..., ge=1)


class Post(PostCreate):
	id: Optional[int] = Field(None, ge=1)

	@validator("id")
	def id_positive(cls, v):
		if v is not None and v < 1:
			raise ValueError("id must be positive when present")
		return v
