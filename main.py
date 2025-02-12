from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from db.db import create_db_and_tables
from api.route import User, Follow, Post, Like, Bookmark, Vote

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Social Media API",
    description="""
    This API is the backend for a social media platform that allows users to:
    - Register and manage user accounts
    - Follow and unfollow other users
    - Create, like, and bookmark posts
    - Add images and polls to posts
    - Comment on posts and vote in polls
    """,
    version="1.0.0",
    contact={
        "name": "Obinna Osegbu",
        "url": "https://valentineosegbu.com/contact",
        "email": "support@valentineosegbu.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan
)

origins = [
    "http://localhost:3000",
    "https://your-nextjs-app.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(User.user_routes)
app.include_router(Follow.follow_routes)
app.include_router(Post.post_routes)
app.include_router(Like.like_routes)
app.include_router(Bookmark.bookmark_routes)
app.include_router(Vote.vote_routes)
