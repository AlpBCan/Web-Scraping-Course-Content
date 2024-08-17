'''
    It's your turn!!!

    You will find the directors who won 'Best Director' award in Drama genre
and save their height :)

    Start from this link:
    https://www.imdb.com/search/title/?explore=genres&title_type=feature

    Let's start, you are ready!
'''



# Create a dictionary to save the data. Keys: 'name', 'height_inch', 'height_cm'
directors_dict = {'name': [], 'height_inch': [], 'height_cm': []}


# Import necessary libraries, you can add some others when you need them later on.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
import openpyxl


# Define the options, create the driver, get to the main page
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
actions = ActionChains(driver)
driver.get('https://www.imdb.com/search/title/?explore=genres&title_type=feature')


# Check for cookies and accept if appears(wait a few seconds before checking)
try:
    accept_button = driver.find_element(By.XPATH, '//button[text()="Accept"]')
    accept_button.click()
except:
    pass


# Select 'Drama' genre and select 'Best Director-Winning' from filters

drama_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-Drama"]')
actions.move_to_element(drama_button).perform()
drama_button.click()

sleep(2)

awards_button = driver.find_element(By.XPATH, '//div[text()="Awards & recognition"]')
actions.move_to_element(awards_button).perform()
awards_button.click()

sleep(2)

director_winning_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-best-director-winning"]')
actions.move_to_element(director_winning_button).perform()
director_winning_button.click()




# Create a loop to load all movies by pressing 'more' button at the bottom (The same with earlier)
while True:
    sleep(2)
    more_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.ipc-see-more__text')
    if len(more_buttons) != 0:
        more_button = more_buttons[0]
        actions.move_to_element(more_button).perform()
        more_button.click()
    else:
        break


# Take a list of information buttons(use svg tags) at the right side of all the movies
i_buttons = driver.find_elements(By.CSS_SELECTOR, 'svg.ipc-icon--info')


# Create a loop to press info buttons one by one and take the links of the directors from them into a list
director_links = []
for i_button in i_buttons:
    actions.move_to_element(i_button).perform()
    i_button.click()
    sleep(0.5)
    a_tag = driver.find_element(By.CSS_SELECTOR, 'a.ktChvQ')
    link = a_tag.get_attribute('href')
    director_links.append(link)
    close_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close Prompt"]')
    actions.move_to_element(close_button).perform()
    close_button.click()
    sleep(0.5)



# Visit every link using a loop and save name and height of director to the dictionary you defined at the beginning

for link in director_links:
    driver.get(link)

    try:
        name = driver.find_element(By.CSS_SELECTOR, 'h1[data-testid="hero__pageTitle"] span[data-testid="hero__primary-text"]').text
    except:
        name = 'No info'

    try:
        raw_height = driver.find_element(By.XPATH, '//span[text()="Height"]/following-sibling::div[1]/ul/li/span').text
        # 5′ 11¼″ (1.81 m)
        height_inch = raw_height.split('(')[0].strip()
        height_cm = raw_height.split('(')[1][:-1]

    except:
        height_inch = 'No info'
        height_cm = 'No info'

    directors_dict['name'].append(name)
    print(name)
    directors_dict['height_inch'].append(height_inch)
    print(height_inch)
    directors_dict['height_cm'].append(height_cm)
    print(height_cm)


# Using Pandas save the data into Excel

df = pd.DataFrame(directors_dict)
df.to_excel('height.xlsx')


