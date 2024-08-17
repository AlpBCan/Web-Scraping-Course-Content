from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


url = 'https://quotes.toscrape.com/js-delayed'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(3)
driver.get(url)

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.quote'))
)


sleep(2)
quotes = driver.find_elements(By.CSS_SELECTOR, 'div.quote')
print(len(quotes))

