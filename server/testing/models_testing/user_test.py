import pytest
from server.app import app
from server.config import db
from server.models import User

@pytest.fixture
def app_context():
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

def test_user_creation(app_context):
    user = User(username='testuser', image_url='https://example.com/image.jpg', bio='Test bio')
    user.password_hash = 'testpassword'
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.username == 'testuser'
    assert user.authenticate('testpassword')