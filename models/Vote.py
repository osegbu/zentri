from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime, timezone

class Model(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    poll_id: int = Field(default=None, foreign_key="poll.id")
    post_id: int
    user_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))