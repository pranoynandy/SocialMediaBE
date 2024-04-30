from fastapi import FastAPI
from .routers import post, user, auth, like
from .database import engine
from . import model

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)


model.Base.metadata.create_all(bind=engine)