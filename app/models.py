from .database import Base
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key = True, nullable = False)
  user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
  user = relationship('User')
  title = Column(String, nullable = False)
  content = Column(String, nullable = False)
  published = Column(Boolean, server_default = 'TRUE', nullable = False)
  created_at = Column(TIMESTAMP(timezone=True), server_default = text('NOW()'), nullable = False)

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key = True, nullable = False)
  email = Column(String, nullable = False, unique = True)
  password = Column(String, nullable = False)
  created_at = Column(TIMESTAMP(timezone=True), server_default = text('NOW()'), nullable = False)

class Like(Base):
  __tablename__ = 'likes'

  user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
  post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)