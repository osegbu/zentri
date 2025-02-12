from fastapi import HTTPException
from sqlmodel import select, and_
from db.db import SessionDep
from models.Models import User, Like
from api.controller.PostController import fetch_post

def like_post(user_id: int, post_id: int, session: SessionDep):

    try:
        user = session.get(User, user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        is_like = session.exec(
            select(Like).where(
                and_(Like.user_id == user_id, Like.post_id == post_id)
            )
        ).first()

        if is_like:
            raise HTTPException(status_code=409, detail="User has already liked this post")
        
        like = Like(user_id=user_id, post_id=post_id)
        session.add(like)
        session.commit()
        session.refresh(like)

        return fetch_post(post_id, user_id, session)

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e


def unlike_post(user_id: int, post_id: int, session: SessionDep):
    try:
        user = session.get(User, user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        is_like = session.exec(
            select(Like).where(
                and_(Like.user_id == user_id, Like.post_id == post_id)
            )
        ).first()

        if not is_like:
            raise HTTPException(status_code=404, detail="User has not liked this post")
        
        session.delete(is_like)
        session.commit()

        return fetch_post(post_id, user_id, session)

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=e.status_code, detail=str(e.detail)) from e