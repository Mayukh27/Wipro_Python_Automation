from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

browsername = "chrome"

if browsername.lower() == "chrome":

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )

else:
    raise Exception("Invalid browser name. Please choose 'chrome'.")

try:
    driver.get("https://rahulshettyacademy.com/AutomationPractice/")

    time.sleep(2)

    driver.find_element(By.XPATH, '//input[@value="option1"]').click()

    time.sleep(2)

    driver.find_element(By.XPATH, '//input[@value="option2"]').click()

    time.sleep(2)

    driver.find_element(By.XPATH, '//input[@value="option3"]').click()

    time.sleep(2)

finally:
    driver.quit()
