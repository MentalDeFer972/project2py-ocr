import requests

from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com/"
url_list = []
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

category_side = soup.findAll('ul', 'nav nav-list')
article = soup.findAll('article', 'product_pod')

"""for cat in category_side:
    get_li = cat.findAll('li')
    for li in get_li:
        get_a = li.findAll('a')
        for a in get_a:
            print(a['href'])"""


def tab_catalogue():
    for a in article:
        get_div = a.findAll('div')
        for div in get_div:
            get_a = div.findAll('a')
            for a in get_a:
                url_list.append(url+a['href'])

tab_catalogue()

for urll in url_list:
    print(urll)























