import pytest
from server.app import app as flask_app
from server.config import db

@pytest.fixture(scope='session')
def flask_app_fixture():
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    return flask_app

@pytest.fixture(scope='function')
def client(flask_app_fixture):
    with flask_app_fixture.test_client() as client:
        with flask_app_fixture.app_context():
            db.create_all()
            yield client
            db.drop_all()