from fastapi import APIRouter, Depends
from db.db import SessionDep
from api.controller.BookmarkController import bookmark_post, remove_bookmark_post, get_bookmarks
from utils.jwt_utils import decode_access_token

bookmark_routes = APIRouter()


@bookmark_routes.get(
    "/bookmark", 
    summary="Get all current user bookmarks", 
    description="Removes a bookmark for a specific post by providing the user and post IDs."
)
def remove_bookmark_post_endpoint(session: SessionDep,  token: dict = Depends(decode_access_token)):
    return get_bookmarks(token['id'], session)

@bookmark_routes.post(
    "/bookmark/{post_id}", 
    summary="Bookmark a post", 
    description="Allows a user to bookmark a specific post by providing the user and post IDs."
)
def bookmark_post_endpoint(post_id: int, session: SessionDep, token: dict = Depends(decode_access_token)):
    return bookmark_post(token['id'], post_id, session)

@bookmark_routes.delete(
    "/bookmark/{post_id}", 
    summary="Remove bookmark from a post", 
    description="Removes a bookmark for a specific post by providing the user and post IDs."
)
def remove_bookmark_post_endpoint(post_id: int, session: SessionDep,  token: dict = Depends(decode_access_token)):
    return remove_bookmark_post(token['id'], post_id, session)
