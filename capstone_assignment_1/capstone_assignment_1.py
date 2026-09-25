import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

BASE_URL = "https://automationexercise.com"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(PROJECT_DIR, "screenshots")
REPORT_DIR = os.path.join(PROJECT_DIR, "reports")

TEST_DATA = {
    "search_keyword": "Top",
    "product_a_index": 0,
    "product_b_index": 1,
    "quantity_to_set": 4,
    "profile": {
        "email": "mayukhghosh@gmail.com",
        "password": "mayukh27",
        "first_name": "Mayukh",
        "last_name": "Ghosh",
        "dob_day": "27",
        "dob_month": "February",
        "dob_year": "2004",
        "address": "Kolkata, West Bengal",
        "country": "India",
        "state": "West Bengal",
        "city": "Kolkata",
        "zipcode": "700156",
        "mobile": "9874561536",
    },
}

NAV_LOGIN_LINK = (By.LINK_TEXT, "Signup / Login")
SIGNUP_NAME_INPUT = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
SIGNUP_EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")
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
CONTINUE_BUTTON = (By.CSS_SELECTOR, "a[data-qa='continue-button']")
LOGGED_IN_AS_LINK = (By.XPATH, "//a[contains(text(),'Logged in as')]")
SIGNUP_ALREADY_EXISTS_ERROR = (By.XPATH, "//p[contains(text(),'already exist')]")
LOGIN_EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-email']")
LOGIN_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-password']")
LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")

SEARCH_INPUT = (By.ID, "search_product")
SEARCH_BUTTON = (By.ID, "submit_search")
SEARCH_RESULTS_HEADING = (By.XPATH, "//h2[contains(text(),'Searched Products')]")
SEARCH_RESULT_LINKS = (By.CSS_SELECTOR, "div.product-image-wrapper a[href*='/product_details/']")

PRODUCT_NAME_HEADING = (By.CSS_SELECTOR, "div.product-information h2")
PRODUCT_QUANTITY_INPUT = (By.ID, "quantity")
PRODUCT_ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "div.product-information button.cart")
MODAL_CONTENT = (By.CSS_SELECTOR, "div.modal-content")
MODAL_VIEW_CART_LINK = (By.LINK_TEXT, "View Cart")
MODAL_CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "button.btn-success")

CART_TABLE = (By.ID, "cart_info")
CART_ROWS = (By.CSS_SELECTOR, "#cart_info tbody tr")


def create_driver():
    options = Options()
    options.add_argument("--window-size=1600,1000")
    driver = webdriver.Chrome(options=options)
    return driver


def take_screenshot(driver, label):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = label + "_" + timestamp + ".png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(filepath)
    return filename


def handle_alert_if_present(driver, timeout=3, accept=True):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
    except TimeoutException:
        return None
    alert = driver.switch_to.alert
    alert_text = alert.text
    if accept:
        alert.accept()
    else:
        alert.dismiss()
    return alert_text


def record(report, step, status, message, screenshot=None):
    report.append({
        "step": step,
        "status": status,
        "message": message,
        "screenshot": screenshot,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    print("[" + status + "] " + step + " - " + message)


def step_login(driver, wait, data, report):
    driver.get(BASE_URL + "/login")
    wait.until(EC.presence_of_element_located(SIGNUP_NAME_INPUT))

    profile = data["profile"]
    email = profile["email"]
    full_name = profile["first_name"] + " " + profile["last_name"]

    driver.find_element(*SIGNUP_NAME_INPUT).send_keys(full_name)
    driver.find_element(*SIGNUP_EMAIL_INPUT).send_keys(email)
    driver.find_element(*SIGNUP_BUTTON).click()

    already_exists = False
    try:
        WebDriverWait(driver, 4).until(
            EC.visibility_of_element_located(SIGNUP_ALREADY_EXISTS_ERROR)
        )
        already_exists = True
    except TimeoutException:
        already_exists = False

    if already_exists:
        driver.find_element(*LOGIN_EMAIL_INPUT).send_keys(email)
        driver.find_element(*LOGIN_PASSWORD_INPUT).send_keys(profile["password"])
        driver.find_element(*LOGIN_BUTTON).click()
        wait.until(EC.visibility_of_element_located(LOGGED_IN_AS_LINK))
        logged_in_text = driver.find_element(*LOGGED_IN_AS_LINK).text
        assert "logged in as" in logged_in_text.lower(), "Login did not succeed, header text was: " + logged_in_text
        screenshot = take_screenshot(driver, "01_login_success")
        record(report, "Login", "PASS", "Account already existed, logged in directly, header shows: " + logged_in_text, screenshot)
        return email, profile["password"]

    wait.until(EC.url_contains("/signup"))
    wait.until(EC.presence_of_element_located(ACCOUNT_PASSWORD_INPUT))

    driver.find_element(*ACCOUNT_PASSWORD_INPUT).send_keys(profile["password"])
    Select(driver.find_element(*ACCOUNT_DAYS_SELECT)).select_by_value(profile["dob_day"])
    Select(driver.find_element(*ACCOUNT_MONTHS_SELECT)).select_by_visible_text(profile["dob_month"])
    Select(driver.find_element(*ACCOUNT_YEARS_SELECT)).select_by_value(profile["dob_year"])
    driver.find_element(*ACCOUNT_FIRST_NAME_INPUT).send_keys(profile["first_name"])
    driver.find_element(*ACCOUNT_LAST_NAME_INPUT).send_keys(profile["last_name"])
    driver.find_element(*ACCOUNT_ADDRESS1_INPUT).send_keys(profile["address"])
    Select(driver.find_element(*ACCOUNT_COUNTRY_SELECT)).select_by_visible_text(profile["country"])
    driver.find_element(*ACCOUNT_STATE_INPUT).send_keys(profile["state"])
    driver.find_element(*ACCOUNT_CITY_INPUT).send_keys(profile["city"])
    driver.find_element(*ACCOUNT_ZIPCODE_INPUT).send_keys(profile["zipcode"])
    driver.find_element(*ACCOUNT_MOBILE_INPUT).send_keys(profile["mobile"])
    driver.find_element(*CREATE_ACCOUNT_BUTTON).click()

    wait.until(EC.url_contains("/account_created"))
    driver.find_element(*CONTINUE_BUTTON).click()

    wait.until(EC.visibility_of_element_located(LOGGED_IN_AS_LINK))
    logged_in_text = driver.find_element(*LOGGED_IN_AS_LINK).text
    assert "logged in as" in logged_in_text.lower(), "Login did not succeed, header text was: " + logged_in_text

    screenshot = take_screenshot(driver, "01_login_success")
    record(report, "Login", "PASS", "Registered and logged in as new user, header shows: " + logged_in_text, screenshot)
    return email, profile["password"]


def step_search_product(driver, wait, keyword, report):
    driver.get(BASE_URL + "/products")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.features_items")))

    search_box = wait.until(EC.presence_of_element_located(SEARCH_INPUT))
    search_box.clear()
    search_box.send_keys(keyword)
    driver.find_element(*SEARCH_BUTTON).click()

    heading = wait.until(EC.visibility_of_element_located(SEARCH_RESULTS_HEADING))
    assert "searched products" in heading.text.lower(), "Search results heading showed unexpected text: " + heading.text

    result_links = wait.until(EC.presence_of_all_elements_located(SEARCH_RESULT_LINKS))
    result_urls = [link.get_attribute("href") for link in result_links]
    assert len(result_urls) >= 2, "Expected at least two search results for keyword: " + keyword

    screenshot = take_screenshot(driver, "02_product_search")
    record(report, "Product Search", "PASS", "Search for '" + keyword + "' returned " + str(len(result_urls)) + " results", screenshot)
    return result_urls


def step_add_product_to_cart(driver, wait, product_url, report):
    driver.get(product_url)
    wait.until(EC.presence_of_element_located(PRODUCT_NAME_HEADING))
    product_name = driver.find_element(*PRODUCT_NAME_HEADING).text.strip()

    add_to_cart_button = wait.until(EC.element_to_be_clickable(PRODUCT_ADD_TO_CART_BUTTON))
    add_to_cart_button.click()

    alert_text = handle_alert_if_present(driver, timeout=2)
    if alert_text is not None:
        record(report, "Popup/Alert Check", "PASS", "Alert appeared after Add To Cart and was handled: " + alert_text)

    wait.until(EC.visibility_of_element_located(MODAL_CONTENT))
    driver.find_element(*MODAL_VIEW_CART_LINK).click()
    wait.until(EC.url_contains("/view_cart"))
    wait.until(EC.presence_of_element_located(CART_TABLE))

    screenshot = take_screenshot(driver, "03_add_to_cart")
    record(report, "Add Product To Cart", "PASS", "Added '" + product_name + "' to cart with default quantity", screenshot)
    return product_name


def step_update_quantity_and_add_second_product(driver, wait, product_url, quantity, report):
    driver.get(product_url)
    wait.until(EC.presence_of_element_located(PRODUCT_NAME_HEADING))
    product_name = driver.find_element(*PRODUCT_NAME_HEADING).text.strip()

    quantity_input = wait.until(EC.visibility_of_element_located(PRODUCT_QUANTITY_INPUT))
    quantity_input.clear()
    quantity_input.send_keys(str(quantity))
    actual_value = quantity_input.get_attribute("value")
    assert actual_value == str(quantity), "Quantity field shows " + actual_value + ", expected " + str(quantity)

    screenshot_before = take_screenshot(driver, "04_quantity_updated")
    record(report, "Update Quantity", "PASS", "Quantity field for '" + product_name + "' updated to " + str(quantity), screenshot_before)

    add_to_cart_button = wait.until(EC.element_to_be_clickable(PRODUCT_ADD_TO_CART_BUTTON))
    add_to_cart_button.click()

    alert_text = handle_alert_if_present(driver, timeout=2)
    if alert_text is not None:
        record(report, "Popup/Alert Check", "PASS", "Alert appeared after Add To Cart and was handled: " + alert_text)

    wait.until(EC.visibility_of_element_located(MODAL_CONTENT))
    driver.find_element(*MODAL_VIEW_CART_LINK).click()
    wait.until(EC.url_contains("/view_cart"))
    wait.until(EC.presence_of_element_located(CART_TABLE))

    return product_name, quantity


def parse_rupee_amount(text):
    digits = "".join(character for character in text if character.isdigit())
    return int(digits) if digits else 0


def step_verify_cart_details(driver, wait, expected, report):
    wait.until(EC.presence_of_element_located(CART_TABLE))
    rows = wait.until(EC.presence_of_all_elements_located(CART_ROWS))
    assert len(rows) >= len(expected), "Expected at least " + str(len(expected)) + " rows in the cart"

    found = {}
    for row in rows:
        name = row.find_element(By.CSS_SELECTOR, "td.cart_description h4").text.strip()
        unit_price_text = row.find_element(By.CSS_SELECTOR, "td.cart_price p").text.strip()
        quantity_text = row.find_element(By.CSS_SELECTOR, "td.cart_quantity button").text.strip()
        total_text = row.find_element(By.CSS_SELECTOR, "td.cart_total p").text.strip()
        found[name.lower()] = {
            "display_name": name,
            "unit_price": parse_rupee_amount(unit_price_text),
            "quantity": int(quantity_text),
            "total": parse_rupee_amount(total_text),
        }

    for product_name, expected_quantity in expected.items():
        lookup_key = product_name.lower()
        assert lookup_key in found, "Product not found in cart: " + product_name
        row_data = found[lookup_key]
        assert row_data["quantity"] == expected_quantity, (
            "Quantity mismatch for " + row_data["display_name"] + ": expected " + str(expected_quantity)
            + ", found " + str(row_data["quantity"])
        )
        expected_total = row_data["unit_price"] * row_data["quantity"]
        assert row_data["total"] == expected_total, (
            "Total price mismatch for " + row_data["display_name"] + ": expected " + str(expected_total)
            + ", found " + str(row_data["total"])
        )

    screenshot = take_screenshot(driver, "05_cart_verified")
    record(report, "Verify Cart Details", "PASS", "Verified product names, quantities and line totals for " + str(len(expected)) + " products", screenshot)

def clear_cart(driver, wait):
    driver.get(BASE_URL + "/view_cart")

    wait.until(EC.presence_of_element_located(CART_TABLE))

    rows = driver.find_elements(*CART_ROWS)

    for row in rows:
        try:
            delete_button = row.find_element(
                By.CSS_SELECTOR,
                "td.cart_delete a.cart_quantity_delete"
            )
            delete_button.click()

            wait.until(
                EC.staleness_of(row)
            )
        except Exception:
            pass

    
    wait.until(
        lambda d: len(d.find_elements(*CART_ROWS)) == 0
    )
def write_html_report(report, overall_status, path):
    os.makedirs(REPORT_DIR, exist_ok=True)
    rows_html = ""
    for entry in report:
        if entry["screenshot"] is not None:
            image_html = "<img src='../screenshots/" + entry["screenshot"] + "' width='220'>"
        else:
            image_html = "-"
        status_class = "pass" if entry["status"] == "PASS" else "fail"
        rows_html += (
            "<tr class='" + status_class + "'>"
            + "<td>" + entry["step"] + "</td>"
            + "<td>" + entry["status"] + "</td>"
            + "<td>" + entry["message"] + "</td>"
            + "<td>" + entry["timestamp"] + "</td>"
            + "<td>" + image_html + "</td>"
            + "</tr>"
        )

    html = (
        "<html><head><title>Capstone Assignment 1 Execution Report</title>"
        "<style>"
        "body{font-family:Arial,sans-serif;margin:24px;}"
        "table{border-collapse:collapse;width:100%;}"
        "th,td{border:1px solid #ccc;padding:8px;text-align:left;vertical-align:top;}"
        "th{background:#333;color:#fff;}"
        "tr.pass{background:#eaffea;}"
        "tr.fail{background:#ffeaea;}"
        "h1{margin-bottom:4px;}"
        ".summary{margin-bottom:16px;font-weight:bold;}"
        "</style></head><body>"
        "<h1>Capstone Assignment 1 - Execution Report</h1>"
        "<div class='summary'>Overall Status: " + overall_status + " | Generated: "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "</div>"
        "<table><tr><th>Step</th><th>Status</th><th>Message</th><th>Timestamp</th><th>Screenshot</th></tr>"
        + rows_html + "</table></body></html>"
    )

    with open(path, "w", encoding="utf-8") as report_file:
        report_file.write(html)


def main():
    data = TEST_DATA
    report = []
    overall_status = "PASS"
    driver = create_driver()
    wait = WebDriverWait(driver, 15)
    report_path = os.path.join(REPORT_DIR, "execution_report.html")

    try:
        driver.get(BASE_URL)
        wait.until(EC.title_contains("Automation Exercise"))
        screenshot = take_screenshot(driver, "00_browser_launch")
        record(report, "Browser Launch", "PASS", "Chrome launched and home page loaded", screenshot)

        step_login(driver, wait, data, report)
        clear_cart(driver, wait)
        result_urls = step_search_product(driver, wait, data["search_keyword"], report)
        product_a_url = result_urls[data["product_a_index"]]
        product_b_url = result_urls[data["product_b_index"]]

        product_a_name = step_add_product_to_cart(driver, wait, product_a_url, report)
        product_b_name, quantity_b = step_update_quantity_and_add_second_product(
            driver, wait, product_b_url, data["quantity_to_set"], report
        )

        expected_cart = {product_a_name: 1, product_b_name: quantity_b}
        step_verify_cart_details(driver, wait, expected_cart, report)

    except Exception as error:
        overall_status = "FAIL"
        failure_screenshot = take_screenshot(driver, "99_failure")
        record(report, "Unhandled Error", "FAIL", str(error), failure_screenshot)
        raise

    finally:
        write_html_report(report, overall_status, report_path)
        driver.quit()
        print("Execution report written to: " + report_path)


if __name__ == "__main__":
    main()