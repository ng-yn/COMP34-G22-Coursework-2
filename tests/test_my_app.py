from unittest import TestCase

from flask_login import logout_user
from flask_login import login_user

from my_app import create_app, db
from my_app.config import TestingConfig
import pytest


class Testmyapp:
    def test_home_page_valid(self, client):
        """
        GIVEN a Flask application is running
        WHEN the '/' home page is requested (GET)
        THEN check the response is valid
        """
        response = client.get('/')
        assert response.status_code == 200

    def test_profile_not_allowed_when_user_not_logged_in(self, client):
        """
        GIVEN A user is not logged in
        WHEN When they access the profile menu option
        THEN they should be redirected to the login page
        """
        response = client.get('/profile', follow_redirects=True)
        assert response.status_code == 200
        assert b'/login' in response.data

    def test_signup_succeeds(self,client):
        """
        GIVEN A user is not registered
        WHEN When they submit a valid registration form
        THEN they the should be redirected to a page with a custom welcome message and there should be an additional
        record in the user table in the database
        """
        from my_app.models import User
        count = User.query.count()
        response = client.post('/signup', data=dict(
            username='user2',
            email='person_2@people.com',
            password='password2',
            password_repeat='password2'
        ), follow_redirects=True)
        count2 = User.query.count()
        assert count2 - count == 1
        assert response.status_code == 200
        assert b'user2' in response.data

    def test_login(self, client):
        """
        GIVEN A user is registered
        WHEN When they login
        THEN they the should be redirected to the home page with a login message
        """
        from my_app.models import User
        response = client.post('/login', data=dict(
            email='testuser@gmail.com',
            password='password1'
        ), follow_redirects=True)
        assert response.status_code == 200
        assert b'testuser' in response.data

    # def test_logout(self, client):
    #     """
    #     GIVEN A user is logged in
    #     WHEN When they logout
    #     THEN they the should be redirected to the home page with a logout message
    #     """
    #     login_user('testuser')
    #
    #     response = client.post('/logout', follow_redirects=True)
    #     assert response.status_code == 200
    #     assert b'successfully' in response.data
