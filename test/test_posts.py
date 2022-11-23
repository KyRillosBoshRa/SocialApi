from app import schemas, models
import pytest

async def test_get_all_posts(authorized_client, posts):
  res = authorized_client.get('posts/')
  assert len(res.json()) == len(posts)
  for x, y in zip(res.json(), reversed(posts)):
    assert schemas.PostBase(**x) == schemas.PostBase(**y.__dict__)
  assert res.status_code == 200

async def test_get_all_posts_unauthorized(client, posts):
  res = client.get('posts/')
  assert res.status_code == 401


async def test_get_one_post(authorized_client, posts):
  res = authorized_client.get(f'posts/{posts[0].id}/')
  assert res.status_code == 200
  assert schemas.PostRespanse(**res.json()) == schemas.PostRespanse(**posts[0].__dict__)

async def test_get_one_post_unauthorized(client, posts):
  res = res = client.get(f'posts/{posts[0].id}')
  assert res.status_code == 401

async def test_get_one_post_not_found(authorized_client):
  res = authorized_client.get(f'posts/9999999/')
  assert res.status_code == 404

@pytest.mark.parametrize('title, content, published',[
  ('p1', 'p1 content', True),
  ('p2', 'p2 content', False)
])
async def test_create_post(authorized_client, users, title, content, published):
  res = authorized_client.post(f'posts/', json={'title': title, 'content': content, 'published': published})
  res.status_code == 201
  post = models.Post(**res.json())
  assert post.id == 1
  assert post.title == title
  assert post.content == content
  assert post.published == published
  assert post.user['id'] == users[0].id

async def test_create_post_default_published(authorized_client, users):
  res = authorized_client.post(f'posts/', json={'title': 'p1 title', 'content': 'p1 content'})
  res.status_code == 201
  post = models.Post(**res.json())
  assert post.id == 1
  assert post.title == 'p1 title'
  assert post.content == 'p1 content'
  assert post.published == True
  assert post.user['id'] == users[0].id

async def test_create_post_unauthorized(client):
  res = client.post(f'posts/', json={'title': 'title', 'content': 'content', 'published': True})
  res.status_code == 401

async def test_delete_post(authorized_client, posts):
  res = authorized_client.delete(f'posts/{posts[0].id}')
  assert res.status_code == 204

async def test_delete_post_not_here(authorized_client):
  res = authorized_client.delete(f'posts/999999')
  assert res.status_code == 404

async def test_delete_post_unauthorized(client, posts):
  res = client.delete(f'posts/{posts[0].id}')
  assert res.status_code == 401

async def test_delete_other_user_post(authorized_client, users, posts):
  res = authorized_client.delete(f'posts/{posts[1].id}')
  assert res.status_code == 401

async def test_update_post(authorized_client, posts):
  data = {
      'title': '111111111111x',
      'content': 'first postx',
  }
  res = authorized_client.put(f'posts/{posts[0].id}', json=data)
  assert res.status_code == 200
  res = models.Post(**res.json())
  assert res.content == data['content']
  assert res.title == data['title']

async def test_update_post_not_here(authorized_client):
  data = {
      'title': '111111111111x',
      'content': 'first postx',
  }
  res = res = authorized_client.put(f'posts/999999', json=data)
  assert res.status_code == 404

async def test_update_post_unauthorized(client, posts):
  data = {
      'title': '111111111111x',
      'content': 'first postx',
  }
  res = client.put(f'posts/{posts[0].id}', json=data)
  assert res.status_code == 401

async def test_update_other_user_post(authorized_client, users, posts):
  data = {
      'title': '111111111111x',
      'content': 'first postx',
  }
  res = authorized_client.put(f'posts/{posts[1].id}', json=data)
  assert res.status_code == 401

