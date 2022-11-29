from app import models
async def test_like_post(authorized_client, session, posts, users):
  post_id = posts[1].id
  user_id = users[0].id
  res = authorized_client.post('/like/', json={'post_id': post_id, 'direction': True})
  assert res.status_code == 204
  res = session.query(models.Like).one_or_none()
  assert res != None
  assert res.post_id == post_id
  assert res.user_id == user_id

async def test_unlike_post(authorized_client, session, posts):
  post_id = posts[1].id
  res = authorized_client.post('/like/', json={'post_id': post_id, 'direction': True})
  assert res.status_code == 204
  res = session.query(models.Like).one_or_none()
  assert res != None
  res = authorized_client.post('/like/', json={'post_id': post_id, 'direction': False})
  assert res.status_code == 204
  res = session.query(models.Like).one_or_none()
  assert res == None

async def test_like_post_twice(authorized_client, posts):
  post_id = posts[1].id
  res = authorized_client.post('/like/', json={'post_id': post_id, 'direction': True})
  assert res.status_code == 204
  res = authorized_client.post('/like/', json={'post_id': post_id, 'direction': True})
  assert res.status_code == 409

async def test_unlike_post_that_you_dont_like(authorized_client, posts):
  post_id = posts[1].id
  res = authorized_client.post('/like/', json={'post_id': post_id, 'direction': False})
  assert res.status_code == 409

async def test_like_post_not_existing(authorized_client):
  res = authorized_client.post('/like/', json={'post_id': '9999999', 'direction': True})
  assert res.status_code == 404

async def test_like_post_unauthorized(client, posts):
  res = client.post('/like/', json={'post_id': posts[1].id, 'direction': True})
  assert res.status_code == 401