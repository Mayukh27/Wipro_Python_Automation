import os
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = 'https://automationexercise.com'
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')

def ensure_screenshot_dir():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def timestamped_filename(label):
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    return os.path.join(SCREENSHOT_DIR, f'{label}_{stamp}.png')

def take_screenshot(driver, label):
    path = timestamped_filename(label)
    driver.save_screenshot(path)
    print(f'Screenshot saved: {path}')
    return path

def main():
    ensure_screenshot_dir()
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    try:
        driver.get(BASE_URL)
        wait.until(EC.title_contains('Automation Exercise'))
        take_screenshot(driver, '01_home_page_loaded')
        products_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Products')))
        products_link.click()
        wait.until(EC.url_contains('/products'))
        search_box = wait.until(EC.presence_of_element_located((By.ID, 'search_product')))
        search_box.send_keys('Jeans')
        driver.find_element(By.ID, 'submit_search').click()
        results_heading = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.title.text-center')))
        assert 'Searched Products' in results_heading.text
        take_screenshot(driver, '02_after_product_search')
        try:
            short_wait = WebDriverWait(driver, 1)
            short_wait.until(EC.presence_of_element_located((By.ID, 'this_element_does_not_exist')))
        except TimeoutException:
            take_screenshot(driver, '03_failure_element_not_found')
            print('Expected TimeoutException handled; failure screenshot captured.')
        print('Assignment 7 PASSED: evidence captured across the workflow.')
    except WebDriverException as driver_error:
        take_screenshot(driver, '99_unexpected_webdriver_error')
        print(f'Unexpected WebDriver error captured with screenshot: {driver_error}')
        raise
    finally:
        driver.quit()
if __name__ == '__main__':
    main()
