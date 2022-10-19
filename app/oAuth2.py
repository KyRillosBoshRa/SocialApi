from fastapi import status, Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

async def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode['exp'] = expire
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def verify_access_token(token: str, credentials_exeption):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get('id')
    if id == None:
      raise credentials_exeption
    return schemas.TokenData(id=id)
  except JWTError:
    raise credentials_exeption

async def get_current_user(token: str = Depends(oauth2_scheme)):
  credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='cannot validate credentials')
  return await verify_access_token(token, credentials_exeption)