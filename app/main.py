from multiprocessing import synchronize
from pyexpat import model
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from . import models, database
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


class Post(BaseModel):
  title: str
  content: str
  published: bool = True

@app.get('/')
async def root():
  return 'this is just a social media api you can see how it works from /docs'

@app.get('/posts')
async def get_posts(db: Session = Depends(database.get_db)):
  posts = db.query(models.Post).all()
  return {'data': posts}

@app.get('/posts/{id}')
async def get_post(id: int, db: Session = Depends(database.get_db)):
  post = db.query(models.Post).filter(models.Post.id == id).one_or_none()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {id} not found')
  return {'data': post}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(database.get_db)):
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  if not new_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {id} not found')
  return {'data': new_post}

@app.put('/posts/{id}')
async def update_post(id: int, post: Post, db: Session = Depends(database.get_db)):
  updated_post = db.query(models.Post).filter(models.Post.id == id)
  if not updated_post.one_or_none():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {id} not found')
  updated_post.update(post.dict(), synchronize_session=False)
  db.commit()
  return {'data': updated_post.one()}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(database.get_db)):
  post = db.query(models.Post).filter(models.Post.id == id)
  if not post.one_or_none():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {id} not found')
  post.delete(synchronize_session=False)
  db.commit()