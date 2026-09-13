from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://rahulshettyacademy.com/AutomationPractice/")

    suggestion_box = wait.until(
        EC.visibility_of_element_located((By.ID, "autocomplete"))
    )

    suggestion_box.send_keys("Ger")

    suggestions = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".ui-menu-item div"))
    )

    for suggestion in suggestions:
        if suggestion.text == "Germany":
            suggestion.click()
            break

finally:
    driver.quit()
