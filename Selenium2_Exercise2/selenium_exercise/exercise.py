'''
    It's your turn!!!

    You will use Selenium and scrape following data into an Excel file:
        author name
        author birth date
        author birth place

    Follow the instructions, try to do this by yourself. But if you are stuck,
    do not hesitate to take a look at that part of the solution and come back.

    url = https://quotes.toscrape.com/  -->  not the JS version!

'''

# Import necessary libraries, you can add some others when you need them later on.
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import openpyxl



# Create a dictionary to save the data
author_dict = {'name': [], 'birth_date': [], 'birth_place': []}



# Create an empty list to save the links of author pages
author_urls = []



# Define the options, create the driver, get to the main page
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.get('https://quotes.toscrape.com/')



# Login (the same with earlier)
login_button = driver.find_element(By.XPATH, '//a[text()="Login"]')
login_button.click()

username_input = driver.find_element(By.ID, 'username')
username_input.send_keys('myusername')

password_input = driver.find_element(By.ID, 'password')
password_input.send_keys('123456')

login = driver.find_element(By.CSS_SELECTOR, 'input[value="Login"]')
login.click()



# Create a loop to visit every page (this is the same with what we did earlier).
# In this loop find every author's link(from (about) section) and save them to the empy list you created.
while True:
    quotes = driver.find_elements(By.CLASS_NAME, 'quote')
    for quote in quotes:
        author_link = quote.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        author_urls.append(author_link)

    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'li.next a')
        next_button.click()
    except:
        break


# Take the author url list and put it in a set to remove duplicates
author_urls = list(set(author_urls))


# Create another loop with this list and visit every page to get the name, birth date and birth place to the dictionary
for url in author_urls:
    driver.get(url)
    name = driver.find_element(By.CSS_SELECTOR, 'h3.author-title').text
    author_dict['name'].append(name)
    birth_date = driver.find_element(By.CSS_SELECTOR, 'span.author-born-date').text
    author_dict['birth_date'].append(birth_date)
    birth_place = driver.find_element(By.CSS_SELECTOR, 'span.author-born-location').text
    author_dict['birth_place'].append(birth_place)

# Create Pandas dataframe, put dictionary in and convert it to an Excel file
df = pd.DataFrame(author_dict)
df.to_excel('authors.xlsx')