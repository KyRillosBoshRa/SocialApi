from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = 'auto')

def hash(x):
  return pwd_context.hash(x)