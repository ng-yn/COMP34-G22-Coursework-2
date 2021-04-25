import pytest
from my_app import create_app
from my_app import db as _db
from my_app.config import TestingConfig


@pytest.fixture(scope='session')
def app(request):
    """ returns a session wide flask app """
    _app = create_app(TestingConfig)
    ctx = _app.app_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    """ exposes the werkzeug test client for use in the tests. """
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """Using the current database for testing session as database is too large to clone every test"""
    _db.app = app
    yield _db


@pytest.fixture(scope='function', autouse=True)
def session(db):
    """ rolls back database changes at the end of each test """
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)
    db.session = session_
    yield session_
    transaction.rollback()
    connection.close()
    session_.remove()


@pytest.fixture(scope='function')
def user(db):
    """ Creates a user without a profile. ID must be included so @login_required decorators won't block the tests """
    from my_app.models import User
    count = User.query.count()
    user = User(id=count+1, username="testuser", email='testuser@gmail.com')
    user.set_password('password1')
    db.session.add(user)
    db.session.commit()
    return user
