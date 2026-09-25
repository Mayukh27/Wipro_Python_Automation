from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = 'https://automationexercise.com'

def add_first_n_products_to_cart(driver, wait, n=2):
    driver.get(f'{BASE_URL}/products')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.features_items')))
    product_wrappers = driver.find_elements(By.CSS_SELECTOR, 'div.product-image-wrapper')
    assert len(product_wrappers) >= n, 'Not enough products found on the page'
    for index in range(n):
        wrappers = driver.find_elements(By.CSS_SELECTOR, 'div.product-image-wrapper')
        add_to_cart_button = wrappers[index].find_element(By.CSS_SELECTOR, 'a.add-to-cart')
        driver.execute_script('arguments[0].scrollIntoView(true);', add_to_cart_button)
        add_to_cart_button.click()
        modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.modal-content')))
        continue_shopping = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-success')))
        continue_shopping.click()
        wait.until(EC.invisibility_of_element(modal))

def extract_table_data(driver, wait):
    driver.get(f'{BASE_URL}/view_cart')
    table = wait.until(EC.presence_of_element_located((By.ID, 'cart_info')))
    header_cells = table.find_elements(By.CSS_SELECTOR, 'thead tr th')
    headers = [cell.text.strip() for cell in header_cells]
    assert headers, 'Expected non-empty table headers'
    print('Table headers:', headers)
    rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
    assert len(rows) >= 2, 'Expected at least two products in the cart'
    table_data = []
    for row in rows:
        description_cell = row.find_element(By.CSS_SELECTOR, 'td.cart_description')
        product_name = description_cell.find_element(By.TAG_NAME, 'h4').text.strip()
        price_cell = row.find_element(By.CSS_SELECTOR, 'td.cart_price p')
        quantity_cell = row.find_element(By.CSS_SELECTOR, 'td.cart_quantity button')
        total_cell = row.find_element(By.CSS_SELECTOR, 'td.cart_total p')
        row_data = {'name': product_name, 'price': price_cell.text.strip(), 'quantity': quantity_cell.text.strip(), 'total': total_cell.text.strip()}
        table_data.append(row_data)
        print('Row extracted:', row_data)
    return table_data

def find_row_by_product_name(table_data, target_name):
    for row in table_data:
        if row['name'] == target_name:
            return row
    return None

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    try:
        add_first_n_products_to_cart(driver, wait, n=2)
        table_data = extract_table_data(driver, wait)
        target_product_name = table_data[0]['name']
        matching_row = find_row_by_product_name(table_data, target_product_name)
        assert matching_row is not None, f"Could not find a row for '{target_product_name}'"
        print(f"Total for '{target_product_name}': {matching_row['total']}")
        assert matching_row['total'].startswith('Rs.'), "Expected an 'Rs.' formatted total"
        print('Assignment 5 PASSED: table parsed and target row located dynamically.')
    finally:
        driver.quit()
if __name__ == '__main__':
    main()
