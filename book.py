import os
from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup
import csv

link_category = []
link_pagination = []
link_books = []

final_link = ""
base_url = "https://books.toscrape.com/"

data = ["product_page_url", "title", "category", "universal_product_code", "price_including_tax", "price_excluding_tax",
        "number_available", "product_description", "image_url", "review_rating"]
data_list = []

def extract_book(book_link):
    response = requests.get(book_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_page_url = book_link
    title = soup.find("h1")
    category = soup.findAll("a")[3]
    universal_product_code = soup.findAll("td")[0]
    price_including_tax = soup.findAll("td")[2]
    price_excluding_tax = soup.findAll("td")[3]
    number_available = soup.findAll("td")[5]
    product_description = soup.findAll("p")[3]
    image = soup.findAll("img")[0]
    review_rating = soup.findAll("td")[6]
    image_url = base_url + image['src'].strip('../')

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

def extract_img(book_link):
    response = requests.get(book_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    image = soup.findAll("img")[0]
    image_url = base_url + image['src'].strip('../')
    return image_url

def extract_title(book_link):
    response = requests.get(book_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find("h1")
    return title.text

def link_category_function():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.findAll('div', 'side_categories')
    for d in divs:
        ahref = d.findAll('a')
        for a in ahref:
            link_category.append(base_url + a['href'])


def link_books_function(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.findAll('article', 'product_pod')
    for art in articles:
        divs = art.findAll('div', 'image_container')
        for div in divs:
            ahref = div.findAll('a')
            for href in ahref:
                link_books.append(base_url + 'catalogue/' + href['href'].strip('../'))


def pagination_page(link):
    previous_url = link
    while True:
        response = requests.get(previous_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        footer = soup.select_one('li.current')
        print(footer.text.strip())
        print(previous_url)
        link_pagination.append(previous_url)
        next_page = soup.select_one('li.next>a')
        if next_page:
            next_url = next_page.get('href')
            previous_url = urljoin(previous_url, next_url)
        else:
            break

def type_category(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.findAll("div","container-fluid page")
    for div in divs:
        uls = div.findAll("ul","breadcrumb")
        for ul in uls:
            li = ul.find("li","active")
            category = li.text
            return category

def scrape_a_book(link_book):
    with open("book_selected.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f,delimiter=";")
        extract_book(link_book)
        writer.writerow(data)
        writer.writerow(data_list)
        data_list.clear()

def scrape_books_for_one_category(link_category):
        pagination_page(link_category)
        category_name = type_category(link_category)
        for link_p in link_pagination:
           link_books_function(link_p)
           with open(category_name+".csv", "w", encoding="utf-8") as f:
                writer = csv.writer(f,delimiter=";")
                writer.writerow(data)
                for link_b in link_books:
                   extract_book(link_b)
                   writer.writerow(data_list)
                   data_list.clear()

def scrape_books_and_img_for_all_category():
    link_category_function()

    for link_c in link_category:
        pagination_page(link_c)
        category_name = type_category(link_c)
        for link_p in link_pagination:
            link_books_function(link_p)
            with open(category_name + ".csv", "w", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(data)
                os.mkdir(category_name)
                for link_b in link_books:
                    extract_book(link_b)
                    extract_img(link_b)
                    response_img = requests.get(link_b)
                    title = extract_title(link_b)
                    file = open(category_name + "/" + title + ".jpg", "wb")
                    file.write(response_img.content)
                    writer.writerow(data_list)
                    data_list.clear()
                    file.close()


scrape_a_book("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
scrape_books_for_one_category("https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html")
scrape_books_and_img_for_all_category()