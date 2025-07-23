from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
import re
from recommender_app.scraping.mappings_key import KEY_MAPPING
from recommender_app.utils.parsing_utils import extract_float, extract_int
from recommender_app import create_app
from recommender_app.services.motorcycle_service import save_bike_data_on_db
from concurrent.futures import ThreadPoolExecutor, as_completed


url_base = "https://www.moto.it/social/recensioni"

def scrape_with_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url_base)
        brand_elements = page.query_selector_all("a.readall")
        brands = []

        for brand in brand_elements:
            href = brand.get_attribute("href")
            title = brand.get_attribute("title")

            if href:
                brand_name = brand.text_content().strip()
                if not brand_name and title:
                    brand_name = title.strip().split(" ")[-1]
                elif not brand_name:
                    brand_name = "Unknown Brand"
                brand_url = href.replace("../", url_base)
                brands.append({
                    "name": brand_name,
                    "url": brand_url
                })
            
            print(f"Brand found: {brand_name} - URL: {brand_url}")
        browser.close()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_brand, brand) for brand in brands]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Errore nel thread: {e}")


def process_brand(brand: dict):
    print(f"Processing brand: {brand['name']} - URL: {brand['url']}")


app = create_app()    

if __name__ == "__main__":
    with app.app_context():
        scrape_with_playwright()
