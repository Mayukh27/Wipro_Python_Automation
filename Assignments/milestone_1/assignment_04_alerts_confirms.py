from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
AE_CONTACT_URL = 'https://automationexercise.com/contact_us'
FALLBACK_ALERTS_URL = 'https://the-internet.herokuapp.com/javascript_alerts'

def demo_confirm_dialog_on_automation_exercise(driver, wait):
    driver.get(AE_CONTACT_URL)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-qa='name']")))
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='name']").send_keys('Selenium Tester')
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='email']").send_keys('selenium.tester@example.com')
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='subject']").send_keys('Milestone 1 - Alert Handling')
    driver.find_element(By.CSS_SELECTOR, "textarea[data-qa='message']").send_keys('This is an automated message used to exercise JS confirm() handling.')
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='submit-button']").click()
    confirm_dialog = wait.until(EC.alert_is_present())
    dialog_text = confirm_dialog.text
    assert 'proceed' in dialog_text.lower(), f'Unexpected dialog text: {dialog_text!r}'
    confirm_dialog.accept()
    success_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.status.alert-success')))
    assert 'successfully' in success_message.text.lower()
    print('Confirm dialog ACCEPT path PASSED.')
    driver.get(AE_CONTACT_URL)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-qa='name']")))
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='name']").send_keys('Selenium Tester')
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='email']").send_keys('selenium.tester@example.com')
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='subject']").send_keys('Milestone 1 - Dismiss Path')
    driver.find_element(By.CSS_SELECTOR, "textarea[data-qa='message']").send_keys('This message should never be submitted because the dialog is dismissed.')
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='submit-button']").click()
    confirm_dialog = wait.until(EC.alert_is_present())
    confirm_dialog.dismiss()
    still_on_contact_page = 'contact_us' in driver.current_url
    assert still_on_contact_page
    print('Confirm dialog DISMISS path PASSED.')

def demo_alert_and_prompt_on_fallback_page(driver, wait):
    driver.get(FALLBACK_ALERTS_URL)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[onclick='jsAlert()']")))
    driver.find_element(By.CSS_SELECTOR, "button[onclick='jsAlert()']").click()
    alert = wait.until(EC.alert_is_present())
    assert alert.text == 'I am a JS Alert'
    alert.accept()
    result_text = wait.until(EC.visibility_of_element_located((By.ID, 'result'))).text
    assert 'successfully clicked an alert' in result_text.lower()
    driver.find_element(By.CSS_SELECTOR, "button[onclick='jsPrompt()']").click()
    prompt_dialog = wait.until(EC.alert_is_present())
    prompt_dialog.send_keys('Selenium Milestone 1')
    prompt_dialog.accept()
    result_text = wait.until(EC.text_to_be_present_in_element((By.ID, 'result'), 'Selenium Milestone 1'))
    assert result_text
    print('Fallback alert()/prompt() section PASSED on the-internet.herokuapp.com.')

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    try:
        demo_confirm_dialog_on_automation_exercise(driver, wait)
        demo_alert_and_prompt_on_fallback_page(driver, wait)
        print('Assignment 4 PASSED.')
    finally:
        driver.quit()
if __name__ == '__main__':
    main()
