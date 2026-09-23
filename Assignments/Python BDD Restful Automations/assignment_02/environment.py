from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def before_scenario(context, scenario):
    options = Options()
    options.add_argument('--window-size=1600,1000')
    context.driver = webdriver.Chrome(options=options)

def after_scenario(context, scenario):
    context.driver.quit()
