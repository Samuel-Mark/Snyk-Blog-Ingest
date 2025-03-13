from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

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