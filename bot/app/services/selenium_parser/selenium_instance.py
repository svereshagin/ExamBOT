from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")  # Disable sandboxing
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
