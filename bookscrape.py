import requests

from bs4 import BeautifulSoup
import pandas as pd


url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)

books = []

if response.ok:
    soup = BeautifulSoup(response.text, "html.parser")
    #product_page_url = soup.find("h3")
    title = soup.find("h1")
    category = soup.findAll("a")[3]
    universal_product_code = soup.findAll("td")[0]
    price_including_tax = soup.findAll("td")[2]
    price_excluding_tax = soup.findAll("td")[3]
    number_available = soup.findAll("td")[4]
    product_description = soup.findAll("p")[3]
    image_url = soup.findAll("img")[0]

    #print(product_page_url.text)
    print(universal_product_code.text)
    print(title.text)
    print(price_including_tax.text)
    print(price_excluding_tax.text)
    print(product_description.text)
    print(category.text)
    print(image_url)















