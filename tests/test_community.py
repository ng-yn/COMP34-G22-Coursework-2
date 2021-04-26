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

    def login(self):
        self.driver.get(self.local_test_url + '/login')
        self.driver.find_element_by_id("email").send_keys(self.test_account['username'])
        self.driver.find_element_by_id("password").send_keys(self.test_account['password'])
        self.driver.find_element_by_css_selector('form .btn-primary').click()
        self.driver.implicitly_wait(3)

    def test_not_logged_in_community_visit(self):
        """
        GIVEN a user is not logged in
        WHEN they try to access the community page
        THEN they will be redirected to the login page and a message will inform them that they must be logged in
        """
        # Visit community page without logging in
        self.driver.get(self.local_test_url + '/community')

        # The login page and a message should display so the text for both of these should be found in the page source
        self.assertTrue('You must be logged in to view that page.' in self.driver.page_source)
        self.assertTrue('Log in to an existing account' in self.driver.page_source)

    def test_logged_in_community_visit(self):
        """
        GIVEN a user is logged in
        WHEN they try to access the community page
        THEN they will be given access to the community page
        """
        # Login first
        self.login()

        # Visit community page and find some known text in the page source
        self.driver.get(self.local_test_url + '/community')
        self.assertTrue('Welcome to the Community Section' in self.driver.page_source)

    def test_create_and_view_new_post(self):
        """
        GIVEN a user can access the community page
        WHEN they follow the steps to create a new post
        THEN they will be taken to the /community/create page where they can fill in the title and content and submit
             their post, and they can then find and view the post from the main community page
        """
        self.login()
        self.driver.get(self.local_test_url + '/community')

        # Find the 'New Post' button and click to go to redirect to create page
        self.driver.find_element_by_link_text('New Post').click()

        # Submit new post with content but no title and assert that the error message is displayed
        self.driver.find_element_by_name('content').send_keys('test_content')
        self.driver.find_element_by_xpath('//button[text()="Submit"]').click()
        self.assertTrue('Title is required!' in self.driver.page_source)

        # Enter the title this time
        self.driver.find_element_by_name('title').send_keys('post_added_by_test')
        self.driver.find_element_by_xpath('//button[text()="Submit"]').click()

        # Find the post title in the page, which should already by redirected to the main community page
        self.assertTrue('post_added_by_test' in self.driver.page_source)

        # Click the post title which should redirect to the post page and find the post content
        self.driver.find_element_by_link_text('post_added_by_test').click()
        self.assertTrue('test_content' in self.driver.page_source)

    def test_edit_and_delete_post(self):
        """
        GIVEN a user has created a post
        WHEN they try to edit/delete the post
        THEN they will be taken to the /community/#/edit page where they can edit the details of the post or delete it
        """
        self.login()
        self.driver.get(self.local_test_url + '/community')

        # Click the edit button and edit the post title and content in the edit page
        self.driver.find_element_by_xpath("//div[@name='post_added_by_test']/a[1]").click()
        self.driver.find_element_by_name('title').send_keys('_edited_for_test')
        self.driver.find_element_by_name('content').send_keys('_edited_for_test')
        self.driver.find_element_by_xpath('//button[text()="Submit"]').click()

        # Ensure the post title is edited correctly in the main community page
        self.assertTrue('post_added_by_test_edited_for_test' in self.driver.page_source)

        # View the post and ensure the content is edited correctly
        self.driver.find_element_by_xpath("//div[@name='post_added_by_test_edited_for_test']/a[1]").click()
        self.assertTrue('test_content_edited_for_test' in self.driver.page_source)

        # Delete the post and ensure it does not appear in the community page anymore
        self.driver.find_element_by_xpath("//input[@value='Delete Post']").click()
        self.driver.switch_to.alert.accept()
        self.assertFalse('test_content_edited_for_test' in self.driver.page_source)
