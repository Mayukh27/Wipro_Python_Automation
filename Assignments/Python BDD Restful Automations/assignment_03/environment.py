import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def before_scenario(context, scenario):
    options = Options()
    options.add_argument('--window-size=1600,1000')
    context.driver = webdriver.Chrome(options=options)

def after_scenario(context, scenario):
    context.driver.quit()
