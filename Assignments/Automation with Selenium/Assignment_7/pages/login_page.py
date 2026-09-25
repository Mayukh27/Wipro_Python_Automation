from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://automationexercise.com/login"

    NAV_LOGIN_LINK = (By.LINK_TEXT, "Signup / Login")
    LOGIN_EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    LOGIN_ERROR_MESSAGE = (By.CSS_SELECTOR, "div.login-form p")

    SIGNUP_NAME_INPUT = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")

    def load(self):
        self.open(self.URL)
        self.wait_for_url_contains("/login")

    def login(self, email, password):
        self.type_text(self.LOGIN_EMAIL_INPUT, email)
        self.type_text(self.LOGIN_PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_login_error_text(self):
        return self.get_text(self.LOGIN_ERROR_MESSAGE)

    def has_login_error(self):
        return self.is_visible(self.LOGIN_ERROR_MESSAGE, timeout=5)

    def start_signup(self, name, email):
        self.type_text(self.SIGNUP_NAME_INPUT, name)
        self.type_text(self.SIGNUP_EMAIL_INPUT, email)
        self.click(self.SIGNUP_BUTTON)
        self.wait_for_url_contains("/signup")
