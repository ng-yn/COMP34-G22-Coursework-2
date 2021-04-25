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
        app = create_app(config.TestingConfig)
        self.app = app.test_client()
        db.create_all()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def tearDown(self):
        db.session.remove()
        # db.drop_all()

    def coming_from_a_different_page(self):
        """
        coming from a different page- taking the driver to a different page
        """
        self.driver.get(self.local_test_url)
        self.driver.find_element_by_id('LoginPage').click()
        self.driver.find_element_by_id('HomePage').click()
        self.driver.implicitly_wait(3)

    def test_homepage_buttom(self):
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
        THEN: It scroll the page down
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
        WHEN:  Click the explain more on Technical Analysis
        THEN:  It will take you to the appropriate link
        """
        self.TAL = "https://www.investopedia.com/articles/active-trading/102914/technical-analysis-strategies-beginners.asp"
        self.coming_from_a_different_page()
        self.driver.implicitly_wait(5)
        #self.driver.find_element_by_id('TAL').click()
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
        WHEN:  Click the explain more on Technical Analysis
        THEN:  It will take you to the appropriate link
        """
        self.FAL = "https://www.investopedia.com/terms/f/fundamentalanalysis.asp"
        self.coming_from_a_different_page()
        self.driver.implicitly_wait(5)
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
        WHEN:  Click each button
        THEN:  It will take you to the appropriate link
        """
        self.coming_from_a_different_page()
        self.driver.implicitly_wait(3)
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