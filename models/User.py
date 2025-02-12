from sqlmodel import Field, SQLModel
from typing import Optional, List
from datetime import datetime, timezone

class CreateUser(SQLModel):
    user_name: str = Field(index=True, unique=True)
    full_name: str = Field(index=True)
    hashed_password: str = Field(..., min_length=6)

class LoginUser(SQLModel):
    user_name: str
    hashed_password: str = Field(..., min_length=6)

class Auth(SQLModel):
    id: int
    user_name: str
    full_name: str
    profile_image: Optional[str] = None 
    cover_image: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

class UpdateUser(SQLModel):
    user_name: str
    full_name: str
    profile_image: Optional[str] = None 
    cover_image: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

class UserResponse(SQLModel):
    id: int
    user_name: str
    full_name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    profile_image: Optional[str] = None 
    cover_image: Optional[str] = None
    followers: Optional[List]
    following: Optional[List]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    post: Optional[List] = None


class Model(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = Field(index=True, unique=True)
    full_name: str = Field(index=True)
    bio: Optional[str] = None
    location: Optional[str] = None
    profile_image: Optional[str] = None 
    cover_image: Optional[str] = None
    hashed_password: str = Field(..., min_length=6)    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))