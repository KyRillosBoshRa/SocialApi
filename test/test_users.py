from app.schemas import UserResponse
from .database import client, session

async def test_create_user(client):
  res = client.post('/users/', json={'email': 'z@gmail.com', 'password': '1234'})
  new_user = UserResponse(**res.json())
  assert new_user.email == 'z@gmail.com'
  assert res.status_code == 201