import pytest
from app.config import settings
from app import schemas
from jose import jwt


def test_create_user(client):
  res = client.post('/users/', json={'email': 'z@gmail.com', 'password': '1234'})
  new_user = schemas.UserResponse(**res.json())
  assert new_user.email == 'z@gmail.com'
  assert res.status_code == 201

def test_login_user(users, client):
  res = client.post('/login', data={'username': users[0].email, 'password': users[0].password})
  token = schemas.Token(**res.json())
  payload = jwt.decode(token.access_token, settings.secret_key, algorithms=[settings.algorithm])
  assert payload.get('id') == users[0].id
  assert res.status_code == 200

@pytest.mark.parametrize('email, password, status_code', [
  ('wmail', '1234', 403),
  ('z@gmail.com', 'wp', 403),
  ('wmail', 'wp', 403),
  (None, '1234', 422),
  ('z@gmail.com', None, 422)
])
def test_invalid_login(users, client, email, password, status_code):
  res = client.post('/login', data={'username': email, 'password': password})
  assert res.status_code == status_code