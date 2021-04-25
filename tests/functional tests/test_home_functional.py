import pytest
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

def test_app_is_running():

    chrome_driver = webdriver.Chrome
    chrome_driver.get("http://127.0.0.1:5000/")
    assert chrome_driver.find_element_by_link_text('Home') == 'Home'