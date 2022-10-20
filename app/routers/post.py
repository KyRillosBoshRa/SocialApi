from fastapi import HTTPException, status, Depends, APIRouter
from app.oAuth2 import get_current_user
from .. import models, database, schemas
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=list[schemas.PostRespanseWL])
async def get_posts(db: Session = Depends(database.get_db), user: dict = Depends(get_current_user),
                      limit: int = 10, skip: int = 0, search: str = ''):
  # posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
  posts = db.query(models.Post, func.count(models.Like.post_id).label('likes'))\
                      .join(models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id)\
                        .filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
  res = []
  for post in posts:
    res.append(post.Post)
    res[-1].likes = post.likes  
  return res

@router.get('/{id}', response_model=schemas.PostRespanseWL)
async def get_post(id: int, db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
  post = db.query(models.Post, func.count(models.Like.post_id).label('likes'))\
                      .join(models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id)\
                        .filter(models.Post.id == id).one_or_none()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {id} not found')
  res = post.Post
  res.likes = post.likes  
  return res

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostRespanse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db),
                                              user: dict = Depends(get_current_user)):
  new_post = models.Post(**post.dict(), user_id = user.id)
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@router.put('/{id}', response_model=schemas.PostRespanse)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db),
                                              user: dict = Depends(get_current_user)):
  updated_post_query = db.query(models.Post).filter(models.Post.id == id)
  updated_post = updated_post_query.one_or_none()
  if not updated_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {id} not found')
  if user.id != updated_post.user.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'sorry you need to be the post creator in order to update it')
  updated_post_query.update(post.dict(), synchronize_session=False)
  db.commit()
  return updated_post_query.one()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(database.get_db),
                                              user: dict = Depends(get_current_user)):
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.one_or_none()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {id} not found')
  if user.id != post.user.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'sorry you need to be the post creator in order to delete it')
  post_query.delete(synchronize_session=False)
  db.commit()