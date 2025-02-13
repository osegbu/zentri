from fastapi import HTTPException
from sqlmodel import select, and_
from db.db import SessionDep
from models.Models import User, Bookmark
from api.controller.PostController import fetch_post

def bookmark_post(user_id: int, post_id: int, session: SessionDep):
    try:
        user = session.get(User, user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        is_booked = session.exec(
            select(Bookmark).where(
                and_(Bookmark.user_id == user_id, Bookmark.post_id == post_id)
            )
        ).first()

        if is_booked:
            return fetch_post(post_id, user_id, session)
        
        bookmark = Bookmark(post_id=post_id, user_id=user_id)
        session.add(bookmark)
        session.commit()
        session.refresh(bookmark)

        return fetch_post(post_id, user_id, session)

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=e.status_code, detail=str(e.detail)) from e


def remove_bookmark_post(user_id: int, post_id: int, session: SessionDep):
    try:
        user = session.get(User, user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        is_booked = session.exec(
            select(Bookmark).where(
                and_(Bookmark.user_id == user_id, Bookmark.post_id == post_id)
            )
        ).first()

        if not is_booked:
            return fetch_post(post_id, user_id, session)
        
        session.delete(is_booked)
        session.commit()

        return fetch_post(post_id, user_id, session)

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=e.status_code, detail=str(e.detail)) from e
    
def get_bookmarks(user_id: int, session: SessionDep):
    try:
        user = session.get(User, user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        posts = session.exec(
            select(Bookmark).where(
                and_(Bookmark.user_id == user_id)
            )
        ).all()

        if not posts:
            raise HTTPException(status_code=404, detail="User has not bookmarked this post")

        post_response = []
        for post in posts: 
            post_response.append(fetch_post(post.post_id, user_id, session))

        return post_response

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=e.status_code, detail=str(e.detail)) from e