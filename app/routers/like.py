from fastapi import HTTPException, status, Depends, APIRouter
from app.oAuth2 import get_current_user
from .. import models, database, schemas
from sqlalchemy.orm import Session

router = APIRouter(prefix='/like', tags=['Like'])

@router.post('/', status_code=status.HTTP_204_NO_CONTENT)
async def like_post(like: schemas.Like, db: Session = Depends(database.get_db),
                                              user: dict = Depends(get_current_user)):
  post = db.query(models.Post).filter(models.Post.id == like.post_id).one_or_none()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {like.post_id} not found')
  like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == user.id)
  is_here = like_query.one_or_none()
  if like.direction:
    if is_here:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'you already like this post')
    new_like = models.Like(post_id = like.post_id, user_id = user.id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
  else:
    if not is_here:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'you already don\'t like this post')
    like_query.delete(synchronize_session=False)
    db.commit()