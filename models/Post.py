from sqlmodel import Field, SQLModel
from typing import Optional, List
from datetime import datetime, timezone
from pydantic import field_validator
from models.User import Auth

class CreatePost(SQLModel):
    post_id: Optional[int] = None
    content: Optional[str] = None
    poll: Optional[List] = None
    image: Optional[List] = None

class UpdatePost(SQLModel):
    content: Optional[str] = None
    poll: Optional[List] = None
    image: Optional[List] = None


class PollResponseModel(SQLModel):
    id: int
    option: str
    votes: int 
    is_voted: bool = False

class ResponseModel(SQLModel):
    id: int
    author: Auth
    post_id: Optional[int] = None
    content: Optional[str] = None
    polls: Optional[List] = None
    images: Optional[List] = None
    likes: Optional[List] = None
    bookmark: bool= False
    comments: Optional[List] = None
    created_at: datetime
    updated_at: datetime

class Model(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    post_id: Optional[int] = Field(default=None, foreign_key="post.id", nullable=True)
    content: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
