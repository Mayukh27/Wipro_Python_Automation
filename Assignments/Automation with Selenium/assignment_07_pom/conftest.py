import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.driver_factory import create_driver

@pytest.fixture
def driver():
    drv = create_driver(headless=os.environ.get('HEADLESS', 'false').lower() == 'true')
    yield drv
    drv.quit()
