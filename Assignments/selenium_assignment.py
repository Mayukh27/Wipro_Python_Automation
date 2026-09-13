from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
import time


def main():

    # Initialize driver as None so that finally can safely check it.
    driver = None

    try:

        driver = webdriver.Chrome()
        driver.maximize_window()

        print("Opening Selenium practice website...")

        driver.get("https://www.selenium.dev/selenium/web/web-form.html")

        time.sleep(2)

        # 1: VERIFY PAGE TITLE

        expected_title = "Web form"
        actual_title = driver.title

        if expected_title in actual_title:

            print("SUCCESS: Page title verified")
            print("Page Title:", actual_title)

        else:

            raise AssertionError(
                f"Expected title containing '{expected_title}', "
                f"but found '{actual_title}'"
            )

        time.sleep(2)

        # CREATE EXPLICIT WAIT

        wait = WebDriverWait(driver, 10) # A 10-second explicit wait is used instead of relying only on fixed delays.
                

        # 2: INTERACT WITH TEXT INPUT

        print("Entering text...")

        text_input = wait.until(EC.visibility_of_element_located((By.NAME, "my-text")))

        text_input.send_keys("Selenium Automation Demo")

        print("SUCCESS: Text entered")

        time.sleep(2)

        # 3: INTERACT WITH CHECKBOX

        print("Selecting checkbox...")

        checkbox = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox']"))
        )

        if not checkbox.is_selected():

            checkbox.click()

        print("SUCCESS: Checkbox selected")

        time.sleep(2)

        # 4: INTERACT WITH DROPDOWN

        print("Selecting dropdown option...")

        dropdown = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "select")))

        select = Select(dropdown)

        select.select_by_visible_text("Two")

        print("SUCCESS: Dropdown option selected")

        time.sleep(2)

        # 5: LOCATE AND SUBMIT FORM

        print("Waiting for submit button...")

        submit_button = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )

        # Scroll button into the center of the visible screen.
        driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            submit_button,
        )

        time.sleep(2)

        # Wait again until Selenium determines the button is
        # clickable after scrolling.
        submit_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )

        print("Submitting form...")

        try:

            # Normal Selenium click.
            submit_button.click()

        except ElementClickInterceptedException:

            # Fallback if another page element intercepts
            # Selenium's normal mouse click.
            print(
                "Normal click was intercepted. " "Using JavaScript click as fallback..."
            )

            driver.execute_script("arguments[0].click();", submit_button)

        # 6: WAIT FOR SUCCESSFUL RESULT
        #
        # EXPLICIT WAIT:
        # Wait until the result message becomes visible.
        #
        # This is a meaningful wait because it confirms that
        # the form submission was completed successfully.

        print("Waiting for successful submission result...")

        result_message = wait.until(
            EC.visibility_of_element_located((By.ID, "message"))
        )

        print("SUCCESS: Form submitted successfully!")

        print("Result message:", result_message.text)

        time.sleep(3)

        # 7: CAPTURE SCREENSHOT
        #
        # The screenshot is taken only after successful
        # interaction with the form.

        screenshot_name = "selenium_success.png"

        driver.save_screenshot(screenshot_name)

        print(f"SUCCESS: Screenshot saved as " f"'{screenshot_name}'")

        time.sleep(2)

        # 8: HANDLE EXPECTED FAILURE
        #
        # We intentionally search for an element that does not
        # exist. The expected exception is caught and handled
        # with a useful error message.

        print("Demonstrating expected failure...")

        try:

            driver.find_element(By.ID, "element-that-does-not-exist")

        except NoSuchElementException:

            print(
                "EXPECTED FAILURE HANDLED: "
                "The requested element "
                "'element-that-does-not-exist' "
                "does not exist on this page."
            )

        time.sleep(3)
    # HANDLE TIMEOUT ERROR

    except TimeoutException as error:

        print(
            "TIMEOUT ERROR: "
            "An expected element did not become ready "
            "within 10 seconds."
        )

        print("Details:", error)
    # HANDLE TITLE VERIFICATION ERRO

    except AssertionError as error:

        print("TITLE VERIFICATION ERROR:")

        print(error)
    # HANDLE OTHER UNEXPECTED ERROR

    except Exception as error:

        print("UNEXPECTED ERROR:")

        print(error)
    # SAFELY CLOSE BROWSE

    finally:

        if driver is not None:

            print("Closing browser safely...")

            time.sleep(2)

            driver.quit()

            print("Browser session closed safely.")


if __name__ == "__main__":

    main()
