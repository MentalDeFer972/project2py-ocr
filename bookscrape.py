from _csv import writer

import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)

with open('url.csv', 'w') as outf :
    outf.write('informations')
    if response.ok:
            beatifulsoup = BeautifulSoup(response.text,'html.parser')
            product = beatifulsoup.findAll('article')
            for pro in product:
                print(pro.text)
