from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
AE_BASE_URL = 'https://automationexercise.com'
OC_REGISTER_URL = 'https://tutorialsninja.com/demo/index.php?route=account/register'

def handle_static_dropdowns_and_checkboxes(driver, wait):
    driver.get(AE_BASE_URL)
    wait.until(EC.title_contains('Automation Exercise'))
    login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Signup / Login')))
    login_link.click()
    wait.until(EC.url_contains('/login'))
    name_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-qa='signup-name']")))
    email_field = driver.find_element(By.CSS_SELECTOR, "input[data-qa='signup-email']")
    unique_email = f'selenium.milestone1.{int(__import__('time').time())}@example.com'
    name_field.send_keys('Selenium Practice')
    email_field.send_keys(unique_email)
    signup_button = driver.find_element(By.CSS_SELECTOR, "button[data-qa='signup-button']")
    signup_button.click()
    wait.until(EC.url_contains('/signup'))
    wait.until(EC.presence_of_element_located((By.ID, 'days')))
    day_dropdown = Select(driver.find_element(By.ID, 'days'))
    month_dropdown = Select(driver.find_element(By.ID, 'months'))
    year_dropdown = Select(driver.find_element(By.ID, 'years'))
    day_dropdown.select_by_value('15')
    month_dropdown.select_by_visible_text('May')
    year_dropdown.select_by_value('1995')
    assert day_dropdown.first_selected_option.get_attribute('value') == '15'
    assert month_dropdown.first_selected_option.text == 'May'
    assert year_dropdown.first_selected_option.get_attribute('value') == '1995'
    newsletter_checkbox = driver.find_element(By.ID, 'newsletter')
    optin_checkbox = driver.find_element(By.ID, 'optin')
    assert newsletter_checkbox.is_selected() is False
    assert optin_checkbox.is_selected() is False
    newsletter_checkbox.click()
    assert newsletter_checkbox.is_selected() is True
    assert optin_checkbox.is_selected() is False
    newsletter_checkbox.click()
    assert newsletter_checkbox.is_selected() is False
    for checkbox in (newsletter_checkbox, optin_checkbox):
        if not checkbox.is_selected():
            checkbox.click()
    assert newsletter_checkbox.is_selected() and optin_checkbox.is_selected()
    country_dropdown = Select(driver.find_element(By.ID, 'country'))
    country_dropdown.select_by_visible_text('United States')
    assert country_dropdown.first_selected_option.text == 'United States'
    print('Static dropdown + checkbox section PASSED on automationexercise.com.')

def handle_dynamic_country_zone_dropdown(driver, wait):
    driver.get(OC_REGISTER_URL)
    wait.until(EC.presence_of_element_located((By.ID, 'input-country')))
    country_select_el = driver.find_element(By.ID, 'input-country')
    country_select = Select(country_select_el)
    country_select.select_by_visible_text('United States')
    zone_select_el = driver.find_element(By.ID, 'input-zone')
    wait.until(lambda d: len(Select(zone_select_el).options) > 1)
    zone_select = Select(zone_select_el)
    target_state = 'California'
    matched = False
    for option in zone_select.options:
        if option.text.strip() == target_state:
            option.click()
            matched = True
            break
    assert matched, f"Expected to find '{target_state}' among the dynamically loaded zones"
    assert zone_select.first_selected_option.text.strip() == target_state
    print('Dynamic (AJAX-populated) dropdown section PASSED on tutorialsninja.com.')

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    try:
        handle_static_dropdowns_and_checkboxes(driver, wait)
        handle_dynamic_country_zone_dropdown(driver, wait)
        print('Assignment 3 PASSED.')
    finally:
        driver.quit()
if __name__ == '__main__':
    main()
