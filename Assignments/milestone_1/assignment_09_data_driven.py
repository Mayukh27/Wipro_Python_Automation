import csv
import json
import os
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BASE_URL = 'https://automationexercise.com'
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def load_csv_test_data(path):
    test_cases = []
    with open(path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            test_cases.append({'test_id': row['test_id'], 'search_term': row['search_term'], 'expect_results': row['expect_results'].strip().lower() == 'yes'})
    return test_cases

def load_json_test_data(path):
    with open(path, encoding='utf-8') as json_file:
        raw_cases = json.load(json_file)
    return [{'test_id': case['test_id'], 'search_term': case['search_term'], 'expect_results': str(case['expect_results']).strip().lower() == 'yes'} for case in raw_cases]

def load_xlsx_test_data(path):
    workbook = openpyxl.load_workbook(path, data_only=True)
    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    headers = [str(header).strip() for header in rows[0]]
    test_cases = []
    for row in rows[1:]:
        record = dict(zip(headers, row))
        test_cases.append({'test_id': record['test_id'], 'search_term': record['search_term'], 'expect_results': str(record['expect_results']).strip().lower() == 'yes'})
    return test_cases

def run_search_test_case(driver, wait, test_case):
    driver.get(f'{BASE_URL}/products')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.features_items')))
    search_box = wait.until(EC.presence_of_element_located((By.ID, 'search_product')))
    search_box.clear()
    search_box.send_keys(test_case['search_term'])
    driver.find_element(By.ID, 'submit_search').click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.title.text-center')))
    result_products = driver.find_elements(By.CSS_SELECTOR, 'div.product-image-wrapper')
    has_results = len(result_products) > 0
    status = 'PASSED' if has_results == test_case['expect_results'] else 'FAILED'
    print(f"[{test_case['test_id']}] search='{test_case['search_term']}' expected_results={test_case['expect_results']} actual_results={has_results} -> {status}")
    assert has_results == test_case['expect_results'], f'Test case {test_case['test_id']} failed: expected_results={test_case['expect_results']}, actual={has_results}'

def main():
    csv_cases = load_csv_test_data(os.path.join(DATA_DIR, 'test_data.csv'))
    json_cases = load_json_test_data(os.path.join(DATA_DIR, 'test_data.json'))
    xlsx_cases = load_xlsx_test_data(os.path.join(DATA_DIR, 'test_data.xlsx'))
    all_cases = csv_cases + json_cases + xlsx_cases
    assert all_cases, 'No test cases were loaded from any data source'
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    try:
        for test_case in all_cases:
            run_search_test_case(driver, wait, test_case)
        print(f'Assignment 9 PASSED: {len(all_cases)} data-driven cases executed successfully.')
    finally:
        driver.quit()
if __name__ == '__main__':
    main()
