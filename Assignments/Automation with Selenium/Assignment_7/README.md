# Assignment 7 - Page Object Model

Site: https://automationexercise.com/

## Structure

- `pages/base_page.py` - shared Selenium operations
- `pages/login_page.py` - login form locators + actions
- `pages/signup_page.py` - account-registration form locators + actions
- `pages/dashboard_page.py` - logged-in state locators + actions
- `tests/test_login.py` - invalid-login and full signup-to-login flow
- `utils/driver_factory.py` - Chrome WebDriver creation
- `conftest.py` - pytest `driver` fixture

## Run

```bash
pip install -r requirements.txt
pytest -v
```
