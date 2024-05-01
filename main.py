from handler import ProductScraper
import asyncio


async def main():
    base_url = 'https://www.nay.sk/zastrihavace'
    scraper = ProductScraper(base_url)

    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())
