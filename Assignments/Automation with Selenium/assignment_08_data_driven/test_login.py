import csv
import json
import os
import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = 'https://automationexercise.com'
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
LOGIN_EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-email']")
LOGIN_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-password']")
LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
LOGIN_ERROR_MESSAGE = (By.CSS_SELECTOR, 'div.login-form p')
LOGGED_IN_AS_LINK = (By.XPATH, "//a[contains(text(),'Logged in as')]")
LOGOUT_LINK = (By.LINK_TEXT, 'Logout')
SIGNUP_NAME_INPUT = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
SIGNUP_EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")
ACCOUNT_PASSWORD_INPUT = (By.ID, 'password')
ACCOUNT_DAYS_SELECT = (By.ID, 'days')
ACCOUNT_MONTHS_SELECT = (By.ID, 'months')
ACCOUNT_YEARS_SELECT = (By.ID, 'years')
ACCOUNT_FIRST_NAME_INPUT = (By.ID, 'first_name')
ACCOUNT_LAST_NAME_INPUT = (By.ID, 'last_name')
ACCOUNT_ADDRESS1_INPUT = (By.ID, 'address1')
ACCOUNT_COUNTRY_SELECT = (By.ID, 'country')
ACCOUNT_STATE_INPUT = (By.ID, 'state')
ACCOUNT_CITY_INPUT = (By.ID, 'city')
ACCOUNT_ZIPCODE_INPUT = (By.ID, 'zipcode')
ACCOUNT_MOBILE_INPUT = (By.ID, 'mobile_number')
CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[data-qa='create-account']")
CONTINUE_BUTTON = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

def load_csv_cases(path):
    with open(path, newline='', encoding='utf-8') as csv_file:
        return list(csv.DictReader(csv_file))

def load_json_cases(path):
    with open(path, encoding='utf-8') as json_file:
        return json.load(json_file)

def load_xlsx_cases(path):
    workbook = openpyxl.load_workbook(path, data_only=True)
    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    headers = [str(header).strip() for header in rows[0]]
    return [dict(zip(headers, row)) for row in rows[1:]]

def register_new_account(driver, wait, email, password):
    driver.get(f'{BASE_URL}/login')
    wait.until(EC.presence_of_element_located(SIGNUP_NAME_INPUT))
    driver.find_element(*SIGNUP_NAME_INPUT).send_keys('DDT Test User')
    driver.find_element(*SIGNUP_EMAIL_INPUT).send_keys(email)
    driver.find_element(*SIGNUP_BUTTON).click()
    wait.until(EC.url_contains('/signup'))
    wait.until(EC.presence_of_element_located(ACCOUNT_PASSWORD_INPUT))
    driver.find_element(*ACCOUNT_PASSWORD_INPUT).send_keys(password)
    Select(driver.find_element(*ACCOUNT_DAYS_SELECT)).select_by_value('12')
    Select(driver.find_element(*ACCOUNT_MONTHS_SELECT)).select_by_visible_text('June')
    Select(driver.find_element(*ACCOUNT_YEARS_SELECT)).select_by_value('1997')
    driver.find_element(*ACCOUNT_FIRST_NAME_INPUT).send_keys('DDT')
    driver.find_element(*ACCOUNT_LAST_NAME_INPUT).send_keys('Tester')
    driver.find_element(*ACCOUNT_ADDRESS1_INPUT).send_keys('456 Data Driven Ave')
    Select(driver.find_element(*ACCOUNT_COUNTRY_SELECT)).select_by_visible_text('United States')
    driver.find_element(*ACCOUNT_STATE_INPUT).send_keys('Texas')
    driver.find_element(*ACCOUNT_CITY_INPUT).send_keys('Austin')
    driver.find_element(*ACCOUNT_ZIPCODE_INPUT).send_keys('73301')
    driver.find_element(*ACCOUNT_MOBILE_INPUT).send_keys('5559876543')
    driver.find_element(*CREATE_ACCOUNT_BUTTON).click()
    wait.until(EC.url_contains('/account_created'))
    driver.find_element(*CONTINUE_BUTTON).click()
    wait.until(EC.visibility_of_element_located(LOGGED_IN_AS_LINK))
    driver.find_element(*LOGOUT_LINK).click()
    wait.until(EC.url_contains('/login'))

def attempt_login(driver, wait, email, password):
    driver.get(f'{BASE_URL}/login')
    wait.until(EC.presence_of_element_located(LOGIN_EMAIL_INPUT))
    driver.find_element(*LOGIN_EMAIL_INPUT).send_keys(email)
    driver.find_element(*LOGIN_PASSWORD_INPUT).send_keys(password)
    driver.find_element(*LOGIN_BUTTON).click()
    wait.until(EC.any_of(EC.visibility_of_element_located(LOGGED_IN_AS_LINK), EC.visibility_of_element_located(LOGIN_ERROR_MESSAGE)))
    logged_in_elements = driver.find_elements(*LOGGED_IN_AS_LINK)
    if logged_in_elements and logged_in_elements[0].is_displayed():
        driver.find_element(*LOGOUT_LINK).click()
        wait.until(EC.url_contains('/login'))
        return 'valid'
    error_element = driver.find_element(*LOGIN_ERROR_MESSAGE)
    assert 'incorrect' in error_element.text.lower()
    return 'invalid'

def run_data_driven_cases(driver, wait, cases):
    passed = 0
    for case in cases:
        result = attempt_login(driver, wait, case['email'], case['password'])
        expected = str(case['expected']).strip().lower()
        status = 'PASSED' if result == expected else 'FAILED'
        print(f'[{case['test_id']}] expected={expected} actual={result} -> {status}')
        assert result == expected, f'{case['test_id']}: expected {expected}, got {result}'
        passed += 1
    return passed

def main():
    csv_cases = load_csv_cases(os.path.join(DATA_DIR, 'test_data.csv'))
    json_cases = load_json_cases(os.path.join(DATA_DIR, 'test_data.json'))
    xlsx_cases = load_xlsx_cases(os.path.join(DATA_DIR, 'test_data.xlsx'))
    file_backed_cases = csv_cases + json_cases + xlsx_cases
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    try:
        run_data_driven_cases(driver, wait, file_backed_cases)
        unique_email = f'ddt.runtime.{int(time.time())}@example.com'
        correct_password = 'DataDriven!2024'
        register_new_account(driver, wait, unique_email, correct_password)
        runtime_cases = [{'test_id': 'RUNTIME-VALID', 'email': unique_email, 'password': correct_password, 'expected': 'valid'}, {'test_id': 'RUNTIME-WRONG-PASSWORD', 'email': unique_email, 'password': 'TotallyWrongPassword!', 'expected': 'invalid'}]
        run_data_driven_cases(driver, wait, runtime_cases)
        total = len(file_backed_cases) + len(runtime_cases)
        print(f'Assignment 8 PASSED: {total} data-driven login cases executed.')
    finally:
        driver.quit()
if __name__ == '__main__':
    main()
