from fastapi import FastAPI
from . import models, database
from .routers import user, post, auth, like
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def root():
  return 'this is just a social media api you can see how it works from /docs'

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(like.router)