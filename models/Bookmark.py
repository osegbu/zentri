from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime, timezone


class Model(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))