from fastapi import APIRouter, Depends
from db.db import SessionDep
from api.controller.VoteController import cast_vote, remove_vote
from utils.jwt_utils import decode_access_token

vote_routes = APIRouter()

@vote_routes.post(
    "/vote/{post_id}/{poll_id}", 
    summary="Vote on a poll",
    description="Allows a user to vote on a poll for a specific post by providing the post, poll, and user IDs."
)
def cast_vote_endpoint(post_id: int, poll_id: int, session: SessionDep, token: dict = Depends(decode_access_token)):
    print(post_id)
    # return cast_vote(post_id, token['id'], poll_id, session)

@vote_routes.delete(
    "/vote/{post_id}/{poll_id}", 
    summary="Remove vote from a poll", 
    description="Allows a user to remove their vote from a poll for a specific post by providing the post, poll, and user IDs."
)
def remove_vote_endpoint(post_id: int, poll_id: int, session: SessionDep, token: dict = Depends(decode_access_token)):
    return remove_vote(post_id, token['id'], poll_id, session)
