from fastapi import status, HTTPException, APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from .. import model, schemas
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(new_user: schemas.Users, db: Session = Depends(get_db)):
    user = model.Users(**new_user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return(user)

@router.get("/{username}", response_model=schemas.UserResponse)
def get_User(username: str, db: Session = Depends(get_db)):
    user = db.query(model.Users).filter(model.Users.username==username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with id = {id} does not exist.")
    return (user)