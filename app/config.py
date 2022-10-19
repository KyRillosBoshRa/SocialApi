from pydantic import BaseSettings

class Settings(BaseSettings):
  # database
  database_hostname: str
  database_port: str
  database_name: str
  database_username: str
  database_password: str
  # jwt
  secret_key: str
  algorithm: str
  access_token_expire_minutes: int

settings = Settings()