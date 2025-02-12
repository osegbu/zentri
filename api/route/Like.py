from fastapi import APIRouter, Depends
from db.db import SessionDep
from api.controller.LikeController import like_post, unlike_post
from utils.jwt_utils import decode_access_token

like_routes = APIRouter()

@like_routes.post(
    "/like/{post_id}", 
    summary="Like a post", 
    description="Allows a user to like a specific post by providing the user and post IDs."
)
def like_post_endpoint(post_id: int, session: SessionDep, token: dict = Depends(decode_access_token)):
    return like_post(token['id'], post_id, session)

@like_routes.delete(
    "/like/{post_id}", 
    summary="Unlike a post", 
    description="Allows a user to remove their like from a specific post by providing the user and post IDs."
)
def unlike_post_endpoint(post_id: int, session: SessionDep, token: dict = Depends(decode_access_token)):
    return unlike_post(token['id'], post_id, session)
