from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

url = 'https://quotes.toscrape.com/scroll'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.get(url)

def scroll_to_bottom():
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(1)


old_height = 0
new_height = driver.execute_script('return document.body.scrollHeight')

while new_height != old_height:
    scroll_to_bottom()
    old_height = new_height
    new_height = driver.execute_script('return document.body.scrollHeight')

quotes = driver.find_elements(By.CSS_SELECTOR, 'div.quote')
print(len(quotes))

