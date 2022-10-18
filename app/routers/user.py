from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, database, schemas, utils
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
  user.password = utils.hash(user.password)
  new_user = models.User(**user.dict())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  # handle if the email is in the database
  return new_user

@router.get('/users/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(database.get_db)):
  user = db.query(models.User).filter(models.User.id == id).one_or_none()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'sorry post with id: {id} not found')
  return user