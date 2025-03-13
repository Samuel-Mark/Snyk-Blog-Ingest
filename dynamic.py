from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_dynamic(url):
    # Set up Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # Open the webpage
    driver.get(url)
    
    # Click the "Show previous updates" link until all articles are loaded
    while True:
        try:
            show_more_link = driver.find_element(By.CSS_SELECTOR, 'div.pagination a')
            show_more_link.click()
            time.sleep(2)  # Wait for content to load
        except:
            break  # Exit loop if link is not found
    
    # Get the page source and close the browser
    html_content = driver.page_source
    driver.quit()
    
    return html_content