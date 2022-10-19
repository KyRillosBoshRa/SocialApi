from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
  email: EmailStr
  
class UserCreate(UserBase):
  password: str

class UserResponse(UserBase):
  id: int
  class Config:
    orm_mode = True



class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True

class PostCreate(PostBase):
  pass

class PostRespanse(PostBase):
  id: int
  user: UserResponse
  created_at: datetime
  class Config:
    orm_mode = True



class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: int | None = None