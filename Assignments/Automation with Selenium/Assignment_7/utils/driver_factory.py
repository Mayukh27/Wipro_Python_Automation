from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument('--headless=new')
    options.add_argument('--window-size=1600,1000')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)
    return driver
