import os
import subprocess
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def start_streamlit():
    """
    Start the Streamlit app as a subprocess.
    Stops automatically when tests complete.
    """
    process = subprocess.Popen(
        ["streamlit", "run", "app/solar_dashboard.py", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Give Streamlit time to start
    time.sleep(10)
    yield
    process.terminate()

def test_dashboard_loads(start_streamlit):
    """
    Launch Chrome, open the dashboard, and verify page title.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")   # run without opening a window
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options)

    try:
        driver.get("http://localhost:8501")
        time.sleep(5)  # wait for Streamlit to render

        # Check if page title contains our app title
        assert "Smart Solar Allocator" in driver.title or "Streamlit" in driver.title

        # Optional: Check for presence of upload button
        upload_elem = driver.find_element(By.XPATH, "//input[@type='file']")
        assert upload_elem is not None, "Upload element not found"

    finally:
        driver.quit()

