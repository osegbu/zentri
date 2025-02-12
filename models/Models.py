from sqlmodel import Relationship
from typing import Optional, List
from models import PostImage, User, Post, Like, Bookmark, Follow, Poll, Vote


class User(User.Model, table=True):
    posts: List["Post"] = Relationship(back_populates="user")
    bookmarks: List["Bookmark"] = Relationship(back_populates="user")
    following: List["Follow"] = Relationship(back_populates="follower", sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"})
    followers: List["Follow"] = Relationship(back_populates="followed", sa_relationship_kwargs={"foreign_keys": "[Follow.followed_id]"})

class Post(Post.Model, table=True):
    user: Optional["User"] = Relationship(back_populates="posts")
    parent_post: Optional["Post"] = Relationship(back_populates="child_posts", sa_relationship_kwargs={"remote_side": "Post.id"})
    child_posts: List["Post"] = Relationship(back_populates="parent_post")
    polls: List["Poll"] = Relationship(back_populates="post")
    likes: List["Like"] = Relationship(back_populates="post")
    bookmarks: List["Bookmark"] = Relationship(back_populates="post")
    images: List["PostImage"] = Relationship(back_populates="post")

class PostImage(PostImage.Model, table=True):   
    post: Optional["Post"] = Relationship(back_populates="images")

class Poll(Poll.Model, table=True):
    post: Optional["Post"] = Relationship(back_populates="polls")
    votes: List["Vote"] = Relationship(back_populates="poll")

class Vote(Vote.Model, table=True):
    poll: Optional[Poll] = Relationship(back_populates="votes")

class Like(Like.Model, table=True):
    post: Optional["Post"] = Relationship(back_populates="likes")

class Follow(Follow.Model, table=True):
    follower: Optional["User"] = Relationship(
        back_populates="following", sa_relationship_kwargs={"primaryjoin": "User.id==Follow.follower_id"}
    )
    followed: Optional["User"] = Relationship(
        back_populates="followers", sa_relationship_kwargs={"primaryjoin": "User.id==Follow.followed_id"}
    )

class Bookmark(Bookmark.Model, table=True):
    user: Optional["User"] = Relationship(back_populates="bookmarks")
    post: Optional["Post"] = Relationship(back_populates="bookmarks")