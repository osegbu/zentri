from fastapi import HTTPException
from sqlmodel import select, and_
from db.db import SessionDep
from models.Models import User, Vote
from api.controller.PostController import fetch_post

def cast_vote(post_id: int, user_id: int, poll_id: int, session: SessionDep):
    try:
        user = session.get(User, user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        existing_vote = session.exec(
            select(Vote).where(
                and_(Vote.user_id == user_id, Vote.post_id == post_id)
            )
        ).first()

        if existing_vote:
            session.delete(existing_vote)
            session.commit()

        new_vote = Vote(user_id=user_id, post_id=post_id, poll_id=poll_id)
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)

        return fetch_post(post_id, user_id, session)

    except Exception as e:
        print(str(e))
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to cast vote") from e


def remove_vote(post_id:int, user_id: int, poll_id: int, session: SessionDep):
    try:
        user = session.get(User, user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        existing_vote = session.exec(
            select(Vote).where(
                and_(Vote.user_id == user_id, Vote.poll_id == poll_id)
            )
        ).first()

        if not existing_vote:
            return fetch_post(post_id, user_id, session)

        session.delete(existing_vote)
        session.commit()

        return fetch_post(post_id, user_id, session)

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete vote") from e
