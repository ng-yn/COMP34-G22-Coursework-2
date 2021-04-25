import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from my_app import create_app, db, config

# So that chrome does not close instantly after test finishes, for debugging purposes
chrome_options = Options()
chrome_options.add_experimental_option("detach", False)  # Change this to true to debug


class CommunityTests(unittest.TestCase):
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

    def test_not_logged_in_community_visit(self):
        self.driver.get(self.local_test_url + '/community')
        self.assertTrue('You must be logged in to view that page.' in self.driver.page_source)

    def test_logged_in_community_visit(self):
        self.login()
        self.driver.get(self.local_test_url + '/community')
        self.assertTrue('Welcome to the Community Section' in self.driver.page_source)

    def test_create_and_view_new_post(self):
        self.login()

        self.driver.get(self.local_test_url + '/community')

        self.driver.find_element_by_link_text('New Post').click()

        self.driver.find_element_by_name('title').send_keys('post_added_by_test')
        self.driver.find_element_by_name('content').send_keys('test_content')
        self.driver.find_element_by_xpath('//button[text()="Submit"]').click()

        self.assertTrue('post_added_by_test' in self.driver.page_source)

        self.driver.find_element_by_link_text('post_added_by_test').click()
        self.assertTrue('test_content' in self.driver.page_source)

    def test_edit_and_delete_post(self):
        self.login()

        self.driver.get(self.local_test_url + '/community')

        self.driver.find_element_by_xpath("//div[@name='post_added_by_test']/a[1]").click()
        self.driver.find_element_by_name('title').send_keys('_edited_for_test')
        self.driver.find_element_by_name('content').send_keys('_edited_for_test')
        self.driver.find_element_by_xpath('//button[text()="Submit"]').click()

        self.assertTrue('post_added_by_test_edited_for_test' in self.driver.page_source)

        self.driver.find_element_by_xpath("//div[@name='post_added_by_test_edited_for_test']/a[1]").click()
        self.assertTrue('test_content_edited_for_test' in self.driver.page_source)

        self.driver.find_element_by_xpath("//input[@value='Delete Post']").click()
        self.driver.switch_to.alert.accept()
        self.assertFalse('test_content_edited_for_test' in self.driver.page_source)















