import time
from behave import given, when, then
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@given('the user opens the login page')
def step_open_login_page(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.load()

@when('the user submits login credentials "{email}" and "{password}"')
def step_submit_login_credentials(context, email, password):
    context.login_page.login(email, password)

@then('the login page should show an incorrect credentials error')
def step_verify_login_error(context):
    assert context.login_page.has_login_error()
    assert 'incorrect' in context.login_page.get_login_error_text().lower()

@when('the user registers a new account and completes their profile')
def step_register_new_account(context):
    unique_email = f'behave.pom.{int(time.time())}@example.com'
    context.registered_password = 'BehavePOM!2024'
    context.login_page.start_signup('Behave POM User', unique_email)
    context.login_page.complete_registration(password=context.registered_password, first_name='Behave', last_name='POM', address='321 Gherkin Way', country='United States', state='Washington', city='Seattle', zipcode='98101', mobile='5554443322')

@then('the dashboard should show the user as logged in')
def step_verify_dashboard_logged_in(context):
    context.dashboard_page = DashboardPage(context.driver)
    assert context.dashboard_page.is_logged_in()
    assert 'logged in as' in context.dashboard_page.get_logged_in_username_text().lower()
