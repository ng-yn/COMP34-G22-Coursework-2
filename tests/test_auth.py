import pytest


def signup(client, username, email, password, password_repeat):
    """ Function to sign up an unregistered user"""
    return client.post('/signup/', data=dict(
            username=username,
            email=email,
            password=password,
            password_repeat=password_repeat
        ), follow_redirects=True)


def login(client, email, password):
    """Function to login a user"""
    return client.post('/login/', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    """Function to logout a user"""
    return client.get('/logout', follow_redirects=True)


class TestAuth:
    """ Tests for authentication (signup, login, logout etc.) """
    def test_home_page_valid(self, client):
        """
        GIVEN a Flask application is running
        WHEN the '/' home page is requested (GET)
        THEN check the response is valid
        """
        response = client.get('/')
        assert response.status_code == 200

    def test_login_required_pages(self, client):
        """
        GIVEN A user is not logged in
        WHEN When they access the profile menu option
        THEN they should be redirected to the login page
        """
        response = client.get('/watchlist', follow_redirects=True)
        assert response.status_code == 200
        assert b'You must be logged in to view that page.' in response.data
        response = client.get('/community', follow_redirects=True)
        assert response.status_code == 200
        assert b'You must be logged in to view that page.' in response.data
        response = client.get('/profile', follow_redirects=True)
        assert response.status_code == 200
        assert b'You must be logged in to view that page.' in response.data
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'You must be logged in to view that page.' in response.data

    def test_signup_succeeds(self, client):
        """
        GIVEN A user is not registered
        WHEN When they submit a valid registration form
        THEN they the should be redirected to a page with a custom welcome message and there should be an additional
        record in the user table in the database
        """
        from my_app.models import User
        count = User.query.count()
        response = signup(client, 'user2', 'user2@gmail.com', 'password2', 'password2')
        count2 = User.query.count()
        assert response.status_code == 200
        assert b'user2' in response.data
        assert count2 - count == 1
        assert b'Hello, user2. You have successfully signed up. Please login to continue.'

    @pytest.mark.usefixtures('user')
    def test_signup_fails(self, client):
        """
        GIVEN A user is not registered
        WHEN When they submit an invalid registration form
        (i.e. email already exists, incorrect password length and password not matching)
        THEN they should be flashed with invalid credential errors
        """
        response = signup(client, 'user2', 'testuser@gmail.com', 'password2', 'password2')
        assert response.status_code == 200
        assert b'An account is already registered for that email address' in response.data

        response = signup(client, 'user2', 'user2@gmail.com', 'pas', 'pas')
        assert response.status_code == 200
        assert b'Password must be between 4-16 characters long' in response.data

        response = signup(client, 'user2', 'user2@gmail.com', 'password2', 'password')
        assert response.status_code == 200
        assert b'Passwords must match' in response.data

    @pytest.mark.usefixtures('user')
    def test_login_succeeds(self, client):
        """
        GIVEN A user is registered
        WHEN When they login
        THEN they the should be redirected to the home page and flashed with a login message
        """
        response = login(client, 'testuser@gmail.com', 'password1')
        assert response.status_code == 200
        assert b'Hello, testuser. You have successfully logged in.' in response.data

    @pytest.mark.usefixtures('user')
    def test_login_fails(self, client):
        """
        GIVEN A user is registered
        WHEN they login with incorrect details (i.e. wrong email or password)
        THEN they should be flashed with an incorrect login details error
        """
        response = login(client, 'testuser@gmail.comx', 'password1')
        assert response.status_code == 200
        assert b'This email address is not registered'
        response = login(client, 'testuser@gmail.com', 'password1x')
        assert response.status_code == 200
        assert b'The password is incorrect'

    @pytest.mark.usefixtures('user')
    def test_logout(self, client):
        """
        GIVEN A user is logged in
        WHEN they logout
        THEN they the should be redirected to the home page and flashed with a logout message
        """
        response = login(client, 'testuser@gmail.com', 'password1')
        assert response.status_code == 200
        assert b'Hello, testuser. You have successfully logged in.' in response.data
        response = logout(client)
        assert response.status_code == 200
        assert b'You have successfully logged out.' in response.data















