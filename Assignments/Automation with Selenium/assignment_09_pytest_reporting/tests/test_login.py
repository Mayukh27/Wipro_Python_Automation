import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = 'https://automationexercise.com'
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

def test_login_page_loads(driver):
    wait = WebDriverWait(driver, 15)
    driver.get(f'{BASE_URL}/login')
    wait.until(EC.title_contains('Automation Exercise'))
    assert '/login' in driver.current_url
    assert wait.until(EC.presence_of_element_located(LOGIN_EMAIL_INPUT)) is not None

def test_login_with_invalid_credentials(driver):
    wait = WebDriverWait(driver, 15)
    driver.get(f'{BASE_URL}/login')
    wait.until(EC.presence_of_element_located(LOGIN_EMAIL_INPUT))
    driver.find_element(*LOGIN_EMAIL_INPUT).send_keys('no_such_user_98765@example.com')
    driver.find_element(*LOGIN_PASSWORD_INPUT).send_keys('WrongPassword!')
    driver.find_element(*LOGIN_BUTTON).click()
    error_element = wait.until(EC.visibility_of_element_located(LOGIN_ERROR_MESSAGE))
    assert 'incorrect' in error_element.text.lower()

def test_login_with_valid_credentials(driver):
    wait = WebDriverWait(driver, 15)
    driver.get(f'{BASE_URL}/login')
    wait.until(EC.presence_of_element_located(SIGNUP_NAME_INPUT))
    unique_email = f'pytest.report.{int(time.time())}@example.com'
    password = 'PytestReport!2024'
    driver.find_element(*SIGNUP_NAME_INPUT).send_keys('Pytest Report User')
    driver.find_element(*SIGNUP_EMAIL_INPUT).send_keys(unique_email)
    driver.find_element(*SIGNUP_BUTTON).click()
    wait.until(EC.presence_of_element_located(ACCOUNT_PASSWORD_INPUT))
    driver.find_element(*ACCOUNT_PASSWORD_INPUT).send_keys(password)
    Select(driver.find_element(*ACCOUNT_DAYS_SELECT)).select_by_value('20')
    Select(driver.find_element(*ACCOUNT_MONTHS_SELECT)).select_by_visible_text('July')
    Select(driver.find_element(*ACCOUNT_YEARS_SELECT)).select_by_value('1998')
    driver.find_element(*ACCOUNT_FIRST_NAME_INPUT).send_keys('Pytest')
    driver.find_element(*ACCOUNT_LAST_NAME_INPUT).send_keys('Report')
    driver.find_element(*ACCOUNT_ADDRESS1_INPUT).send_keys('789 Report Blvd')
    Select(driver.find_element(*ACCOUNT_COUNTRY_SELECT)).select_by_visible_text('United States')
    driver.find_element(*ACCOUNT_STATE_INPUT).send_keys('New York')
    driver.find_element(*ACCOUNT_CITY_INPUT).send_keys('New York')
    driver.find_element(*ACCOUNT_ZIPCODE_INPUT).send_keys('10001')
    driver.find_element(*ACCOUNT_MOBILE_INPUT).send_keys('5551122334')
    driver.find_element(*CREATE_ACCOUNT_BUTTON).click()
    wait.until(EC.url_contains('/account_created'))
    driver.find_element(*CONTINUE_BUTTON).click()
    assert wait.until(EC.visibility_of_element_located(LOGGED_IN_AS_LINK))
    driver.find_element(*LOGOUT_LINK).click()
    wait.until(EC.url_contains('/login'))
    driver.find_element(*LOGIN_EMAIL_INPUT).send_keys(unique_email)
    driver.find_element(*LOGIN_PASSWORD_INPUT).send_keys(password)
    driver.find_element(*LOGIN_BUTTON).click()
    assert wait.until(EC.visibility_of_element_located(LOGGED_IN_AS_LINK))
