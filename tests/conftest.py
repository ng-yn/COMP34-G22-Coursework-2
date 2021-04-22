from pathlib import Path

import pytest
from flask_login import LoginManager

from my_app import create_app
from my_app import db as _db
from my_app.config import TestingConfig
import pandas as pd
import selenium


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
    """
    returns a session wide database using a flask-sqlalchemy database connection.
    """
    _db.app = app
    # add the local authority data to the database (this is a workaround you don't need this for your coursework!)

    yield _db

# @pytest.fixture(scope='session')
# def loginmanager(app):
#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login'
#     login_manager.app = app
#
#     yield login_manager


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
    """ creates a user without a profile. """
    from my_app.models import User
    user = User(username="testuser", email='testuser@gmail.com')
    user.set_password('password1')
    db.session.add(user)
    db.session.commit()
    return user


# @pytest.fixture(scope='function')
# def test_with_authenticated_user(app):
#     @login_manager.request_loader
#     def load_user_from_request(request):
#         return User.query.first()
#
# @pytest.fixture(scope='class')
# def chrome_driver(request):
#     """ Fixture for selenium webdriver with options to support running in GitHub actions"""
#     options = ChromeOptions()
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--headless")
#     options.add_argument("--window-size=1920,1080")
#     chrome_driver = webdriver.Chrome(options=options)
#     request.cls.driver = chrome_driver
#     yield
#     chrome_driver.close()
#
#
# @pytest.fixture(scope='class')
# def selenium(app):
#     """
#     Fixture to run the Flask app
#     A better alternative would be to use flask-testing live_server
#     """
#     process = multiprocessing.Process(target=app.run, args=())
#     process.start()
#     yield process
#     process.terminate()

