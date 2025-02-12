from fastapi import HTTPException
from sqlmodel import select, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from db.db import SessionDep
from models.User import CreateUser, Auth, UpdateUser, LoginUser, UserResponse
from models.Post import ResponseModel, PollResponseModel
from models.Models import User, Post, Vote, Bookmark
from utils.password_utils import hash_password, verify_password
from utils.jwt_utils import create_access_token

def create_user(user_data: CreateUser, session: SessionDep):
    try:
        user_data.user_name = user_data.user_name.lower()
        hashed_password = hash_password(user_data.hashed_password)
        user_data.hashed_password = hashed_password
        user = User.model_validate(user_data)
        
        existing_user = session.exec(select(User).where(User.user_name == user_data.user_name)).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Username is already taken")
        
        session.add(user)
        session.commit()
        session.refresh(user)
        user_dict = {"id": user.id, "user_name": user.user_name, "full_name": user.full_name}
        token = create_access_token(user_dict)
        return {"access_token": token}
    
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error while creating user") from e
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=e.status_code, detail=str(e.detail)) from e

def login_user(user_data: LoginUser, session: SessionDep):
    try:
        user_data.user_name = user_data.user_name.lower()
        user = session.exec(select(User).where(User.user_name == user_data.user_name)).first()

        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        if not verify_password(user_data.hashed_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        user_dict = {"id": user.id, "user_name": user.user_name, "full_name": user.full_name}
        token = create_access_token(user_dict)
        return {"access_token": token, "token_type": "bearer"}
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error during login") from e
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.detail)) from e

def fetch_user(user_name: str, session: SessionDep):
    try:
        user = session.exec(select(User).where(User.user_name == user_name.lower())).first()

        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        
        fetched_posts = session.exec(select(Post).where(and_(Post.user_id == user.id, or_(Post.post_id == None, Post.post_id == 0)))).all()

        def build_response(post):
            poll_responses = []
            for poll in post.polls:
                vote_count = session.exec(select(Vote).where(Vote.poll_id == poll.id)).all()
                
                user_vote = session.exec(
                    select(Vote).where(Vote.poll_id == poll.id, Vote.user_id == user.id)
                ).first()
                
                poll_responses.append(PollResponseModel(
                    id=poll.id,
                    option=poll.option,
                    votes=len(vote_count),
                    is_voted=bool(user_vote) 
                ))

            author = Auth(
                id=user.id,
                user_name=user.user_name,
                full_name=user.full_name,
                profile_image=user.profile_image,
                cover_image=user.cover_image,
                bio=user.bio,
                location=user.location
            )

            bookmark = session.exec(
                select(Bookmark).where(Bookmark.post_id == post.id, Bookmark.user_id == user.id)
            ).first()

            return ResponseModel(
                id=post.id,
                author=author,
                content=post.content,
                post_id=post.post_id,
                polls=poll_responses,
                images=[image.image_url for image in post.images],
                likes=[like for like in post.likes],
                bookmark=bool(bookmark),
                comments=[build_response(child_post) for child_post in post.child_posts],
                created_at=post.created_at.isoformat(),
                updated_at=post.updated_at.isoformat()
            )

        posts = [build_response(post) for post in fetched_posts] if fetched_posts else []

        followers = [{"id": follower.follower.id, "user_name": follower.follower.user_name, "full_name": follower.follower.full_name} for follower in user.followers]
        following = [{"id": followed.followed.id, "user_name": followed.followed.user_name, "full_name": followed.followed.full_name} for followed in user.following]

        response = UserResponse(
            id=user.id,
            user_name=user.user_name,
            full_name=user.full_name,
            bio=user.bio,
            location=user.location,            
            profile_image=user.profile_image,
            cover_image=user.cover_image,
            followers=followers,
            following=following,
            created_at=user.created_at.isoformat(),
            post=posts
        )

        return response
    
    except SQLAlchemyError as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Database error while fetching user") from e
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e
    
def auth(current_user:int, session: SessionDep):
    try:
        user = session.get(User, current_user)

        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        return Auth(
            id=user.id,
            user_name=user.user_name,
            full_name=user.full_name,
            profile_image=user.profile_image,
            cover_image=user.cover_image,
            bio=user.bio,
            location=user.location
        )
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error while fetching user") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

def update_user(user_id: int, user_data: UpdateUser, session: SessionDep):
    try:
        user_data.user_name = user_data.user_name.lower()

        user = session.get(User, user_id)
        
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        existing_user = session.exec(select(User).where(and_(User.user_name == user_data.user_name, User.id != user_id))).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username is already taken")

        user_data = user_data.model_dump(exclude_unset=True)
        user.sqlmodel_update(user_data)
        session.add(user)
        session.commit()
        session.refresh(user)

        return {"response": "Successful"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error during update") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

