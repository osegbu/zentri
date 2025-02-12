from fastapi import HTTPException, Query
from sqlmodel import select, or_
from db.db import SessionDep
from models.Post import CreatePost, UpdatePost, ResponseModel, PollResponseModel
from models.Models import Post, User, Poll, PostImage, Like, Bookmark, Vote
from models.User import Auth

def create_post(current_user:int, post_data: CreatePost, session: SessionDep):
    try:
        user = session.get(User, current_user)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        post = Post(user_id=current_user, post_id=post_data.post_id, content=post_data.content)
        session.add(post)
        session.commit()
        session.refresh(post)
        
        if post_data.image:
            post.images = [PostImage(image_url=image_url, post_id=post.id) for image_url in post_data.image]

        if post_data.poll:
            post.polls = [Poll(option=option, post_id=post.id) for option in post_data.poll]

        author = Auth(
            id=user.id,
            user_name=user.user_name,
            full_name=user.full_name,
            profile_image=user.profile_image,
            cover_image=user.cover_image,
            bio=user.bio,
            location=user.location
        )

        poll_responses = []
        for poll in post.polls:            
            poll_responses.append(PollResponseModel(
                id=poll.id,
                option=poll.option,
                votes=0,
                is_voted=bool(False) 
            ))

        session.commit()
        

        response = ResponseModel(
            id=post.id,
            author=author,
            content=post.content,
            post_id=post.post_id,
            polls=poll_responses,
            images=[image.image_url for image in post.images],
            likes=[],
            bookmark=bool(False),
            comments=[],
            created_at=post.created_at.isoformat(),
            updated_at=post.updated_at.isoformat()
        )

        return response

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e
    

def fetch_post(post_id: int, current_user: int, session: SessionDep):
    try:
        post = session.get(Post, post_id)
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        def build_response(post):
            poll_responses = []
            for poll in post.polls:
                vote_count = session.exec(select(Vote).where(Vote.poll_id == poll.id)).all()
                
                user_vote = session.exec(
                    select(Vote).where(Vote.poll_id == poll.id, Vote.user_id == current_user)
                ).first()
                
                poll_responses.append(PollResponseModel(
                    id=poll.id,
                    option=poll.option,
                    votes=len(vote_count),
                    is_voted=bool(user_vote) 
                ))

            user = session.get(User, post.user_id)

            if not user:
                raise HTTPException(status_code=400, detail="User not found")

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
                select(Bookmark).where(Bookmark.post_id == post.id, Bookmark.user_id == current_user)
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

        response = build_response(post)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def fetch_all_posts(current_user: int, session: SessionDep, offset: int = Query(0, ge=0), limit: int = 10):
    try:
        posts = session.exec(
            select(Post)
            .where(or_(Post.post_id == None, Post.post_id == 0))
            .offset(offset)
            .limit(limit)
        ).all()

        if not posts:
            raise HTTPException(status_code=404, detail="No posts found")
        
        def build_response(post):
            poll_responses = []
            for poll in post.polls:
                vote_count = session.exec(select(Vote).where(Vote.poll_id == poll.id)).all()
                
                user_vote = session.exec(
                    select(Vote).where(Vote.poll_id == poll.id, Vote.user_id == current_user)
                ).first()
                
                poll_responses.append(PollResponseModel(
                    id=poll.id,
                    option=poll.option,
                    votes=len(vote_count),
                    is_voted=bool(user_vote) 
                ))

            user = session.get(User, post.user_id)

            if not user:
                raise HTTPException(status_code=400, detail="User not found")

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
                select(Bookmark).where(Bookmark.post_id == post.id, Bookmark.user_id == current_user)
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

        response_list = [build_response(post) for post in posts]
        return response_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    
def update_post(post_id: int, current_user: int, post_data: UpdatePost, session: SessionDep):
    try:
        post = session.get(Post, post_id)

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        user = session.get(User, post.user_id)

        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        if post.user_id != current_user:
            raise HTTPException(status_code=403, detail="Unauthorized to update this post")

        post_data_dict = post_data.model_dump(exclude_unset=True)
        post.sqlmodel_update(post_data_dict)
        session.add(post)
        session.commit()
        session.refresh(post)
        
        prev_images = session.exec(select(PostImage).where(PostImage.post_id == post.id)).all()
        for prev_image in prev_images:
            session.delete(prev_image)

        prev_polls = session.exec(select(Poll).where(Poll.post_id == post.id)).all()
        for prev_poll in prev_polls:
            session.delete(prev_poll)
        
        if post_data.image:
            post.images = [PostImage(image_url=image_url, post_id=post.id) for image_url in post_data.image]

        if post_data.poll:
            post.polls = [Poll(option=option, post_id=post.id) for option in post_data.poll]

        bookmark = session.exec(
            select(Bookmark).where(Bookmark.post_id == post.id, Bookmark.user_id == current_user)
        ).first()

        poll_responses = []
        for poll in post.polls:
            vote_count = session.exec(select(Vote).where(Vote.poll_id == poll.id)).all()
            
            user_vote = session.exec(
                select(Vote).where(Vote.poll_id == poll.id, Vote.user_id == current_user)
            ).first()
            
            poll_responses.append(PollResponseModel(
                id=poll.id,
                option=poll.option,
                votes=len(vote_count),
                is_voted=bool(user_vote) 
            ))

                
        session.commit()


        author = Auth(
            id=user.id,
            user_name=user.user_name,
            full_name=user.full_name,
            profile_image=user.profile_image,
            cover_image=user.cover_image,
            bio=user.bio,
            location=user.location
        )
        
        def build_response(post):
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

        return build_response(post)

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e


def delete_post(post_id: int, current_user: int, session: SessionDep):
    try:
        post = session.get(Post, post_id)

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id != current_user:
            raise HTTPException(status_code=403, detail="Unauthorized to delete this post")

        images = session.exec(select(PostImage).where(PostImage.post_id == post.id)).all()
        for image in images:
            session.delete(image)

        polls = session.exec(select(Poll).where(Poll.post_id == post.id)).all()
        for poll in polls:
            session.delete(poll)

        child_posts = session.exec(select(Post).where(Post.post_id == post.id)).all()
        for child_post in child_posts:
            session.delete(child_post)

        likes = session.exec(select(Like).where(Like.post_id == post.id)).all()
        for like in likes:
            session.delete(like)

        bookmarks = session.exec(select(Bookmark).where(Bookmark.post_id == post.id)).all()
        for bookmark in bookmarks:
            session.delete(bookmark)

        session.delete(post)
        session.commit()

        return {"detail": "Post and associated data deleted successfully"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e
