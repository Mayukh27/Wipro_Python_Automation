import os
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')

@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--window-size=1600,1000')
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = (yield)
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' and report.failed:
        drv = item.funcargs.get('driver')
        if drv is not None:
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{item.name}_{timestamp}.png'
            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            drv.save_screenshot(filepath)
            try:
                import pytest_html
                relative_path = os.path.relpath(filepath, os.path.dirname(os.path.abspath(__file__)))
                extra.append(pytest_html.extras.image(relative_path))
            except ImportError:
                pass
    report.extra = extra
