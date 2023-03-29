import requests

from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com/"
one_product_url = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
url_list = []
url_for_unique_categorie = []
url_by_categories = []

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
category_side = soup.findAll('ul', 'nav nav-list')
article = soup.findAll('article', 'product_pod')

"""Etape 4"""
def get_link_category():
    for cat in category_side:
        get_li = cat.findAll('li')
        for li in get_li:
            get_a = li.findAll('a')
            for a in get_a:
                link = url + a['href']
                print(a.text.strip())
                response_for_category = requests.get(link)
                soup_for_category = BeautifulSoup(response_for_category.text, "html.parser")
                s_link = soup_for_category.findAll('div', 'image_container')
                for s in s_link:
                    link_s = s.findAll('a')
                    for l in link_s:
                        print(url + 'catalogue/' + l['href'].strip('../'))


def tab_catalogue():
    for a in article:
        get_div = a.findAll('div')
        for div in get_div:
            get_a = div.findAll('a')
            for a in get_a:
                url_list.append(url + a['href'])

def tab_for_book(url_link):
    response = requests.get(url_link)
    soup = BeautifulSoup(response.text, "html.parser")
    category_side = soup.findAll('ul', 'nav nav-list')
    article = soup.findAll('article', 'product_pod')
    for a in article:
        s_link = a.findAll('div', 'image_container')
        for s in s_link:
            link_s = s.findAll('a')
            for l in link_s:
                url_for_unique_categorie.append(url + 'catalogue/' + l['href'].strip('../'))


def display_book(book_link):
        response2 = requests.get(book_link)
        soup2 = BeautifulSoup(response2.text, 'html.parser')

        product_page_url = book_link
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


"""Etape 2"""
display_book(one_product_url)

"""Etape 3"""
tab_for_book("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")
for url in url_for_unique_categorie:
    display_book(url)

"""Etape 4"""

