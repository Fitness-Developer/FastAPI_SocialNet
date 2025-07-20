from fastapi import FastAPI
from app.routers import auth,post,comment,chat,user
from app.database import Base,engine

Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(chat.router)
app.include_router(user.router)