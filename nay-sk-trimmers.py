import requests
from bs4 import BeautifulSoup

class ProductScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def fetch_page(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print("Failed to retrieve the web page")
            return None
        

    def scrape_products(self, soup):
        if soup is not None:
            # Find all product sections
            product_sections = soup.find_all('section', class_='product-box product-box--main position-relative bg-white p-3 p-sm-4 typo-complex-12 flex-grow-0 flex-shrink-0')
            
            for section in product_sections:
                # Extract the product title
                title_tag = section.find('h3', class_='product-box__name')
                if title_tag:
                    title = title_tag.text.strip()
                    print("Title:", title)

                # Extract the product price
                price_tag = section.find('strong', class_='typo-complex-16')
                if price_tag:
                    price = price_tag.text.strip()
                    print("Price:", price)

                # Extract the price before discount
                price_before_discount_tag = section.find('span', class_='d-block text-gray-600 typo-complex-12')
                if price_before_discount_tag and price_before_discount_tag.find('del'):
                    price_before_discount = price_before_discount_tag.text.strip()
                    print("Price Before Discount:", price_before_discount)



    def run(self):
        page_number = 1  # Start with the first page
        while True:
            current_page_url = f"{self.base_url}?page={page_number}"
            soup = self.fetch_page(current_page_url)
            if not soup or soup.find('h3', class_='product-box__name') is None:
                print("No more products or failed to retrieve the page.")
                break
            self.scrape_products(soup)

            # Check if there's a 'next' link available
            next_page = soup.find('i', {'class': 'icon-arrow-right ml-1'})
            if next_page:
                page_number = page_number + 1
                print(f"goint to page {page_number}")
            else:
                print("Reached the end of the product list.")
                break


# Usage
scraper = ProductScraper('https://www.nay.sk/zastrihavace')
scraper.run()
