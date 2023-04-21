import requests

from bs4 import BeautifulSoup
import csv
import os

#Liens URL pour scraper les informations.
base_url = "https://books.toscrape.com/"
one_product_url = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"

#Créations des tableaux pour créer le fichier CSV ainsi que la liste des liens URL et liens images.
data = ["product_page_url", "title", "category", "universal_product_code", "price_including_tax", "price_excluding_tax",
        "number_available", "product_description", "image_url", "review_rating"]
data_list = []
img_list = []

#Récupérer le code source du lien HTML et l'extraire.
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")
category_side = soup.findAll('ul', 'nav nav-list')
articles = soup.findAll('article', 'product_pod')



#Extraire les URL de la page Web principale.
def get_url_list():
    url_list = []
    for article in articles:
        div = article.findAll('div')
        for d in div:
            ahref = d.findAll('a')
            for a in ahref:
                url_list.append(base_url + a['href'])
    return url_list

#Extraire les URL de la page Web,par catégories.
def get_url_for_unique_categories(url_link):
    url_for_unique_categories = []
    response = requests.get(url_link)
    soup = BeautifulSoup(response.text, "html.parser")
    category_side = soup.findAll('ul', 'nav nav-list')
    articles = soup.findAll('article', 'product_pod')
    for article in articles:
        image_container = article.findAll('div', 'image_container')
        for image in image_container:
            link_s = image.findAll('a')
            for l in link_s:
                url_for_unique_categories.append(base_url + 'catalogue/' + l['href'].strip('../'))
    return url_for_unique_categories


#Afficher les informations du livre sélectionné à partir de l'URL choisie.
def display_book(book_link):
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

#Afficher uniquement le titre du livre sélectionné à partir de l'URL choisie.
def extract_title(book_link):
    response = requests.get(book_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find("h1")
    return title.text

#Afficher les URL des images des livres sélectionné à partir de l'URL de la catégorie choisie.
def extract_img(book_link):
    response = requests.get(book_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    image = soup.findAll("img")[0]
    image_url = base_url + image['src'].strip('../')
    img_list.append(image_url)


"""Etape 2"""
#Permet d'extraire les données de la page sélectionnée au format de fichier csv.

def get_extract_for_one_product():
    with open('url.csv', "w", encoding="utf-8") as f:
        writer = csv.writer(f,delimiter=";")
        writer.writerow(data)
        display_book(one_product_url)
        writer.writerow(data_list)
        data_list.clear()


"""Etape 3"""
#Extraire les données de tous les livres de la catégories sélectionnés.


def get_url_for_one_categories():
    with open('url_for_one_categories.csv', "w", encoding="utf-8") as f:
        writer = csv.writer(f,delimiter=";")
        writer.writerow(data)

        for url_required in get_url_for_unique_categories(
                "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"):
            display_book(url_required)
            writer.writerow(data_list)
            data_list.clear()

"""Etape 4 et 5"""
#Extraire les données de tous les livres de toutes les catégories,et de générer un fichier csv pour chaque catégorie.
#Extraire et enregistrer les images par catégories.

def get_all_img_and_books_by_category():
    for cat in category_side:
        get_li = cat.findAll('li')
        for li in get_li:
            get_a = li.findAll('a')
            for a in get_a:
                link = base_url + a['href']
                with open(a.text.strip() + '.csv', "w", encoding="utf-8") as f:
                    response_for_category = requests.get(link)
                    soup_for_category = BeautifulSoup(response_for_category.text, "html.parser")
                    s_link = soup_for_category.findAll('div', 'image_container')
                    writer = csv.writer(f,delimiter=";")
                    writer.writerow(data)
                    os.mkdir(a.text.strip())
                    for s in s_link:
                        link_s = s.findAll('a')
                        for l in link_s:
                            url_required = base_url + 'catalogue/' + l['href'].strip('../')
                            display_book(url_required)
                            writer.writerow(data_list)
                            extract_img(url_required)
                            data_list.clear()
                            for img in img_list:
                                response_img = requests.get(img)
                                title = extract_title(url_required)
                                file = open(a.text.strip()+"/"+title+".jpg","wb")
                                file.write(response_img.content)
                                file.close()


#Exécutions des scripts.

get_extract_for_one_product()
get_url_for_one_categories()
get_all_img_and_books_by_category()

