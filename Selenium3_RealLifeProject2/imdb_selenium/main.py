from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
import openpyxl


movie_dict = {
    'name': [],
    'year': [],
    'duration': [],
    'stars': [],
    'votes': [],
    'metascore': [],
    'description': []
}

def accept_cookie(the_driver):
    try:
        accept_cookies = the_driver.find_element(By.XPATH, '//button[text()="Accept"]')
        accept_cookies.click()
    except:
        pass


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
actions = ActionChains(driver)
driver.implicitly_wait(1)

driver.get('https://www.imdb.com/')

sleep(2)

accept_cookie(driver)

menu_button = driver.find_element(By.ID, 'imdbHeader-navDrawerOpen')
menu_button.click()

sleep(2)

by_genre_button = driver.find_element(By.XPATH, '//span[text()="Browse Movies by Genre"]')
by_genre_button.click()

accept_cookie(driver)
sleep(2)

comedy_links = driver.find_elements(By.XPATH, '//span[text()="Comedy"]')

comedy_movies_button = comedy_links[1]
driver.execute_script('arguments[0].click()', comedy_movies_button)

sleep(2)

awards_button = driver.find_element(By.XPATH, '//div[text()="Awards & recognition"]')
actions.move_to_element(awards_button).perform()
awards_button.click()

sleep(2)

oscar_nominated_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-oscar-nominated"]')
actions.move_to_element(oscar_nominated_button).perform()
oscar_nominated_button.click()

while True:
    sleep(2)
    more_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.ipc-see-more__text')
    if len(more_buttons) != 0:
        more_button = more_buttons[0]
        actions.move_to_element(more_button).perform()
        more_button.click()
    else:
        break

movies = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item')

for movie in movies:
    raw_name = movie.find_element(By.CSS_SELECTOR, 'h3.ipc-title__text').text
    # 1. Beverly Hills Cop
    name = ' '.join(raw_name.split(' ')[1:])
    print(name)
    movie_dict['name'].append(name)

    year = movie.find_elements(By.CLASS_NAME, 'dli-title-metadata-item')[0].text
    print(year)
    movie_dict['year'].append(year)

    duration = movie.find_elements(By.CLASS_NAME, 'dli-title-metadata-item')[1].text
    print(duration)
    movie_dict['duration'].append(duration)

    raw_stars = movie.find_element(By.CSS_SELECTOR, 'span[data-testid="ratingGroup--imdb-rating"]').get_attribute('aria-label')
    # IMDb rating: 7.4
    stars = raw_stars.split(' ')[-1]
    print(stars)
    movie_dict['stars'].append(stars)

    # (211K)
    votes = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--voteCount').text.strip()[1:-1]
    print(votes)
    movie_dict['votes'].append(votes)

    try:
        metascore = movie.find_element(By.CLASS_NAME, 'metacritic-score-box').text
        print(metascore)
        movie_dict['metascore'].append(metascore)
    except:
        metascore = 'No info'
        print(metascore)
        movie_dict['metascore'].append(metascore)


    description = movie.find_element(By.CLASS_NAME, 'ipc-html-content-inner-div').text
    print(description)
    movie_dict['description'].append(description)
    print('\n')

df = pd.DataFrame(movie_dict)
df.to_excel('movies.xlsx')







