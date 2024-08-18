import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

# https://www.ebay.com/sch/i.html?_dcat=177&_fsrp=1&rt=nc&_from=R40&RAM%2520Size=32%2520GB&_nkw=laptop&_sacat=0&SSD%2520Capacity=1%2520TB&_pgn=1

laptop_dict = {
    'name': [],
    'price': [],
    'shipping': [],
    'link': []
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

page_no = 1
while True:
    print('*********************************')
    print(f'Page no --> {page_no}')
    print('*********************************')

    url = f'https://www.ebay.com/sch/i.html?_dcat=177&_fsrp=1&rt=nc&_from=R40&RAM%2520Size=32%2520GB&_nkw=laptop&_sacat=0&SSD%2520Capacity=1%2520TB&_pgn={page_no}'
    response = requests.get(url, headers=headers)
    print(response.status_code)

    if response.status_code != 200:
        continue

    page_html = response.text
    soup = BeautifulSoup(page_html, 'html.parser')
    print(soup.title)
    laptops = soup.find_all('div', class_='s-item__info')
    for laptop in laptops[2:]:
        if laptop.find('span', attrs={'role': 'heading'}) is not None:
            name = laptop.find('span', attrs={'role': 'heading'}).text
            laptop_dict['name'].append(name)
            print(name)
        else:
            name = 'No info'
            laptop_dict['name'].append(name)
            print(name)
        if laptop.find('span', class_='s-item__price') is not None:
            price = laptop.find('span', class_='s-item__price').text
            laptop_dict['price'].append(price)
            print(price)
        else:
            price = 'No info'
            laptop_dict['price'].append(price)
            print(price)

        if laptop.find('span', class_='s-item__logisticsCost') is not None:
            shipping = laptop.find('span', class_='s-item__logisticsCost').text
            laptop_dict['shipping'].append(shipping)
            print(shipping)
        else:
            shipping = 'No info'
            laptop_dict['shipping'].append(shipping)
            print(shipping)

        if laptop.find('a', class_='s-item__link') is not None:
            link = laptop.find('a', class_='s-item__link')['href']
            laptop_dict['link'].append(link)
            print(link)
        else:
            link = 'No info'
            laptop_dict['link'].append(link)
            print(link)

    next_as_button = soup.find('button', class_='pagination__next')
    if next_as_button is not None:
        break

    page_no += 1

    print('\n\n')

df = pd.DataFrame(laptop_dict)
df.to_excel('laptops.xlsx')





