from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = 'https://automationexercise.com'

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    try:
        driver.get(BASE_URL)
        wait.until(EC.title_contains('Automation Exercise'))
        headings = driver.find_elements(By.TAG_NAME, 'h2')
        assert len(headings) > 0, 'Expected at least one <h2> on the home page'
        products_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Products')))
        products_link.click()
        wait.until(EC.url_contains('/products'))
        assert '/products' in driver.current_url
        search_box = wait.until(EC.presence_of_element_located((By.ID, 'search_product')))
        search_box.clear()
        search_box.send_keys('Dress')
        search_button = driver.find_element(By.ID, 'submit_search')
        search_button.click()
        results_heading = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.title.text-center')))
        assert 'searched products' in results_heading.text.lower()
        result_products = driver.find_elements(By.CSS_SELECTOR, 'div.product-image-wrapper')
        assert len(result_products) > 0, "Expected at least one search result for 'Dress'"
        login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Signup / Login')))
        login_link.click()
        wait.until(EC.url_contains('/login'))
        email_field = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        password_field = driver.find_element(By.NAME, 'password')
        email_field.send_keys('not_a_real_user_12345@example.com')
        password_field.send_keys('WrongPassword123!')
        login_button = driver.find_element(By.XPATH, "//form[@action='/login']//button[text()='Login']")
        login_button.click()
        error_container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'login-form')))
        error_message = error_container.find_element(By.TAG_NAME, 'p')
        assert 'incorrect' in error_message.text.lower(), f'Expected an incorrect-credentials message, got: {error_message.text!r}'
        print('Assignment 1 PASSED: all locator strategies exercised successfully.')
    finally:
        driver.quit()
if __name__ == '__main__':
    main()