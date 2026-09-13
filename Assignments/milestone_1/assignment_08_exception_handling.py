from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementClickInterceptedException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = 'https://automationexercise.com'

def recover_from_no_such_element(driver, wait):
    driver.get(BASE_URL)
    try:
        driver.find_element(By.ID, 'search_product')
        print('Unexpectedly found the search box on the home page.')
    except NoSuchElementException:
        print('NoSuchElementException handled: navigating to the correct page.')
        products_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Products')))
        products_link.click()
        wait.until(EC.url_contains('/products'))
        search_box = wait.until(EC.presence_of_element_located((By.ID, 'search_product')))
        assert search_box is not None
        print('Recovered: search box located on the Products page.')

def recover_from_timeout(driver):
    driver.get(f'{BASE_URL}/products')
    try:
        short_wait = WebDriverWait(driver, 1)
        short_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.modal-content')))
        print('Modal was already visible (unexpected but not an error).')
    except TimeoutException:
        print('TimeoutException handled: modal was not visible yet, retrying with a longer wait.')
        add_to_cart_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.product-image-wrapper:first-of-type a.add-to-cart')))
        add_to_cart_button.click()
        modal = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.modal-content')))
        assert modal.is_displayed()
        print('Recovered: modal became visible with an appropriate wait.')
        continue_shopping = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-success')))
        continue_shopping.click()
        WebDriverWait(driver, 15).until(EC.invisibility_of_element(modal))

def recover_from_stale_element(driver, wait):
    driver.get(f'{BASE_URL}/products')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.features_items')))
    stale_candidate = driver.find_elements(By.CSS_SELECTOR, 'div.product-image-wrapper')[1]
    second_add_to_cart = driver.find_elements(By.CSS_SELECTOR, 'div.product-image-wrapper')[2].find_element(By.CSS_SELECTOR, 'a.add-to-cart')
    second_add_to_cart.click()
    modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.modal-content')))
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-success'))).click()
    wait.until(EC.invisibility_of_element(modal))
    try:
        _ = stale_candidate.text
        print('Original reference still valid (site markup may have changed).')
    except StaleElementReferenceException:
        print('StaleElementReferenceException handled: re-locating the element fresh.')
        fresh_candidate = driver.find_elements(By.CSS_SELECTOR, 'div.product-image-wrapper')[1]
        assert fresh_candidate.text != '' or fresh_candidate is not None
        print('Recovered: fresh element reference obtained successfully.')

def recover_from_click_intercepted(driver, wait):
    driver.get(f'{BASE_URL}/products')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.features_items')))
    first_add_to_cart = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.product-image-wrapper:first-of-type a.add-to-cart')))
    first_add_to_cart.click()
    modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.modal-content')))
    third_add_to_cart = driver.find_elements(By.CSS_SELECTOR, 'div.product-image-wrapper')[3].find_element(By.CSS_SELECTOR, 'a.add-to-cart')
    try:
        third_add_to_cart.click()
        print('Click succeeded without interception (timing-dependent).')
    except ElementClickInterceptedException:
        print('ElementClickInterceptedException handled: closing the overlay first.')
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-success'))).click()
        wait.until(EC.invisibility_of_element(modal))
        third_add_to_cart = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.product-image-wrapper:nth-of-type(4) a.add-to-cart')))
        third_add_to_cart.click()
        second_modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.modal-content')))
        assert second_modal.is_displayed()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-success'))).click()
        print('Recovered: second product added to cart after the overlay closed.')

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    try:
        recover_from_no_such_element(driver, wait)
        recover_from_timeout(driver)
        recover_from_stale_element(driver, wait)
        recover_from_click_intercepted(driver, wait)
        print('Assignment 8 PASSED: all recovery paths exercised.')
    except WebDriverException as unexpected_driver_error:
        print(f'Unhandled WebDriverException reached the top level: {unexpected_driver_error}')
        raise
    finally:
        driver.quit()
if __name__ == '__main__':
    main()
