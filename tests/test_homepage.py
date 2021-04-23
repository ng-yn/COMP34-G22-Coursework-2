from unittest import TestCase

from flask_login import logout_user
from flask_login import login_user
from my_app import create_app, db
from my_app.config import TestingConfig
import pytest


class Homepage:

    def test_homepage_button(self, client):
        """
        GIVEN: User (Logged in or not) is on any page
        WHEN: Click Home Button
        THEN: It directs you to the homepage
        """
        response = client.get('/')
        assert response.data == b''

    def test_scroll_button(self):
        """
        GIVEN: User (Logged in or not) is on any page
        WHEN:  Click the scroll Button
        THEN:  It scroll the page down
        """

    def test_Technical_Analysis_url_link(self):
        """
        GIVEN: User (Logged in or not) is on any page
        WHEN:  Click the explain more on Technical Analysis
        THEN:  It will take you to the appropriate link
        """

    def test_Fundamental_Analysis_url_link(self):
        """
        GIVEN: User (Logged in or not) is on any page
        WHEN:  Click the explain more on Fundamental Analysis
        THEN:  It will take you to the appropriate link
        """

    def test_Watchlist_url_link(self):
        """
        GIVEN: User (Logged in or not) is on any page
        WHEN:  Click the explain more on Watchlist
        THEN:  It will take you to the appropriate link
        """