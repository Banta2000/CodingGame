import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re


URLNAME = "leap-of-sheep"
URL = "https://www.codingame.com/ide/puzzle/" + URLNAME


def setup_selenium_driver():
    """Set up Chrome WebDriver with appropriate options."""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # suppresses most logs
    chrome_options.add_argument("--log-level=3")  # 0=INFO, 1=WARNING, 2=ERROR, 3=FATAL

    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        return None


def extract_data_via_html_analysis(driver, data_type):
    """Extract data using the exact HTML structure found in CodinGame."""
    # Use the exact selectors from the HTML structure you identified
    if data_type == "input":
        selector = ".testcase-content-texts .testcase-text.testcase-in"
    elif data_type == "output":
        selector = ".testcase-content-texts .testcase-text.testcase-out"

    element = driver.find_element(By.CSS_SELECTOR, selector)
    text = element.text.strip()

    if text and len(text) > 0:
        print(f"Found {data_type}: {len(text)} chars")
        return text


def extract_real_testcases(url):
    """Extract real testcases using Selenium."""
    driver = setup_selenium_driver()

    # print(f"Loading page: {url}")
    driver.get(url)

    # Wait for page to load
    wait = WebDriverWait(driver, 20)
    time.sleep(1)

    # Step 1: Click the "Show testcases" button and find all test cases
    testcases_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.showtestcases-button")))
    driver.execute_script("arguments[0].click();", testcases_button)
    time.sleep(1)
    testcase_headers = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".testcase-header")))
    print(f"Found {len(testcase_headers)} testcase headers")

    # Step 2: Click on each testcase and extract content
    test_inputs = {}
    test_outputs = {}

    for index, header in enumerate(testcase_headers):
        test_number = index + 1

        # Click on the testcase header
        driver.execute_script("arguments[0].click();", header)
        time.sleep(1)  # Give more time for content to load

        # Extract input and ouput using exact selector
        input_data = extract_data_via_html_analysis(driver, "input")
        output_data = extract_data_via_html_analysis(driver, "output")

        # Store the extracted data
        test_inputs[test_number] = input_data
        test_outputs[test_number] = output_data

    driver.quit()
    return test_inputs, test_outputs


def save_testcases_as_object(test_inputs, test_outputs):
    """Save testcases to a Python file."""
    content = f"""TEST_INPUTS = {repr(test_inputs)}
TEST_OUTPUTS = {repr(test_outputs)}"""

    filename = URLNAME + "-testcases.py"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return filename


def save_testcases_as_txt(test_inputs, test_outputs):
    """Save testcases to a text file."""
    content = ""
    for key in test_inputs:
        content += f"=== Input {key} ===\n{test_inputs[key]}\n\n"
        content += f"=== Output {key} ===\n{test_outputs[key]}\n\n"

    filename = URLNAME + "-testcases.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return filename


def create_template_copy():
    """Create a new script file from the template."""
    import os
    import shutil

    target_filename = URLNAME + ".py"

    # Only create if it doesn't exist to avoid overwriting your work
    if not os.path.exists(target_filename):
        if os.path.exists("_template.py"):
            shutil.copy("_template.py", target_filename)
            print(f"📄 Created new puzzle file: {target_filename}")
        else:
            print("⚠️ Warning: _template.py not found!")
    else:
        print(f"ℹ️ Puzzle file {target_filename} already exists, skipping copy.")


# ************************************************************

test_inputs, test_outputs = extract_real_testcases(URL)
print(f"\n✅ SUCCESS! Extracted {len(test_inputs)} testcases")

# Save to file
# filename = save_testcases_as_object(test_inputs, test_outputs)
filename = save_testcases_as_txt(test_inputs, test_outputs)
create_template_copy()

print(f"\n💾 Testcases saved to: {filename}")
