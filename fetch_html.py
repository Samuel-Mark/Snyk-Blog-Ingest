import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1A. Static fetching of HTML Content, loads the page and then takes all content loaded.
def fetch_static(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve content: {response.status_code}")
        return None

# 1B. Dynamic fetching of HTML Content, loads the page repeatedly presses the pages 'Show previous updates'
# button to load all posts.
def fetch_dynamic(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    driver.get(url)
    
    while True:
        try:
            show_more_link = driver.find_element(By.CSS_SELECTOR, 'div.pagination a')
            show_more_link.click()
            time.sleep(2)
        except:
            break
    
    html_content = driver.page_source
    driver.quit()
    
    return html_content

# 1C. Performs a HTML fetch based to a URL based on an input.
def fetch_html_content(url, mode):
    if mode == 'static':
        return fetch_static(url)
    elif mode == 'dynamic':
        return fetch_dynamic(url)
    else:
        print("Invalid HTML collection mode. Use 'static' or 'dynamic'.")
        return None