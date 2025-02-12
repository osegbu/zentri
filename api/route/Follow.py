from fastapi import APIRouter
from db.db import SessionDep
from api.controller.FollowController import follow_user, unfollow_user

follow_routes = APIRouter()

@follow_routes.post(
    "/follow/{follower_id}/{followed_id}", 
    summary="Follow a user",
    description="Allows a user to follow another user by providing the follower and followed user IDs."
)
def follow_user_endpoint(follower_id: int, followed_id: int, session: SessionDep):
    return follow_user(follower_id, followed_id, session)

@follow_routes.delete(
    "/follow/{follower_id}/{followed_id}", 
    summary="Unfollow a user", 
    description="Allows a user to unfollow another user by providing the follower and followed user IDs."
)
def unfollow_user_endpoint(follower_id: int, followed_id: int, session: SessionDep):
    return unfollow_user(follower_id, followed_id, session)
