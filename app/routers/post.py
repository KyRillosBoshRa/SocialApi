from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, database, schemas
from sqlalchemy.orm import Session

router = APIRouter()

@router.get('/posts', response_model=list[schemas.PostRespanse])
async def get_posts(db: Session = Depends(database.get_db)):
  posts = db.query(models.Post).all()
  return posts

@router.get('/posts/{id}', response_model=schemas.PostRespanse)
async def get_post(id: int, db: Session = Depends(database.get_db)):
  post = db.query(models.Post).filter(models.Post.id == id).one_or_none()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {id} not found')
  return post

@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostRespanse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db)):
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@router.put('/posts/{id}', response_model=schemas.PostRespanse)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db)):
  updated_post = db.query(models.Post).filter(models.Post.id == id)
  if not updated_post.one_or_none():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {id} not found')
  updated_post.update(post.dict(), synchronize_session=False)
  db.commit()
  return updated_post.one()

@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(database.get_db)):
  post = db.query(models.Post).filter(models.Post.id == id)
  if not post.one_or_none():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {id} not found')
  post.delete(synchronize_session=False)
  db.commit()