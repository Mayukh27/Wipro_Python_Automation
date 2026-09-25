from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class SignupPage(BasePage):
    ACCOUNT_PASSWORD_INPUT = (By.ID, "password")
    ACCOUNT_DAYS_SELECT = (By.ID, "days")
    ACCOUNT_MONTHS_SELECT = (By.ID, "months")
    ACCOUNT_YEARS_SELECT = (By.ID, "years")
    ACCOUNT_FIRST_NAME_INPUT = (By.ID, "first_name")
    ACCOUNT_LAST_NAME_INPUT = (By.ID, "last_name")
    ACCOUNT_ADDRESS1_INPUT = (By.ID, "address1")
    ACCOUNT_COUNTRY_SELECT = (By.ID, "country")
    ACCOUNT_STATE_INPUT = (By.ID, "state")
    ACCOUNT_CITY_INPUT = (By.ID, "city")
    ACCOUNT_ZIPCODE_INPUT = (By.ID, "zipcode")
    ACCOUNT_MOBILE_INPUT = (By.ID, "mobile_number")
    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[data-qa='create-account']")
    ACCOUNT_CREATED_HEADER = (By.CSS_SELECTOR, "h2[data-qa='account-created']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    def wait_for_account_information_form(self):
        self.wait_for_url_contains("/signup")
        self.find(self.ACCOUNT_PASSWORD_INPUT)

    def complete_registration(self, password, first_name, last_name, address,
                               country, state, city, zipcode, mobile):
        self.type_text(self.ACCOUNT_PASSWORD_INPUT, password)
        Select(self.find(self.ACCOUNT_DAYS_SELECT)).select_by_value("10")
        Select(self.find(self.ACCOUNT_MONTHS_SELECT)).select_by_visible_text("May")
        Select(self.find(self.ACCOUNT_YEARS_SELECT)).select_by_value("1996")
        self.type_text(self.ACCOUNT_FIRST_NAME_INPUT, first_name)
        self.type_text(self.ACCOUNT_LAST_NAME_INPUT, last_name)
        self.type_text(self.ACCOUNT_ADDRESS1_INPUT, address)
        Select(self.find(self.ACCOUNT_COUNTRY_SELECT)).select_by_visible_text(country)
        self.type_text(self.ACCOUNT_STATE_INPUT, state)
        self.type_text(self.ACCOUNT_CITY_INPUT, city)
        self.type_text(self.ACCOUNT_ZIPCODE_INPUT, zipcode)
        self.type_text(self.ACCOUNT_MOBILE_INPUT, mobile)
        self.click(self.CREATE_ACCOUNT_BUTTON)
        self.wait_for_url_contains("/account_created")
        self.click(self.CONTINUE_BUTTON)
