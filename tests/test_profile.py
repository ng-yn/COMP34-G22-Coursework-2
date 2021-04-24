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
        # db.drop_all()

    def login(self):
        self.driver.get(self.local_test_url + '/login')
        self.driver.find_element_by_id("email").send_keys(self.test_account['username'])
        self.driver.find_element_by_id("password").send_keys(self.test_account['password'])
        self.driver.find_element_by_css_selector('form .btn-primary').click()
        self.driver.implicitly_wait(3)

    # def test_first_time_profile_visit(self):
    #     self.login()
    #     self.driver.get(self.local_test_url + '/profile')
    #     self.assertTrue('Create a profile to access community features!' in self.driver.page_source)

    # def test_create_new_profile(self):
    #     self.login()
    #     self.driver.get(self.local_test_url + '/profile')
    #     self.driver.find_element_by_id("username").send_keys('TestUsername')
    #     self.driver.find_element_by_id("bio").send_keys('This is a test bio')
    #     self.driver.find_element_by_xpath('//button[text()="Save"]').click()
    #
    #     self.driver.get(self.local_test_url + '/profile/TestUsername')
    #     self.assertTrue('This is a test bio' in self.driver.page_source)

    def test_update_profile(self):
        self.login()
        self.driver.get(self.local_test_url + '/profile')
        self.driver.find_element_by_id("username").send_keys('Updated')
        self.driver.find_element_by_id("bio").send_keys('(updated)')
        # self.driver.find_element_by_id("picture").send_keys(
        #     r"C:\Users\richa\OneDrive\Pictures\Screenshot 2021-04-15 154940.PNG")
        self.driver.find_element_by_xpath('//button[text()="Save"]').click()

        self.driver.get(self.local_test_url + '/profile/TestUsernameUpdated')
        self.assertTrue('This is a test bio(updated)' in self.driver.page_source)

    # def test_search_for_profile(self):
    #     self.login()
    #
    #     self.driver.get(self.local_test_url + '/community')
    #
    #     self.driver.find_element_by_xpath("//input[@name='search_term']").send_keys('test')
    #     self.driver.find_element_by_xpath('//button[text()="Search"]').click()
    #     self.driver.find_element_by_link_text('TestUsername').click()
    #     self.assertTrue('This is a test bio' in self.driver.page_source)