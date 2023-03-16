import requests

from bs4 import BeautifulSoup


url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)


if response.ok:
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1")
    td = soup.findAll("td")
    p = soup.findAll("p")
    a = soup.findAll("a")

    category = a[3]
    universal_product_code = td[0]
    price_including_tax = td[2]
    price_excluding_tax = td[3]
    number_available = td[4]
    product_description = p[3]
    image_url = soup.findAll("img")

    print(universal_product_code.text)
    print(title.text)
    print(price_including_tax.text)
    print(price_excluding_tax.text)
    print(product_description.text)
    print(category.text)










