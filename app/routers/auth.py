from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, database, schemas, utils, oAuth2
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  user = db.query(models.User).filter(models.User.email == user_credentials.username).one()
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'invalid credentials')
  # if password is not hashed it can raise exeption
  if not utils.verify(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'invalid credentials')
  token = await oAuth2.create_access_token({'id': user.id})
  return {'access_token': token, 'token_type': 'bearer'}