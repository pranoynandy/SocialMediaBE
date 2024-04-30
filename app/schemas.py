from pydantic import BaseModel, BaseConfig
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_on: datetime
    owner: str
    class Config(BaseConfig):
        from_attributes = True

class PostResponse2(BaseModel):
    Posts: PostResponse
    like: int
    class Config():
        orm_mode = True

class Users(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    created_on: datetime
    class Config(BaseConfig):
        from_attribute = True

class Login(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    username: str

class Like(BaseModel):
    post_id: int

