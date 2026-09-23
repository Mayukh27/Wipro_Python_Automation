from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = 'https://automationexercise.com'
LOGIN_EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-email']")
LOGIN_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-password']")
LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
LOGIN_ERROR_MESSAGE = (By.CSS_SELECTOR, 'div.login-form p')

@given('the user is on the Automation Exercise login page')
def step_open_login_page(context):
    context.wait = WebDriverWait(context.driver, 15)
    context.driver.get(f'{BASE_URL}/login')
    context.wait.until(EC.presence_of_element_located(LOGIN_EMAIL_INPUT))

@when('the user logs in with email "{email}" and password "{password}"')
def step_perform_login(context, email, password):
    context.driver.find_element(*LOGIN_EMAIL_INPUT).send_keys(email)
    context.driver.find_element(*LOGIN_PASSWORD_INPUT).send_keys(password)
    context.driver.find_element(*LOGIN_BUTTON).click()

@then('the user should see an incorrect credentials error')
def step_verify_error(context):
    error_element = context.wait.until(EC.visibility_of_element_located(LOGIN_ERROR_MESSAGE))
    assert 'incorrect' in error_element.text.lower(), f'Expected an incorrect-credentials message, got: {error_element.text!r}'
