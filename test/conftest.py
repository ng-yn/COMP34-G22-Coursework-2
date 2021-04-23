import pytest
import pandas as pd
from my_app import db as _db
from my_app import create_app
from my_app.config import TestingConfig
#from my_app.models import User

@pytest.fixture(scope='session')
def app(request):
    """
    returns a session wide flask app
    """
    _app = create_app(TestingConfig)
    ctx = _app.app_context()
    ctx.push()
    yield _app
    ctx.pop()

@pytest.fixture(scope='session')
def client(app):
    """
    exposes the Werkzeug client for use in the unit tests """
    return app.test_client()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    """ Rolls back database changes at the end of each test """
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
    """ Creates a user without a profile. """

    user = User(firstname="Person",
                lastname='One',
                email='person1@people.com')
    user.set_password('password1')
    db.session.add(user)
    db.session.commit()
    return user