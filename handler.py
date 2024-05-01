import requests
from bs4 import BeautifulSoup
import csv
import json
from product import Product
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import aiohttp
import asyncio




class ProductScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.products = []

    
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
            print("Found product sections:", len(product_sections))  # Check how many sections are found
            for section in product_sections:
                title_tag = section.find('h3', class_='product-box__name')
                title = title_tag.text.strip() if title_tag else None

                price_tag = section.find('strong', class_='typo-complex-16')
                price = price_tag.text.strip() if price_tag else None

                price_before_discount_tag = section.find(
                    'span', 
                    class_='d-block text-gray-600 typo-complex-12'
                    )
                price_before_discount = price_before_discount_tag.find('del').text.strip() if price_before_discount_tag and price_before_discount_tag.find('del') else None
                
                if title and price:
                    product = Product(title, price, price_before_discount)
                    self.products.append(product)
                    print("Scraped product:", product)


    def save_to_csv(self, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price', 'Price Before Discount'])
            for product in self.products:
                writer.writerow([product.title, product.price, product.price_before_discount])

    def save_to_json(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([product.__dict__ for product in self.products], file, indent=4)

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

        # Save results to files
        self.save_to_csv('products.csv')
        self.save_to_json('products.json')
