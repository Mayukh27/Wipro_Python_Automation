from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
AE_BASE_URL = 'https://automationexercise.com'
IFRAME_URL = 'https://the-internet.herokuapp.com/iframe'

def demo_windows_and_tabs(driver, wait):
    driver.get(AE_BASE_URL)
    wait.until(EC.title_contains('Automation Exercise'))
    original_window = driver.current_window_handle
    original_handles = driver.window_handles
    assert len(original_handles) == 1
    video_tutorials_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Video Tutorials')))
    video_tutorials_link.click()
    wait.until(EC.number_of_windows_to_be(2))
    all_handles = driver.window_handles
    new_window = [handle for handle in all_handles if handle != original_window][0]
    driver.switch_to.window(new_window)
    wait.until(lambda d: 'youtube' in d.current_url.lower() or 'google' in d.current_url.lower())
    child_title = driver.title
    child_url = driver.current_url
    print(f'Child tab -> title: {child_title!r}, url: {child_url}')
    assert child_url != f'{AE_BASE_URL}/'
    driver.close()
    driver.switch_to.window(original_window)
    assert driver.current_window_handle == original_window
    assert len(driver.window_handles) == 1
    assert 'automationexercise.com' in driver.current_url
    print('Window/tab handling section PASSED.')

def demo_iframe_interaction(driver, wait):
    driver.get(IFRAME_URL)
    iframe_element = wait.until(EC.presence_of_element_located((By.ID, 'mce_0_ifr')))
    driver.switch_to.frame(iframe_element)
    editor_body = wait.until(EC.presence_of_element_located((By.ID, 'tinymce')))
    editor_body.clear()
    editor_body.send_keys('Editing content inside a real iframe via Selenium.')
    assert 'real iframe' in editor_body.text
    driver.switch_to.default_content()
    page_heading = driver.find_element(By.TAG_NAME, 'h3')
    assert 'iframe' in page_heading.text.lower()
    print('Iframe handling section PASSED.')

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    try:
        demo_windows_and_tabs(driver, wait)
        demo_iframe_interaction(driver, wait)
        print('Assignment 6 PASSED.')
    finally:
        driver.quit()
if __name__ == '__main__':
    main()
