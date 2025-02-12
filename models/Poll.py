from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime, timezone

class Model(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(default=None, foreign_key="post.id")
    option: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))