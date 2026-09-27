from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = 'https://automationexercise.com'
CONTACT_URL = f'{BASE_URL}/contact_us'


def demo_alert_on_contact_form(driver, wait):
    driver.get(CONTACT_URL)

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[data-qa='name']")
        )
    )

    driver.find_element(
        By.CSS_SELECTOR,
        "input[data-qa='name']"
    ).send_keys('Selenium Tester')

    driver.find_element(
        By.CSS_SELECTOR,
        "input[data-qa='email']"
    ).send_keys('selenium.tester@example.com')

    driver.find_element(
        By.CSS_SELECTOR,
        "input[data-qa='subject']"
    ).send_keys('Assignment 4 - Alert Handling')

    driver.find_element(
        By.CSS_SELECTOR,
        "textarea[data-qa='message']"
    ).send_keys(
        'This is an automated test message for alert handling.'
    )

    driver.find_element(
        By.CSS_SELECTOR,
        "input[data-qa='submit-button']"
    ).click()

    # AutomationExercise displays a JavaScript alert.
    alert = wait.until(EC.alert_is_present())

    print('Alert text:', alert.text)

    alert.accept()

    success_message = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.status.alert-success')
        )
    )

    assert 'successfully' in success_message.text.lower()

    print('JavaScript ALERT ACCEPT path PASSED.')


def demo_confirm_accept(driver, wait):
    driver.get(BASE_URL)

    # Create a real browser JavaScript confirm dialog
    # on the allowed AutomationExercise domain.
    driver.execute_script(
        "window.__seleniumConfirmResult = confirm("
        "'Do you want to proceed with the test?');"
    )

    confirm_dialog = wait.until(
        EC.alert_is_present()
    )

    print('Confirm text:', confirm_dialog.text)

    assert 'proceed' in confirm_dialog.text.lower()

    confirm_dialog.accept()

    print('JavaScript CONFIRM ACCEPT path PASSED.')


def demo_confirm_dismiss(driver, wait):
    driver.get(BASE_URL)

    driver.execute_script(
        "window.__seleniumConfirmResult = confirm("
        "'Do you want to proceed with the test?');"
    )

    confirm_dialog = wait.until(
        EC.alert_is_present()
    )

    print('Confirm text:', confirm_dialog.text)

    assert 'proceed' in confirm_dialog.text.lower()

    confirm_dialog.dismiss()

    print('JavaScript CONFIRM DISMISS path PASSED.')


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()

    wait = WebDriverWait(driver, 15)

    try:
        demo_alert_on_contact_form(driver, wait)
        demo_confirm_accept(driver, wait)
        demo_confirm_dismiss(driver, wait)

        print('Assignment 4 PASSED.')

    finally:
        driver.quit()


if __name__ == '__main__':
    main()