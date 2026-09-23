import json
import os
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = 'https://automationexercise.com'
TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test_data')
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

@when('the user attempts login using each combination in "{data_filename}"')
def step_attempt_login_from_json(context, data_filename):
    data_path = os.path.join(TEST_DATA_DIR, data_filename)
    with open(data_path, encoding='utf-8') as data_file:
        combinations = json.load(data_file)
    context.json_attempt_results = []
    for combo in combinations:
        context.driver.get(f'{BASE_URL}/login')
        context.wait.until(EC.presence_of_element_located(LOGIN_EMAIL_INPUT))
        context.driver.find_element(*LOGIN_EMAIL_INPUT).send_keys(combo['email'])
        context.driver.find_element(*LOGIN_PASSWORD_INPUT).send_keys(combo['password'])
        context.driver.find_element(*LOGIN_BUTTON).click()
        error_element = context.wait.until(EC.visibility_of_element_located(LOGIN_ERROR_MESSAGE))
        context.json_attempt_results.append('incorrect' in error_element.text.lower())

@then('every attempt should be rejected with an incorrect credentials error')
def step_verify_all_json_attempts_rejected(context):
    assert context.json_attempt_results, 'No JSON-driven login attempts were executed'
    assert all(context.json_attempt_results), f'Some JSON-driven login attempts did not show the expected error: {context.json_attempt_results}'
