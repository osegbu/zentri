from fastapi import APIRouter, Query, Depends
from db.db import SessionDep
from models.Post import CreatePost, UpdatePost, ResponseModel
from api.controller.PostController import create_post, fetch_post, fetch_all_posts, update_post, delete_post
from typing import List
from utils.jwt_utils import decode_access_token

post_routes = APIRouter()

@post_routes.post(
    "/posts/create", 
    response_model=ResponseModel, 
    summary="Create a new post", 
    description="Creates a new post with the given content and associated data."
)
def create_post_endpoint(post_data: CreatePost, session: SessionDep, token: dict = Depends(decode_access_token)):
    return create_post(token['id'], post_data, session)

@post_routes.get(
    "/posts/{post_id}", 
    response_model=ResponseModel, 
    summary="Fetch a post", 
    description="Retrieves a post by its unique ID."
)
def fetch_post_endpoint(post_id: int, session: SessionDep, token: dict = Depends(decode_access_token)):
    return fetch_post(post_id, token['id'], session)

@post_routes.get(
    "/posts/", 
    response_model=List[ResponseModel], 
    summary="Fetch all posts", 
    description="Fetches all posts with optional pagination."
)
def fetch_all_posts_endpoint(session: SessionDep, offset: int = Query(0, ge=0), token: dict = Depends(decode_access_token)):
    return fetch_all_posts(token['id'], session, offset)

@post_routes.patch(
    "/posts/{post_id}", 
    response_model=ResponseModel, 
    summary="Update a post", 
    description="Updates an existing post by its ID. The user must be authorized to update the post."
)
def update_post_endpoint(post_id: int, post_data: UpdatePost, session: SessionDep, token: dict = Depends(decode_access_token)):
    return update_post(post_id, token['id'], post_data, session)

@post_routes.delete(
    "/posts/{post_id}", 
    summary="Delete a post", 
    description="Deletes a post by its ID. The user must be authorized to delete the post."
)
def delete_post_endpoint(post_id: int, session: SessionDep, token: dict = Depends(decode_access_token)):
    return delete_post(post_id, token['id'], session)
