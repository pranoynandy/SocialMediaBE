from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from .. import model, schemas, token
from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(tags=['Posts'])


@router.post("/like", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(get_db), user: str = Depends(token.get_currect_user)):
    check_post = db.query(model.Post).filter(model.Post.id == like.post_id).first()

    if not check_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    check_like = db.query(model.Like).filter(model.Like.post_id == like.post_id, model.Like.username == user.username)
    found_like = check_like.first()

    if found_like:
        check_like.delete()
        db.commit()
        return("Like Removed")
    else:
        new_like = model.Like(post_id = like.post_id, username = user.username)
        db.add(new_like)
        db.commit()
        return("Post Liked")