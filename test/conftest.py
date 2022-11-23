import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base, SQLALCHEMY_DATABASE_URL
from app import schemas
from app.oAuth2 import create_access_token
from app import models

engine = create_engine(SQLALCHEMY_DATABASE_URL+'_test')
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()

@pytest.fixture
def client(session):
  def override_get_db():
    try:
      yield session
    finally:
      session.close()
  app.dependency_overrides[get_db] = override_get_db
  yield TestClient(app)

@pytest.fixture
def users(client, session):
  user_data = schemas.UserCreate(email='x@y.z', password='xyz')
  res = client.post('/users/', json=user_data.dict())
  assert res.status_code == 201
  res = models.User(**res.json(), password = 'xyz')
  user_data = schemas.UserCreate(email='x2@y.z', password='xyz')
  res2 = client.post('/users/', json=user_data.dict())
  assert res2.status_code == 201
  res2 = models.User(**res2.json(), password = 'xyz')
  return [res, res2]

@pytest.fixture
async def token(users):
  return await create_access_token({'id': users[0].id})

@pytest.fixture
def authorized_client(client, token):
  client.headers = {
    **client.headers,
    'Authorization': f'Bearer {token}'
  }
  return client

@pytest.fixture
def posts(users, session):
  post_data = [
    {
      'title': '111111111111',
      'content': 'first post',
      'user_id': users[0].id
    },{
      'title': '22222222222222222222',
      'content': 'second post',
      'user_id': users[1].id
    }
  ]
  session.add_all(
    [models.Post(**post_data[0]), models.Post(**post_data[1])]
  )
  session.commit()
  res = session.query(models.Post).all()
  return res