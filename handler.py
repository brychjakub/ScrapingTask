import requests
from bs4 import BeautifulSoup
import csv
import json
from product import Product
import aiohttp
import re

class ProductScraper:
    def __init__(self):
        self.base_url = 'https://www.nay.sk/zastrihavace'
        self.products = []
        self.section = None

    
    async def fetch_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                assert response.status == 200
                text = await response.text()
                return BeautifulSoup(text, 'html.parser')

    async def scrape_products(self, soup):
        if soup is not None:
            product_sections = soup.find_all(
                'section', 
                class_='product-box product-box--main position-relative bg-white p-3 p-sm-4 typo-complex-12 flex-grow-0 flex-shrink-0'
                )
            for section in product_sections:
                self.section = section
                title = self.getInfo('product-box__name', 'h3' )
                price = self.getInfo('typo-complex-16', 'strong' )
                availability = self.getInfo('complex-link__underline')
                rating = self.getRating()
                number_of_ratings = self.getInfo('text-gray-600')
                
                product_url_tag = section.find('a', class_='product-box__link')
                url = self.base_url + product_url_tag['href'] if product_url_tag else None                                          

                price_before_discount_tag = section.find(
                    'span', 
                    class_='d-block text-gray-600 typo-complex-12'
                    )
                price_before_discount = price_before_discount_tag.find('del').text.strip() if price_before_discount_tag and price_before_discount_tag.find('del') else None
                
                if title and price:
                    product = Product(title, price, price_before_discount, availability, rating, number_of_ratings, url)
                    self.products.append(product)
                    print("Scraped product:", product)


    def getRating(self):

        rating_wordy = self.getInfo('sr-only')
        match = re.search(r'Hodnocení: (\d+\.\d+|\d+) z (\d+)', rating_wordy)

        if match:
            rating = match.group(1)  
            total = match.group(2)  
            formatted_rating = f"{rating}/{total}"
            return formatted_rating
     

    def getUrl(self):
        return self.base_url


    def save_to_csv(self, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price', 'Price Before Discount', 'availability', 'rating', 'number_of_ratings', 'url'])
            for product in self.products:
                writer.writerow([product.title, product.price, product.price_before_discount, product.availability, product.rating, product.number_of_ratings, product.url])


    def save_to_json(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([product.__dict__ for product in self.products], file, indent=4, ensure_ascii=False)


    def getInfo(self, selector, tag = 'span'):
        tag = self.section.find(tag, class_ = selector)
        attribute = tag.text.strip() if tag else None

        return attribute


    async def run(self):
        page_number = 1
        while True:
            current_page_url = f"{self.base_url}?page={page_number}"
            soup = await self.fetch_page(current_page_url)
            if not soup or not soup.find('h3', class_='product-box__name'):
                print("No more products or failed to retrieve the page.")
                break
            await self.scrape_products(soup)

            next_page = soup.find('i', {'class': 'icon-arrow-right ml-1'})
            if next_page:
                page_number += 1
                print(f"Going to page {page_number}")
            else:
                print("Reached the end of the product list.")
                break

        self.save_to_csv('products.csv')
        self.save_to_json('products.json')
