from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = 'https://automationexercise.com'
PRODUCTS_URL = f'{BASE_URL}/products'
VIDEO_TUTORIALS_URL = f'{BASE_URL}/video_tutorials'


def demo_windows_and_tabs(driver, wait):

    driver.get(BASE_URL)

    wait.until(
        EC.title_contains('Automation Exercise')
    )

    original_window = driver.current_window_handle

    assert len(driver.window_handles) == 1

    # Open another browser tab/window.
    # The URL is still one of the three allowed domains.
    driver.execute_script(
        "window.open(arguments[0], '_blank');",
        PRODUCTS_URL
    )

    wait.until(
        EC.number_of_windows_to_be(2)
    )

    all_handles = driver.window_handles

    new_window = next(
        handle
        for handle in all_handles
        if handle != original_window
    )

    driver.switch_to.window(new_window)

    wait.until(
        EC.url_contains('/products')
    )

    print(
        f"Child tab -> title: {driver.title!r}, "
        f"url: {driver.current_url!r}"
    )

    assert '/products' in driver.current_url

    products_heading = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'h2.title.text-center')
        )
    )

    assert 'all products' in products_heading.text.lower()

    print('Successfully switched to child tab.')

    # Close child tab
    driver.close()

    # Switch back to original tab
    driver.switch_to.window(original_window)

    assert driver.current_window_handle == original_window

    assert len(driver.window_handles) == 1

    assert 'automationexercise.com' in driver.current_url

    print('Successfully switched back to original tab.')

    print('Window/tab handling section PASSED.')


def demo_iframe_interaction(driver, wait):

    driver.get(VIDEO_TUTORIALS_URL)

    # Wait until at least one iframe exists.
    wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, 'iframe')
        )
    )

    iframes = driver.find_elements(
        By.TAG_NAME,
        'iframe'
    )

    assert len(iframes) > 0, (
        'Expected at least one iframe'
    )

    print(
        f'Number of iframes found: {len(iframes)}'
    )

    # Switch into the first iframe.
    first_iframe = iframes[0]

    driver.switch_to.frame(first_iframe)

    # Once inside the iframe, Selenium is operating
    # in the iframe document.
    iframe_body = wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, 'body')
        )
    )

    print(
        'Inside iframe.'
    )

    assert iframe_body is not None

    print(
        f'Iframe body detected: '
        f'{iframe_body.tag_name}'
    )

    # Return to the main document.
    driver.switch_to.default_content()

    page_heading = wait.until(
        EC.visibility_of_element_located(
            (By.TAG_NAME, 'h2')
        )
    )

    print(
        f'Main page heading: {page_heading.text!r}'
    )

    print('Iframe handling section PASSED.')


def main():

    driver = webdriver.Chrome()
    driver.maximize_window()

    wait = WebDriverWait(driver, 15)

    try:

        demo_windows_and_tabs(
            driver,
            wait
        )

        demo_iframe_interaction(
            driver,
            wait
        )

        print('Assignment 6 PASSED.')

    finally:
        driver.quit()


if __name__ == '__main__':
    main()