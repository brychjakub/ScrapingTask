from handler import ProductScraper
import asyncio


async def main():
    scraper = ProductScraper()

    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())
