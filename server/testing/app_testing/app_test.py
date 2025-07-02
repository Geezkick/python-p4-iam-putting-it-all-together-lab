import pytest

def test_signup(client):
    response = client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpassword',
        'image_url': 'https://example.com/image.jpg',
        'bio': 'Test bio'
    })
    assert response.status_code == 201
    assert response.json['username'] == 'testuser'

def test_check_session(client):
    client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpassword',
        'image_url': 'https://example.com/image.jpg',
        'bio': 'Test bio'
    })
    response = client.get('/check_session')
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'

def test_login(client):
    client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpassword',
        'image_url': 'https://example.com/image.jpg',
        'bio': 'Test bio'
    })
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'

def test_logout(client):
    client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpassword',
        'image_url': 'https://example.com/image.jpg',
        'bio': 'Test bio'
    })
    response = client.delete('/logout')
    assert response.status_code == 204

def test_recipe_index_get(client):
    client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpassword',
        'image_url': 'https://example.com/image.jpg',
        'bio': 'Test bio'
    })
    response = client.get('/recipes')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_recipe_index_post(client):
    client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpassword',
        'image_url': 'https://example.com/image.jpg',
        'bio': 'Test bio'
    })
    response = client.post('/recipes', json={
        'title': 'Test Recipe',
        'instructions': 'This is a test recipe with more than 50 characters to satisfy the validation requirement.',
        'minutes_to_complete': 30
    })
    assert response.status_code == 201
    assert response.json['title'] == 'Test Recipe'