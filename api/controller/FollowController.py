from fastapi import HTTPException
from sqlmodel import select, and_
from db.db import SessionDep
from models.Models import User, Follow

def follow_user(follower_id: int, followed_id: int, session: SessionDep):
    try:
        follower = session.get(User, follower_id)
        followed = session.get(User, followed_id)
        
        if not follower:
            raise HTTPException(status_code=404, detail="Follower not found")
        if not followed:
            raise HTTPException(status_code=404, detail="User to follow not found")
        
        existing_follow = session.exec(
            select(Follow).where(
                and_(Follow.follower_id == follower_id, Follow.followed_id == followed_id)
            )
        ).first()

        if existing_follow:
            raise HTTPException(status_code=400, detail="Already following this user")
        
        new_follow = Follow(follower_id=follower_id, followed_id=followed_id)
        session.add(new_follow)
        session.commit()
        session.refresh(new_follow)

        return {"response": "Successfully followed user"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=e.status_code, detail=str(e.detail)) from e


def unfollow_user(follower_id: int, followed_id: int, session: SessionDep):
    try:
        follower = session.get(User, follower_id)
        followed = session.get(User, followed_id)

        if not follower:
            raise HTTPException(status_code=404, detail="Follower not found")
        if not followed:
            raise HTTPException(status_code=404, detail="User to unfollow not found")
        
        existing_follow = session.exec(
            select(Follow).where(
                and_(Follow.follower_id == follower_id, Follow.followed_id == followed_id)
            )
        ).first()

        if not existing_follow:
            raise HTTPException(status_code=404, detail="Not following this user")

        session.delete(existing_follow)
        session.commit()

        return {"response": "Successfully unfollowed user"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=e.status_code, detail=str(e.detail)) from e
