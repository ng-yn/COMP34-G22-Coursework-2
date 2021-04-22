from pathlib import Path

import pytest
from my_app import create_app
from my_app import db as _db
from my_app.config import TestingConfig
import pandas as pd


@pytest.fixture(scope='session')
def app(request):
    """ Returns a session wide Flask app """
    _app = create_app(TestingConfig)
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    """ Exposes the Werkzeug test client for use in the tests. """
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """
    Returns a session wide database using a Flask-SQLAlchemy database connection.
    """
    _db.app = app
    # Add the local authority data to the database (this is a workaround you don't need this for your coursework!)

    yield _db


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
    from my_app.models import User
    user = User(username="testuser", email='testuser@gmail.com')
    user.set_password('password1')
    db.session.add(user)
    db.session.commit()
    return user



