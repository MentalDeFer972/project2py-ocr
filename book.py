import os
import re
from urllib.parse import urljoin, quote

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

scrape_name_dir = "ScrapeData"


#Extraire les information du livre.
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
    review_rating = soup.find('p',"star-rating").get("class")[1]
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
    data_list.append(rating(review_rating))

#Cette fonction convertir la donnée relatives aux notes d'avis en valeur chiffrée.
def rating(str):
    match str:
        case "One":
            return "1 sur 5"
        case "Two":
            return "2 sur 5"
        case "Three":
            return "3 sur 5"
        case "Four":
            return "4 sur 5"
        case "Five":
            return "5 sur 5"


#Extraire à partir du lien du livre,le chemin jpg image du livre.
def extract_img(book_link):
    response = requests.get(book_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    image = soup.findAll("img")[0]
    image_url = base_url + image['src'].strip('../')
    return image_url

#Extraire à partir du lien du livre,le titre du livre.
def extract_title(book_link):
    response = requests.get(book_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find("h1")
    return title.text

#Extraire toutes les liens relatifs aux catégories du livre.
def link_category_function():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.findAll('div', 'side_categories')
    for d in divs:
        ahref = d.findAll('a')
        for a in ahref:
            link_category.append(base_url + a['href'])


#Extraire toutes les liens relatifs aux livres à partir du lien relatifs à la catégorie du livre.
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

#Permet la pagination du lien relatif à la catégorie du livre(Dans une catégorie,il y plusieurs pages)
def pagination_page(link):
    previous_url = link
    while True:
        response = requests.get(previous_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        footer = soup.select_one('li.current')
        if footer:
            print(footer.text.strip())
            print(previous_url)
            link_pagination.append(previous_url)
            next_page = soup.select_one('li.next>a')
            if next_page:
                next_url = next_page.get('href')
                previous_url = urljoin(previous_url, next_url)
            else:
                break
        else:
            print(previous_url)
            link_pagination.append(previous_url)
            break

#Retourne la catégorie du livre
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

#Permet de créer le dossier principal du projet,de regrouper les données du scraping.
def make_dir(name):
    os.mkdir(name)

#Permet de scraper un seul livre et de l'enregistrer au format csv(Etape 2)
def scrape_a_book(link_book):
    with open(scrape_name_dir+"/"+"BookSelected.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f,delimiter=";")
        extract_book(link_book)
        writer.writerow(data)
        writer.writerow(data_list)
        data_list.clear()

#Permet de scraper tous les livres d'une seule catégorie(Etape 3)
def scrape_books_for_one_category(link_category):
        pagination_page(link_category)
        for link_p in link_pagination:
           link_books_function(link_p)
           with open(scrape_name_dir+"/"+"CategorySelected.csv", "w", encoding="utf-8") as f:
                writer = csv.writer(f,delimiter=";")
                writer.writerow(data)
                for link_b in link_books:
                   extract_book(link_b)
                   writer.writerow(data_list)
                   data_list.clear()
                link_books.clear()
        link_pagination.clear()

#Permet de scraper tous les livres de toutes les catégories,au format csv.(Etape 4)
#Permet d'extraire les images des livres(format jpg),regroupées par catégories(Etape 5)
def scrape_books_and_img_for_all_category():
    link_category_function()

    for link_c in link_category:
        pagination_page(link_c)
        category_name = type_category(link_c)

        with open(scrape_name_dir + "/" + category_name + ".csv", "w", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(data)
            os.mkdir(scrape_name_dir + "/" + category_name)
            for link_p in link_pagination:
                link_books_function(link_p)
            for link_b in link_books:
                extract_book(link_b)
                img = extract_img(link_b)
                response_img = requests.get(img)
                title = extract_title(link_b)
                print(title)
                file = open(scrape_name_dir + "/" + category_name + "/" + re.sub(r'[^\w_. éè-]', '_', title) + ".jpg", "wb")
                file.write(response_img.content)
                writer.writerow(data_list)
                data_list.clear()
                file.close()
            link_books.clear()
            link_pagination.clear()
    link_category.clear()

def execute():
    make_dir(scrape_name_dir)
    scrape_a_book("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    scrape_books_for_one_category("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")
    scrape_books_and_img_for_all_category()

execute()