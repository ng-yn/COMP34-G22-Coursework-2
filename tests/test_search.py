import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from my_app import create_app, db, config

# So that chrome does not close instantly after test finishes, for debugging purposes
chrome_options = Options()
chrome_options.add_experimental_option("detach", False)  # Change this to true to debug


class WatchlistTests(unittest.TestCase):
    local_test_url = 'http://localhost:5000'

    def setUp(self):
        app = create_app(config.TestingConfig)
        self.app = app.test_client()
        db.create_all()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def tearDown(self):
        db.session.remove()
        # db.drop_all()

    def test_search(self):
        """
        GIVEN a user that is using the web application
        WHEN they visit the index page, searching for a company label
        THEN as the search request is send, the page return with the correct information
        """

        # Visit s&p 500 page
        self.driver.get(self.local_test_url + '/index')
        self.driver.find_element_by_id("autocomplete_tickers").send_keys('FB')
        self.driver.find_element_by_xpath('//button[text()="Search"]').click()
        self.assertTrue('FB' in self.driver.page_source)
