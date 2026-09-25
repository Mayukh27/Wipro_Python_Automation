import time

from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.dashboard_page import DashboardPage


def test_login_with_invalid_credentials_shows_error(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login("not_a_real_user_12345@example.com", "WrongPassword123!")

    assert login_page.has_login_error()
    assert "incorrect" in login_page.get_login_error_text().lower()


def test_login_with_valid_credentials_reaches_dashboard(driver):
    login_page = LoginPage(driver)
    login_page.load()

    unique_email = f"pom.milestone.{int(time.time())}@example.com"
    password = "SeleniumPOM!2024"

    login_page.start_signup("POM Test User", unique_email)

    signup_page = SignupPage(driver)
    signup_page.wait_for_account_information_form()
    signup_page.complete_registration(
        password=password,
        first_name="POM",
        last_name="Tester",
        address="123 Automation Street",
        country="United States",
        state="California",
        city="San Francisco",
        zipcode="94105",
        mobile="5551234567",
    )

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_logged_in()
    assert "pom test user" in dashboard_page.get_logged_in_username_text().lower()

    dashboard_page.logout()

    login_page.login(unique_email, password)
    assert dashboard_page.is_logged_in()
