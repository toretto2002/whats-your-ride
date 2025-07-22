from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
import re
from recommender_app.scraping.mappings_key import KEY_MAPPING
from recommender_app.utils.parsing_utils import extract_float, extract_int
from recommender_app import create_app
from recommender_app.services.motorcycle_service import save_bike_data_on_db
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

url_base = "https://bikez.com/"

def scrape_with_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url_base + "brands/index.php")

        brand_elements = page.query_selector_all("table.zebra tbody tr td a")
        brands = []
        count = 0

        for brand in brand_elements:
            href = brand.get_attribute("href")
            if href:
                brand_name = brand.text_content().strip()
                brand_url = href.replace("../", url_base)
                brands.append({
                    "name": brand_name,
                    "url": brand_url
                })
            
            # count += 1
            # if count >= 5:  # Limita a 5 brand per test
            #     break

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

                model_versions = extract_brand_infos(page, brand, brand['url'])
                
                if not model_versions:
                    print(f"Brand {brand['name']} ha restituito None o errore.")
                    return

                for model in model_versions:
                    try:
                        page.goto(model['url'])
                        page.wait_for_selector("table")
                        specs = parse_specs(page)
                        save_bike_data_on_db(specs)
                    except Exception as e:
                        print(f"Errore nel salvataggio di {model['name']}: {e}")
            finally:
                browser.close()


def extract_brand_infos(page, brand, href):
    page.goto(brand['url'])
    page.wait_for_selector("table")

    model_rows = page.query_selector_all("tr.even")
    model_versions = []
    multi_version_model_urls = []

    for model in model_rows:
        tds = []
        tds = model.query_selector_all("td")
        if tds[0]:
            if tds[0].query_selector("a"):
                        # modello con più versioni
                model_url = tds[1].query_selector("a").get_attribute("href")
                model_url = model_url.replace("..", url_base)

                multi_version_model_urls.append(model_url)
                        
                        # Vai nella pagina del modello per estrarre le versioni
                            
            else:
                        # modello con una sola versione
                model_url = tds[1].query_selector("a").get_attribute("href")
                model_url = model_url.replace("..", url_base)
                model_name = tds[1].text_content().strip()

                        # aggiungi la singola versione alla lista
                if not any(m['url'] == model_url for m in model_versions):
                    model_versions.append({
                                "name": model_name,
                                "url": model_url
                            })

    for url in multi_version_model_urls:
        page.goto(url)
        page.wait_for_selector("a")


        links = page.query_selector_all('a')
        existing_urls = set(m['url'] for m in model_versions)

        for link in links:
            title_span = link.query_selector('span[style*="font-size:18px"] b')
            if not title_span:
                continue

            href = link.get_attribute('href')
            if not href:
                continue

            url = urljoin(url_base, href)
            title = title_span.text_content().strip()

            if url not in existing_urls:
                model_versions.append({
                    "name": title,
                    "url": url
                })
                existing_urls.add(url)


    return model_versions

def model_with_multiple_versions():
    pass


def parse_specs(page: Page) -> dict:

    try:

        rows = page.query_selector_all("table.Grid tr")
        final_data = {}
        data = {}
        diameter_count = 0

        for row in rows:
            tds = row.query_selector_all("td")
            if len(tds) == 2:
                raw_key = tds[0].text_content().strip()
                raw_value = tds[1].text_content().strip()
                    
                if raw_key and raw_value:
                    if raw_key == "Diameter":
                        diameter_count += 1
                        raw_key = "Diameter" + str(diameter_count)
                    data[raw_key] = raw_value

        # print("Raw data extracted: ", data)
        diameter_count = 1


        for raw_key, raw_value in data.items():

            mapped = KEY_MAPPING.get(raw_key)
            if mapped:
                if isinstance(mapped, tuple):
                    db_key, parser_func = mapped
                    try:
                        parsed_value = parser_func(raw_value)
                    except Exception as e:
                        print(f"Failed parsing '{raw_key}' with value '{raw_value}': {e}")
                        parsed_value = None
                else:
                        db_key = mapped
                        parsed_value = raw_value

                final_data[db_key] = parsed_value
                # print(f"Mapped '{raw_key}' to '{db_key}': {parsed_value}")
            else:
                if raw_key not in ["Insurance costs", "Maintenance", "Ask questions", "Related bikes", "Update specs", "Rating"]:
                    print(f"Model with url {page.url} has key '{raw_key}' not in KEY_MAPPING, skipped.")
        
        # Aggiungi l'URL della pagina come chiave
        final_data["source_url"] = page.url
        final_data["brand"] = page.query_selector("h1").text_content().strip().split()[0] if page.query_selector("h1") else "Unknown Brand"
        final_data["full_name"] = final_data.get("brand", "") + " " + final_data.get("name", "")

        return final_data
   
    except Exception as e:
        print(f"Error parsing specs: {e}")
        return {}

app = create_app()    

if __name__ == "__main__":
    with app.app_context():
        scrape_with_playwright()
