from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
import re
from recommender_app.scraping.mappings_key import KEY_MAPPING
from recommender_app.utils.parsing_utils import extract_float, extract_int
from recommender_app import create_app
from recommender_app.services.motorcycle_service import save_bike_data_on_db
from concurrent.futures import ThreadPoolExecutor, as_completed


url_base = "https://www.moto.it"

def scrape_with_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url_base + "/listino/")
        brand_elements = page.query_selector_all("span.plist-bcard-content")
        brands = []

        for brand in brand_elements:
            try:
                brand_link = brand.query_selector("a").get_attribute("href") if brand.query_selector("a") else None
                brand_name = brand.query_selector("h2").text_content().strip() if brand.query_selector("h2") else "Unknown Brand"

                if not brand_link:
                    break

                if brand_link:
                    brands.append({
                        "name": brand_name,
                        "url": brand_link
                    })

                print(f"Brand found: {brand_name} - URL: {brand_link}")
            except Exception as e:
                print(f"Error processing brand element: {e}")
        
        browser.close()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_brand, brand) for brand in brands]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Errore nel thread: {e}")


def process_brand(brand: dict):
    from recommender_app import create_app
    app = create_app()
    with app.app_context():  # <-- IMPORTANTE
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url_base + brand['url'])

                model_versions = extract_brand_infos(page, brand, brand['url'])
                
                if not model_versions:
                    print(f"No models found for brand: {brand['name']}")
                    return

                for model in model_versions:
                    save_bike_data_on_db(model)

                browser.close()
            except Exception as e:
                print(f"Error processing brand {brand['name']}: {e}")


def extract_brand_infos(page: Page, brand: dict):
    print(f"Processing brand: {brand['name']} - URL: {brand['url']}")


    


app = create_app()    

if __name__ == "__main__":
    with app.app_context():
        scrape_with_playwright()
