from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from typing import List, Optional
import time
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import model, schemas, main, token
from ..database import get_db

router = APIRouter(tags=["Posts"])


'''
@app.get("/")
def home():
    return("WELCOME TO MY APP")


@app.get("/posts")
def get_posts():
    main.cursor.execute("""SELECT * FROM posts""")
    my_posts = main.cursor.fetchall()
    return(my_posts)


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    main.cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    my_post = main.cursor.fetchone()
    print(my_post)
    if not my_post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return(f"Post with id = {id} does not exist.")
    return (my_post)


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    main.cursor.execute("""INSERT INTO posts (title,content) VALUES (%s, %s) RETURNING * """,
                   (new_post.title,new_post.content))
    new_post = cursor.fetchone()
    conn.commit()
    return("Post successfully saved!", new_post)


@app.put("/posts/{id}")
def uppdate_post(updated_post: Post, id: int):
    cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING * """,
                   (updated_post.title,updated_post.content,str(id)))
    new_post = cursor.fetchone()
    conn.commit()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id = {id} does not exist.")
    return("Post successfully updated!", new_post)
    


@app.delete("/posts/{id}")
def delete_post(id: int, response: Response):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id = {id} does not exist.")
    response.status_code = status.HTTP_204_NO_CONTENT
    return(f"Post with id = {id} is deleted successfully.")
'''



# Connecting to database using SQLALCHEMY

@router.get("/post", response_model=List[schemas.PostResponse])
def get_posts_sqlalchemy(db: Session = Depends(get_db), 
                         limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    likes = db.query(model.Post, func.count(model.Like.post_id)).join(
            model.Like, model.Like.post_id == model.Post.id, isouter=True).group_by(
            model.Post.id)
    print(likes)
    return posts


@router.get("/post/{id}", response_model=schemas.PostResponse)
def get_post_sqlalchemy(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id = {id} does not exist.")
    return (post)


@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post_sqlalchemy(new_post: schemas.Post, db: Session = Depends(get_db), 
                           user: str = Depends(token.get_currect_user)):
    print(f"Post created by {user.username}")
    post = model.Post(**new_post.dict())
    post.owner = user.username
    db.add(post)
    db.commit()
    db.refresh(post)
    return(post)


@router.put("/post/{id}", response_model=schemas.PostResponse)
def uppdate_post_sqlalchemy(updated_post: schemas.Post, id: int, db: Session = Depends(get_db),
                            user: str = Depends(token.get_currect_user)):
    post = db.query(model.Post).filter(model.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id = {id} does not exist.")
    if post.owner != user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Action Denied")
    post.title = updated_post.title
    post.content = updated_post.content
    db.add(post)
    db.commit()
    db.refresh(post)
    return(post)


@router.delete("/post/{id}")
def delete_post(id: int, response: Response, db: Session = Depends(get_db),
                user: str = Depends(token.get_currect_user)):
    post = db.query(model.Post).filter(model.Post.id==id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id = {id} does not exist.")
    if post.first().owner != user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Action Denied")
    post.delete(synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
    return(f"Post with id = {id} is deleted successfully.")