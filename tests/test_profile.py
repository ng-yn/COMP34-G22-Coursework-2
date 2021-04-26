import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from my_app import create_app, db, config

# So that chrome does not close instantly after test finishes, for debugging purposes
chrome_options = Options()
chrome_options.add_experimental_option("detach", False)  # Change this to true to debug


class ProfileTests(unittest.TestCase):
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

    def login(self):
        self.driver.get(self.local_test_url + '/login')
        self.driver.find_element_by_id("email").send_keys(self.test_account['username'])
        self.driver.find_element_by_id("password").send_keys(self.test_account['password'])
        self.driver.find_element_by_css_selector('form .btn-primary').click()
        self.driver.implicitly_wait(3)

    def test_create_new_profile(self):
        """
        GIVEN a user is logged in and has never created a profile
        WHEN they access the profile page
        THEN they will be taken to the /profile/create_profile page and can create a new profile
        """
        # Login and navigate to the profile page
        self.login()
        self.driver.get(self.local_test_url + '/profile')

        # Enter the username and bio info and save the profile
        self.driver.find_element_by_id("username").send_keys('TestUsername')
        self.driver.find_element_by_id("bio").send_keys('This is a test bio')
        self.driver.find_element_by_xpath('//button[text()="Save"]').click()

        # Navigate to the page for the new profile and ensure that it is there by finding the bio info
        self.driver.get(self.local_test_url + '/profile/TestUsername')
        self.assertTrue('This is a test bio' in self.driver.page_source)

    def test_search_for_profile(self):
        """
        GIVEN a user can access the community page and wants to search for a profile
        WHEN they enter a username in the profile search bar
        THEN they will be taken to the /profile/display_profiles page and a list of possible profiles will display and
             they can click the name of the profile to be taken to the page for that profile
        """
        self.login()
        self.driver.get(self.local_test_url + '/community')

        # Enter a search term for the 'TestUsername' profile, click on the result that matches the profile and ensure
        # that is the correct profile by finding the bio info
        self.driver.find_element_by_xpath("//input[@name='search_term']").send_keys('test')
        self.driver.find_element_by_xpath('//button[text()="Search"]').click()
        self.driver.find_element_by_link_text('TestUsername').click()
        self.assertTrue('This is a test bio' in self.driver.page_source)

    def test_update_profile(self):
        """
        GIVEN a user has already created a profile
        WHEN they try to access the profile page
        THEN they will be taken to the /profile/update_profile page where they can update their profile
        """
        self.login()

        # Go the the /profile page which should now redirect to the /profile/update_profile page
        self.driver.get(self.local_test_url + '/profile')

        # Update the profile by adding 'Updated'
        self.driver.find_element_by_id("username").send_keys('Updated')
        self.driver.find_element_by_id("bio").send_keys('(updated)')
        self.driver.find_element_by_xpath('//button[text()="Save"]').click()

        # Go the page for the updated profile and ensure that the bio is updated
        self.driver.get(self.local_test_url + '/profile/TestUsernameUpdated')
        self.assertTrue('This is a test bio(updated)' in self.driver.page_source)
