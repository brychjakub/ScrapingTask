import requests
from bs4 import BeautifulSoup

url = 'https://www.nay.sk/zastrihavace'

session = requests.Session()

response = session.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    product_titles = soup.find_all('h3', class_='product-box__name')
    print("titles")

    for title in product_titles:
        print(title.text.strip())
    
    product_prices = soup.find_all('strong', class_='typo-complex-16')
    print("prices")
    for title in product_prices:
        print(title.text.strip())

    product_prices_before_discount = soup.find_all('span', class_= "d-block text-gray-600 typo-complex-12")
    print("product_prices_before_discount")

    for title in product_prices_before_discount:
            if title.find('del'):
                 
                print(title.text.strip())

    print("success")

else:
    print("Failed to retrieve the web page")
