from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.hash import argon2
from .. import database, schemas, model, token

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(model.Users).filter(model.Users.username == credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= "Invalid Credentials.")
    if user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= "Invalid Credentials")
    
    access_token = token.create_access_token(data={"username":user.username})
    return {"access_token": access_token, "token_type": "bearer"}