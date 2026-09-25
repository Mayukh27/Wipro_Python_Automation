from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    LOGGED_IN_AS_LINK = (By.XPATH, "//a[contains(text(),'Logged in as')]")
    LOGOUT_LINK = (By.LINK_TEXT, 'Logout')

    def is_logged_in(self):
        return self.is_visible(self.LOGGED_IN_AS_LINK, timeout=10)

    def get_logged_in_username_text(self):
        return self.get_text(self.LOGGED_IN_AS_LINK)

    def logout(self):
        self.click(self.LOGOUT_LINK)
        self.wait_for_url_contains('/login')
