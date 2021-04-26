#Arinze
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from my_app import create_app, db, config
from selenium.webdriver.common.by import By

# So that chrome does not close instantly after test finishes, for debugging purposes
chrome_options = Options()
chrome_options.add_experimental_option("detach", False)  # Change this to true to debug

class HomePageTests(unittest.TestCase):
    local_test_url = 'http://localhost:5000'
    test_account = {
        'username': 'test@test.com',
        'password': 'potato'
    }

    def setUp(self):
        #setup the application and client
        app = create_app(config.TestingConfig)
        self.app = app.test_client()
        db.create_all()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def tearDown(self):
        db.session.remove()
        # db.drop_all() #This will wipe the database

    def coming_from_a_different_page(self):
        # Coming from a different page- taking the driver to a different page
        # Create a function that we can call in future tests (avoid repititon)
        self.driver.get(self.local_test_url)
        self.driver.find_element_by_id('LoginPage').click()
        self.driver.find_element_by_id('HomePage').click()
        self.driver.implicitly_wait(3)

    def test_homepage_buttom(self):
        # testing Home route
        """
        GIVEN: User (Not Logged) is on any page e.g Login page
        WHEN: Click Home Button
        THEN: It directs you to the homepage
        """
        self.coming_from_a_different_page()
        self.assertIn(self.local_test_url, self.driver.current_url)

    def test_scroll_button(self):
        """
        GIVEN: User (Not Logged) is on any page e.g Login
        WHEN: Click the scroll Button
        THEN: It scroll the page down to the options
        """
        self.coming_from_a_different_page()
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath("//a[contains(@href,'#options')]").click()
        self.driver.back()
        self.driver.execute_script("window.scrollTo(0, 150)")
        self.driver.implicitly_wait(5)

    def test_Technical_Analysis_url_link(self):
        """
        GIVEN: User (Logged in or not) is on any page
        WHEN:  Click the explain Technical Analysis button
        THEN:  It will take you to the appropriate link
        """
        self.TAL = "https://www.investopedia.com/articles/active-trading/102914/technical-analysis-strategies-beginners.asp"
        self.coming_from_a_different_page()
        self.driver.implicitly_wait(5)
        try:
            self.driver.find_element_by_link_text('Explain Technical Analysis').click()
        except:
            self.driver.find_element_by_id('TAL').click()
        else:
            self.driver.find_element_by_xpath('//*[@id="options"]/div[1]/div/div/p[2]/a/button').click()
            self.driver.back()
            self.assertIn(self.TAL, self.driver.current_url)

    def test_Fundamental_Analysis_url_link(self):
        """
        GIVEN: User (Logged in or not) is on any page
        WHEN:  Click the explain Fundamental Analysis
        THEN:  It will take you to the appropriate link
        """
        #define destination link
        self.FAL = "https://www.investopedia.com/terms/f/fundamentalanalysis.asp"

        self.coming_from_a_different_page()
        self.driver.implicitly_wait(5)

        # if try is not used it doesnt work properly - its a turnaround
        try:
            self.driver.find_element_by_link_text('Explain Fundamental Analysis').click()
        except:
            self.driver.find_element_by_id('FAL').click()
        else:
            self.driver.find_element(By.XPATH, '/html/body/main/div/div[2]/section[2]/div/div/div[2]/div/div/p[2]').click()
        self.assertIn(self.FAL, self.driver.current_url)

    def test_Watchlist_url_link(self):
        """
        GIVEN: User (Logged in or not) is on any page
        WHEN:  Click the explain more on Technical Analysis
        THEN:  It will take you to the appropriate link
        """
        self.WAL = "https://www.investopedia.com/terms/w/watchlist.asp"
        self.coming_from_a_different_page()
        self.driver.implicitly_wait(5)

        # if try is not used it doesnt work properly - its a turnaround
        # applied 3 different ways of locating the element - alone they dont work

        try:
            self.driver.find_element_by_link_text('Explain Watchlist').click()
        except:
            self.driver.find_element_by_id('WAL').click()
        else:
            self.driver.find_element(By.XPATH,('//*[@id="options"]/div[3]/div/div/p[2]/a/button')).click()
        self.assertIn(self.WAL, self.driver.current_url)

    def test_all_links(self):
        """
        GIVEN: User (Logged in or not) is on any page
        WHEN:  Click each button back to back
        THEN:  It will take you to the appropriate link without crashing return back and got to the next
        """
        self.coming_from_a_different_page()
        self.driver.implicitly_wait(3)

        # if try is not used it doesnt work properly - its a turnaround
        try:
            self.driver.find_element_by_link_text('Explain Technical Analysis').click()
        except:
            self.driver.find_element_by_id('TAL').click()
        self.driver.implicitly_wait(3)
        self.driver.back()
        try:
            self.driver.find_element_by_link_text('Explain Fundamental Analysis').click()
        except:
            self.driver.find_element_by_id('FAL').click()
        self.driver.implicitly_wait(3)
        self.driver.back()
        try:
            self.driver.find_element_by_link_text('Explain Watchlist')
        except:
            self.driver.find_element_by_id('WAL').click()
        self.driver.implicitly_wait(3)
        self.driver.back()