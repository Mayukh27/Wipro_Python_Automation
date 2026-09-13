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
        products_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Products')))
        products_link.click()
        wait.until(EC.url_contains('/products'))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.features_items')))
        first_add_to_cart = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.product-image-wrapper:first-of-type a.add-to-cart')))
        first_add_to_cart.click()
        modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.modal-content')))
        assert modal.is_displayed()
        view_cart_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'View Cart')))
        view_cart_link.click()
        wait.until(EC.url_to_be(f'{BASE_URL}/view_cart'))
        cart_table = wait.until(EC.presence_of_element_located((By.ID, 'cart_info')))
        assert cart_table is not None
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#cart_info tbody tr')))
        cart_rows = driver.find_elements(By.CSS_SELECTOR, '#cart_info tbody tr')
        assert len(cart_rows) >= 1, 'Expected at least one item in the cart'
        print('Assignment 2 PASSED: explicit waits handled all synchronization points.')
    finally:
        driver.quit()
if __name__ == '__main__':
    main()
