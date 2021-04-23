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
    test_account = {
        'username': 'test@test.com',
        'password': 'potato'
    }

    def setUp(self):
        app = create_app(config.TestingConfig)
        self.app = app.test_client()
        db.create_all()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def tearDown(self):
        db.session.remove()
        # db.drop_all()

    def login(self):
        self.driver.get(self.local_test_url + '/login')
        self.driver.find_element_by_id("email").send_keys(self.test_account['username'])
        self.driver.find_element_by_id("password").send_keys(self.test_account['password'])
        self.driver.find_element_by_css_selector('form .btn-primary').click()
        self.driver.implicitly_wait(3)

    def test_login(self):
        """
        GIVEN a fresh browser instance
        WHEN a user logs in
        THEN they are redirected to the homepage
        """
        self.login()
        # Assert that browser redirects to home, for some reason my group member
        # put 'user.username' in the url after login lol, so that's how I am checking
        self.assertIn(self.local_test_url + '/user.username', self.driver.current_url)

    def test_not_logged_in_watchlist_visit(self):
        """
        GIVEN a fresh browser instance
        WHEN a user attempts to visit the watchlists page
        THEN they are denied access and given a message telling them they must log in
        """
        self.driver.get(self.local_test_url + '/watchlist')
        self.assertTrue('You must be logged in to view that page.' in self.driver.page_source)

    def test_logged_in_watchlist_visit(self):
        """
        GIVEN a user that is logged in
        WHEN a user attempts to visit the watchlists page
        THEN they are greeted with the logged-in version, and no watchlist will currently be selected,
             so we can check for that text
        """
        self.login()
        self.driver.get(self.local_test_url + '/watchlist')
        # If we visit the watchlist page for the first time while logged in,
        # then no watchlist is selected by default, so we can check for this
        self.assertTrue('(No watchlist selected)' in self.driver.page_source)

    def test_create_and_delete_watchlist(self):
        """
        GIVEN a user that is logged in
        WHEN they visit the watchlists page then create and delete a watchlist
        THEN check that creating a watchlist results in that watchlist being displayed
             on the current page, and deleting the watchlist results in no watchlist
             being currently selected, as denoted by the watchlist title text
        """
        # Log user in
        self.login()
        # Visit watchlists page
        self.driver.get(self.local_test_url + '/watchlist')

        # Click the 'Create Watchlist' button
        self.driver.find_element_by_css_selector("*[data-target='#createWatchlistModal']").click()
        self.driver.implicitly_wait(1)

        # Enter watchlist name and click 'Create'
        self.driver.find_element_by_id('createWatchlistName').send_keys('watchlist_added_by_test_1')
        self.driver.find_element_by_xpath('//button[text()="Create"]').click()

        # Check that the newly added watchlist exists and is currently selected
        self.assertTrue(
            'watchlist_added_by_test_1' in self.driver.find_element_by_class_name('lead').get_attribute("textContent"))

        # Click the 'Delete Watchlist' button
        self.driver.find_element_by_css_selector("*[data-target='#deleteWatchlistModal']").click()
        self.driver.implicitly_wait(1)

        # Click 'Delete' to confirm deletion
        self.driver.find_element_by_xpath('//button[text()="Delete"]').click()
        self.driver.implicitly_wait(1)

        # Check that the newly added watchlist title doesn't appear anymore
        self.assertFalse(
            'watchlist_added_by_test_1' in self.driver.find_element_by_class_name('lead').get_attribute("textContent"))

    def test_create_and_delete_multiple_watchlists(self):
        """
        GIVEN a user that is logged in
        WHEN they visit the watchlists page and then create and delete MULTIPLE watchlists
        THEN check that creating a watchlist results in that watchlist being displayed
             on the current page, then creating another watchlist results in the same. Check
             that both watchlists appear in the dropdown menu and that clicking the watchlist name
             in the dropdown takes you do that watchlist
        """
        # Log user in
        self.login()

        # Visit watchlists page
        self.driver.get(self.local_test_url + '/watchlist')

        # Click the 'Create Watchlist' button
        self.driver.find_element_by_css_selector("*[data-target='#createWatchlistModal']").click()
        self.driver.implicitly_wait(1)

        # Enter watchlist name and click 'Create'
        self.driver.find_element_by_id('createWatchlistName').send_keys('watchlist_added_by_test_1')
        self.driver.find_element_by_xpath('//button[text()="Create"]').click()

        # Check that the newly added watchlist exists and is currently selected
        self.assertTrue(
            'watchlist_added_by_test_1' in self.driver.find_element_by_class_name('lead').get_attribute("textContent"))
        self.driver.implicitly_wait(1)

        # Click the 'Create Watchlist' button again
        self.driver.find_element_by_css_selector("*[data-target='#createWatchlistModal']").click()
        self.driver.implicitly_wait(1)

        # Enter second watchlist name and click 'Create'
        self.driver.find_element_by_id('createWatchlistName').send_keys('watchlist_added_by_test_2')
        self.driver.find_element_by_xpath('//button[text()="Create"]').click()

        # Check that the newly added second watchlist exists and is currently selected
        self.assertTrue(
            'watchlist_added_by_test_2' in self.driver.find_element_by_class_name('lead').get_attribute("textContent"))
        self.driver.implicitly_wait(1)

        # Click the watchlist dropdown
        self.driver.find_element_by_id('watchlistDropdown').click()

        # Check both newly created watchlists are inside the dropdown
        dropdown_items = list(map(lambda x: x.get_attribute('textContent'),
                                  self.driver.find_elements_by_class_name('dropdown-item')))
        self.assertTrue('watchlist_added_by_test_1' in dropdown_items and 'watchlist_added_by_test_2' in dropdown_items)

        # Click the 'Delete Watchlist' button
        self.driver.find_element_by_css_selector("*[data-target='#deleteWatchlistModal']").click()
        self.driver.implicitly_wait(1)

        # Confirm watchlist deletion of the most recently added watchlist (watchlist_added_by_test_2)
        self.driver.find_element_by_xpath('//button[text()="Delete"]').click()
        self.driver.implicitly_wait(1)

        # Use the watchlist dropdown to select 'watchlist_added_by_test_1', and click the dropdown
        # item to go to the watchlist
        self.driver.find_element_by_id('watchlistDropdown').click()
        self.driver.find_element_by_xpath('//a[text()="watchlist_added_by_test_1"]').click()

        # Click the 'Delete Watchlist' button again
        self.driver.find_element_by_css_selector("*[data-target='#deleteWatchlistModal']").click()
        self.driver.implicitly_wait(1)

        # Confirm deletion
        self.driver.find_element_by_xpath('//button[text()="Delete"]').click()
        self.driver.implicitly_wait(1)

        # Check that the first added watchlist title doesn't appear anymore
        self.assertFalse(
            'watchlist_added_by_test_1' in self.driver.find_element_by_class_name('lead').get_attribute("textContent"))

    def test_add_stock_to_watchlist(self):
        """
        GIVEN a user that is logged in
        WHEN they visit the watchlist page, create a watchlist then add some stocks to it, then remove
             those stocks by pressing the 'X' button beside them
        THEN as the stocks are added using a button, check that the stocks appear in the list below
             and check that pressing the 'X' button removes the stock from the list
        """
        # Log user in
        self.login()

        # Visit watchlists page
        self.driver.get(self.local_test_url + '/watchlist')

        # Click the 'Create Watchlist' button
        self.driver.find_element_by_css_selector("*[data-target='#createWatchlistModal']").click()
        self.driver.implicitly_wait(1)

        # Enter watchlist name and click 'Create'
        self.driver.find_element_by_id('createWatchlistName').send_keys('watchlist_added_by_test_1')
        self.driver.find_element_by_xpath('//button[text()="Create"]').click()
        self.driver.implicitly_wait(1)

        # Add Facebook stock ticker and check if it exists in list
        self.driver.find_element_by_id("autocomplete_tickers").send_keys('FB')
        self.driver.find_element_by_xpath('//button[text()="Add Ticker"]').click()
        self.assertTrue('Facebook, Inc' in self.driver.page_source)

        # Add Google stock ticker and check if it exists in list
        self.driver.find_element_by_id("autocomplete_tickers").send_keys('GOOG')
        self.driver.find_element_by_xpath('//button[text()="Add Ticker"]').click()
        self.assertTrue('Alphabet Inc' in self.driver.page_source)

        # Add Nvidia stock ticker and check if it exists in list
        self.driver.find_element_by_id("autocomplete_tickers").send_keys('NVDA')
        self.driver.find_element_by_xpath('//button[text()="Add Ticker"]').click()
        self.assertTrue('NVIDIA Corporation' in self.driver.page_source)

        # Delete all the newly added stocks from the watchlist by pressing the 'X' button
        for _ in range(3):
            self.driver.find_element_by_xpath('//button[text()="X"]').click()

        # Check that all of the newly added stocks no longer exist after deletion
        self.assertFalse('Facebook, Inc' in self.driver.page_source)
        self.assertFalse('Alphabet Inc' in self.driver.page_source)
        self.assertFalse('NVIDIA Corporation' in self.driver.page_source)

        # Delete the watchlist to clean up the test
        self.driver.find_element_by_css_selector("*[data-target='#deleteWatchlistModal']").click()
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_xpath('//button[text()="Delete"]').click()
        self.driver.implicitly_wait(1)

        # Check that the just-deleted watchlist is not currently selected anymore
        self.assertFalse(
            'watchlist_added_by_test_1' in self.driver.find_element_by_class_name('lead').get_attribute("textContent"))
