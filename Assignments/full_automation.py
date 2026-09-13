from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://testautomationpractice.blogspot.com/")

    wait.until(
        EC.visibility_of_element_located((By.ID, "name"))
    ).send_keys("Mayukh")

    driver.find_element(By.ID, "email").send_keys("mayukh@example.com")
    driver.find_element(By.ID, "phone").send_keys("9876543210")
    driver.find_element(By.ID, "textarea").send_keys("Kolkata, West Bengal, India")

    driver.find_element(By.ID, "male").click()

    driver.find_element(By.ID, "monday").click()
    driver.find_element(By.ID, "wednesday").click()
    driver.find_element(By.ID, "friday").click()

    country = Select(driver.find_element(By.ID, "country"))
    country.select_by_visible_text("India")

    colors = Select(driver.find_element(By.ID, "colors"))
    colors.select_by_visible_text("Red")

    animals = Select(driver.find_element(By.ID, "animals"))
    animals.select_by_visible_text("Cat")

    driver.find_element(By.ID, "datepicker").send_keys("08/31/2026")

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        driver.find_element(By.XPATH, "//table[@name='BookTable']")
    )

    rows = driver.find_elements(
        By.XPATH,
        "//table[@name='BookTable']//tr"
    )

    print("Total static table rows:", len(rows) - 1)

    books = driver.find_elements(
        By.XPATH,
        "//table[@name='BookTable']//tr/td[1]"
    )

    for book in books:
        print(book.text)

    dynamic_rows = driver.find_elements(
        By.XPATH,
        "//table[@id='taskTable']//tbody/tr"
    )

    print("Dynamic table rows:", len(dynamic_rows))

    driver.find_element(By.XPATH, "//button[text()='Simple Alert']").click()

    wait.until(EC.alert_is_present())

    alert = driver.switch_to.alert
    print(alert.text)
    alert.accept()

    driver.find_element(
        By.XPATH,
        "//button[text()='Confirmation Alert']"
    ).click()

    wait.until(EC.alert_is_present())

    alert = driver.switch_to.alert
    print(alert.text)
    alert.accept()

    driver.find_element(
        By.XPATH,
        "//button[text()='Prompt Alert']"
    ).click()

    wait.until(EC.alert_is_present())

    alert = driver.switch_to.alert
    alert.send_keys("Mayukh")
    alert.accept()

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        driver.find_element(By.XPATH, "//button[text()='Point Me']")
    )

    hover_button = driver.find_element(
        By.XPATH,
        "//button[text()='Point Me']"
    )

    ActionChains(driver).move_to_element(hover_button).perform()

    wait.until(
        EC.visibility_of_element_located(
            (By.LINK_TEXT, "Mobiles")
        )
    )

    driver.find_element(By.LINK_TEXT, "Mobiles").click()

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        driver.find_element(By.ID, "field1")
    )

    field1 = driver.find_element(By.ID, "field1")
    field2 = driver.find_element(By.ID, "field2")

    field1.send_keys("Selenium Automation")

    copy_button = driver.find_element(
        By.XPATH,
        "//button[text()='Copy Text']"
    )

    ActionChains(driver).double_click(copy_button).perform()

    print("Field 2 value:", field2.get_attribute("value"))

    
    #driver.save_screenshot("testautomationpractice_result.png")

    print("Automation completed successfully.")

except TimeoutException as e:
    print("Timeout error: Element or condition was not available within the expected time.")

except NoSuchElementException as e:
    print("Element not found. Please verify the locator or page structure.")

except Exception as e:
    print("Unexpected error:", e)

finally:
    time.sleep(3)
    driver.quit()