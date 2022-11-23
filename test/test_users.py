import pytest
from app.config import settings
from app import schemas
from jose import jwt


async def test_create_user(client):
  res = client.post('/users/', json={'email': 'z@gmail.com', 'password': '1234'})
  new_user = schemas.UserResponse(**res.json())
  assert new_user.email == 'z@gmail.com'
  assert res.status_code == 201

async def test_login_user(test_user, client):
  res = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
  token = schemas.Token(**res.json())
  payload = jwt.decode(token.access_token, settings.secret_key, algorithms=[settings.algorithm])
  assert payload.get('id') == test_user['id']
  assert res.status_code == 200

@pytest.mark.parametrize('email, password, status_code', [
  ('wmail', '1234', 403),
  ('z@gmail.com', 'wp', 403),
  ('wmail', 'wp', 403),
  (None, '1234', 422),
  ('z@gmail.com', None, 422)
])
async def test_invalid_login(test_user, client, email, password, status_code):
  res = client.post('/login', data={'username': email, 'password': password})
  assert res.status_code == status_code