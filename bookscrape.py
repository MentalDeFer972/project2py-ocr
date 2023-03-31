import requests

from bs4 import BeautifulSoup
import csv
import pandas as pd

url = "https://books.toscrape.com/"
one_product_url = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
url_list = []
url_for_unique_categorie = []
url_by_categories = []
data = ["product_page_url","title","category","universal_product_code","price_including_tax","price_excluding_tax","number_available","product_description","image_url","review_rating"]
data_list = []

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
category_side = soup.findAll('ul', 'nav nav-list')
article = soup.findAll('article', 'product_pod')


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
        image = soup2.findAll("img")[0]
        review_rating = soup2.findAll("td")[6]
        image_url = url + image['src'].strip('../')

        data_list.append(product_page_url)
        data_list.append(title.text)
        data_list.append(category.text)
        data_list.append(universal_product_code.text)
        data_list.append(price_including_tax.text)
        data_list.append(price_excluding_tax.text)
        data_list.append(number_available.text)
        data_list.append(product_description.text)
        data_list.append(image_url)
        data_list.append(review_rating.text)

"""Etape 2"""
with open('url.csv',"w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(data)
    display_book(one_product_url)
    writer.writerow(data_list)
    data_list.clear()

"""Etape 3"""

with open('url_for_one_categories.csv',"w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(data)

    tab_for_book("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")

    for url_required in url_for_unique_categorie:
        display_book(url_required)
        writer.writerow(data_list)
        data_list.clear()

"""Etape 4"""
def get_link_category():
    for cat in category_side:
        get_li = cat.findAll('li')
        for li in get_li:
            get_a = li.findAll('a')
            for a in get_a:
                link = url + a['href']
                with open(a.text.strip()+'.csv', "w", encoding="utf-8") as f:
                    response_for_category = requests.get(link)
                    soup_for_category = BeautifulSoup(response_for_category.text, "html.parser")
                    s_link = soup_for_category.findAll('div', 'image_container')
                    writer = csv.writer(f)
                    writer.writerow(data)
                    for s in s_link:
                        link_s = s.findAll('a')
                        for l in link_s:
                            url_required = url + 'catalogue/' + l['href'].strip('../')
                            display_book(url_required)
                            writer.writerow(data_list)
                            data_list.clear()
get_link_category()




