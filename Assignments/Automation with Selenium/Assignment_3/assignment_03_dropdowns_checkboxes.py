from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = 'https://automationexercise.com'

def create_account_and_open_signup(driver, wait):
    driver.get(BASE_URL)
    wait.until(EC.title_contains('Automation Exercise'))
    login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Signup / Login')))
    login_link.click()
    wait.until(EC.url_contains('/login'))
    name_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-qa='signup-name']")))
    email_field = driver.find_element(By.CSS_SELECTOR, "input[data-qa='signup-email']")
    unique_email = f'selenium.assignment3.{int(time.time())}@example.com'
    name_field.send_keys('Selenium Practice')
    email_field.send_keys(unique_email)
    driver.find_element(By.CSS_SELECTOR, "button[data-qa='signup-button']").click()
    wait.until(EC.url_contains('/signup'))
    wait.until(EC.presence_of_element_located((By.ID, 'days')))

def js_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    driver.execute_script("arguments[0].click();", element)

def handle_static_dropdowns_and_checkboxes(driver, wait):
    create_account_and_open_signup(driver, wait)
    day_dropdown = Select(driver.find_element(By.ID, 'days'))
    month_dropdown = Select(driver.find_element(By.ID, 'months'))
    year_dropdown = Select(driver.find_element(By.ID, 'years'))
    day_dropdown.select_by_value('15')
    month_dropdown.select_by_visible_text('May')
    year_dropdown.select_by_value('1995')
    assert day_dropdown.first_selected_option.get_attribute('value') == '15'
    assert month_dropdown.first_selected_option.text.strip() == 'May'
    assert year_dropdown.first_selected_option.get_attribute('value') == '1995'
    print('Date dropdowns PASSED.')
    newsletter_checkbox = driver.find_element(By.ID, 'newsletter')
    optin_checkbox = driver.find_element(By.ID, 'optin')
    assert not newsletter_checkbox.is_selected()
    assert not optin_checkbox.is_selected()
    js_click(driver, newsletter_checkbox)
    assert newsletter_checkbox.is_selected()
    assert not optin_checkbox.is_selected()
    js_click(driver, newsletter_checkbox)
    assert not newsletter_checkbox.is_selected()
    for checkbox in (newsletter_checkbox, optin_checkbox):
        if not checkbox.is_selected():
            js_click(driver, checkbox)
    assert newsletter_checkbox.is_selected()
    assert optin_checkbox.is_selected()
    print('Checkbox handling PASSED.')
    country_dropdown = Select(driver.find_element(By.ID, 'country'))
    country_dropdown.select_by_visible_text('United States')
    assert country_dropdown.first_selected_option.text.strip() == 'United States'
    print('Country dropdown PASSED.')
    print('Static dropdown + checkbox section PASSED on automationexercise.com.')

def inspect_dynamic_dropdown_options(driver, wait):
    country_element = wait.until(EC.presence_of_element_located((By.ID, 'country')))
    country_dropdown = Select(country_element)
    options = [option.text.strip() for option in country_dropdown.options if option.text.strip()]
    print(f'Number of country options found: {len(options)}')
    print('Available countries:', options)
    assert len(options) > 1
    target_country = 'India'
    assert target_country in options
    country_dropdown.select_by_visible_text(target_country)
    assert country_dropdown.first_selected_option.text.strip() == target_country
    print('Dynamic dropdown option discovery and selection PASSED.')

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    try:
        handle_static_dropdowns_and_checkboxes(driver, wait)
        inspect_dynamic_dropdown_options(driver, wait)
        print('Assignment 3 PASSED.')
    finally:
        driver.quit()

if __name__ == '__main__':
    main()