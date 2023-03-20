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
    response2 = requests.get(urll)
    soup2 = BeautifulSoup(response2.text, 'html.parser')

    product_page_url = urll
    title = soup2.find("h1")
    category = soup2.findAll("a")[3]
    universal_product_code = soup2.findAll("td")[0]
    price_including_tax = soup2.findAll("td")[2]
    price_excluding_tax = soup2.findAll("td")[3]
    number_available = soup2.findAll("td")[5]
    product_description = soup2.findAll("p")[3]
    image_url = soup2.findAll("img")[0]
    review_rating = soup2.findAll("td")[6]

    print(product_page_url)
    print(universal_product_code.text)
    print(title.text)
    print(price_including_tax.text)
    print(price_excluding_tax.text)
    print(product_description.text)
    print(category.text)
    print(number_available.text)
    print(review_rating.text)
    print(image_url['src'])

























