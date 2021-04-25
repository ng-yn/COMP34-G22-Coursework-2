import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from my_app import create_app, db, config

# So that chrome does not close instantly after test finishes, for debugging purposes
chrome_options = Options()
chrome_options.add_experimental_option("detach", False)  # Change this to true to debug


class SearchTests(unittest.TestCase):
    local_test_url = 'http://localhost:5000'

    def setUp(self):
        app = create_app(config.TestingConfig)
        self.app = app.test_client()
        db.create_all()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def tearDown(self):
        db.session.remove()
        # db.drop_all()

    def test_search_valid(self):
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

    def test_search_invalid(self, client):
        """
        GIVEN a user that is using the web application
        WHEN they visit the index page, searching for a invalid company label
        THEN as the search request is send, a error flash will pop out
        """
        with client.session_transaction() as session:
            flash_message = dict(session['_flashes']).get('warning')

        expected_flash_message = 'No symbol found with that company symbol'
        # Visit s&p 500 page
        self.driver.get(self.local_test_url + '/index')
        self.driver.find_element_by_id("autocomplete_tickers").send_keys('xxx')
        self.driver.find_element_by_xpath('//button[text()="Search"]').click()
        self.assertEqual(flash_message,expected_flash_message)
