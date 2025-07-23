from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
import re
from recommender_app.scraping.mappings_key import KEY_MAPPING
from recommender_app.utils.parsing_utils import extract_float, extract_int
from recommender_app import create_app
from recommender_app.services.motorcycle_service import save_bike_data_on_db
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import html
from pprint import pprint
from recommender_app.scraping.moto_it.mappings_key_moto_it import KEY_MAPPING
import re
from recommender_app.utils.parsing_utils import parse_mm, parse_kg, parse_float, parse_boolean, parse_price, parse_power, parse_torque


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
                break  # Limita a un brand per test
            
            except Exception as e:
                print(f"Error processing brand element: {e}")
        
        browser.close()

        with ThreadPoolExecutor(max_workers=1) as executor:
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

                models = extract_brand_infos(page, brand, browser)

                browser.close()
            except Exception as e:
                print(f"Error processing brand {brand['name']}: {e}")


def extract_brand_infos(page: Page, brand: dict, browser):
    print(f"Processing brand: {brand['name']} - URL: {brand['url']}")
    models = []

    cards_models_in_list = page.query_selector_all("div.plist-pcard")

    if not cards_models_in_list:
        print(f"No models found for brand: {brand['name']}")
        return []
    
    for card in cards_models_in_list:
        try:
            anchor = card.query_selector("a.app-set-model")
            model_name = clean_model_name(anchor.text_content().strip()) if anchor else "Unknown Model"
            versions_page_url = anchor.get_attribute("href") if anchor else None
            version_prizes_to_parse = card.query_selector("div.plist-pcard-price").text_content().strip()

            prices_tuple = extract_price_range(version_prizes_to_parse)

            lower_price = prices_tuple[0]
            upper_price = prices_tuple[1]

            if lower_price is None or upper_price is None:
                print(f"Price extraction failed for model: {model_name}")
                continue

        except Exception as e:
            print(f"Error extracting model data: {e}")
            continue
        
        model = {
            "name": model_name,
            "url": versions_page_url,
            "brand": brand['name'],
            "lower_price": lower_price,
            "upper_price": upper_price
        }

        models.append(model)
        print(f"Model extracted: {model['name']} - URL: {model['url']} - Prices: {model['lower_price']} - {model['upper_price']} - Brand: {model['brand']}")

        save_model_on_db(model)

    print(f"Found {len(models)} models for brand: {brand['name']}")

    for model in models:
        try:
            
            versions = extract_model_versions(model, browser)

            if not versions:
                print(f"No versions found for model: {model['name']}")
                continue

        except Exception as e:
            print(f"Error processing model {model['name']}: {e}")
            

def extract_price_range(price_str: str) -> tuple[float, float]:
    # Rimuove entità HTML come &nbsp; e decodifica simboli
    cleaned = html.unescape(price_str)

    # Trova tutti i numeri decimali con . o , (che viene trasformato in .)
    numbers = re.findall(r"\d+(?:[\.,]\d+)?", cleaned)
    prices = [float(n.replace(",", ".")) for n in numbers]

    if not prices:
        return (None, None)

    if len(prices) == 1:
        return (prices[0], prices[0])

    return (min(prices), max(prices))


def clean_model_name(model_name: str) -> str:
    # Rimuove eventuali caratteri speciali e spazi extra
    model_name = model_name.split('\n')[-1].strip()
    model_name = model_name.strip()
    model_name = re.sub(r"[^\w\s-]", "", model_name)
    model_name = re.sub(r"\s+", " ", model_name).strip()
    return model_name


def extract_model_versions(model, browser) -> list:
    versions = []

    context = browser.new_context()
    model_page = context.new_page()
    model_page.goto(url_base + model['url'])
    model_page.wait_for_selector("body")

    versions_urls = []

    if not model_page.query_selector("div.apanels-pan"):
        version_cards = model_page.query_selector_all("div.plist-pcard")

        for card in version_cards:
            try:
                anchor = card.query_selector("a.app-add-search")
                url = anchor.get_attribute("href") if anchor else None

                if not url:
                    print(f"No URL found for model version: {model['name']}")
                    continue

                versions_urls.append(url)

            except Exception as e:
                print(f"Error extracting version data: {e}")
                continue
    
    else:
        versions_urls.append(model['url'])

    print(f"Found {len(versions_urls)} versions for model: {model['name']}")

    for url in versions_urls:
        with model_page.context.new_page() as version_page:
            version = extract_version_data(version_page, url)

            if not version:
                print(f"No version data found for URL: {url}")
                continue

        if version:
            versions.append(version)
        
    return versions


def extract_version_data(page, url):
    data = {}
    page.goto(url_base + url)
    page.wait_for_selector(".apanels-pan-wrapper")

    panels = page.query_selector_all(".apanels-pan-wrapper")

    for panel in panels:
        rows = panel.query_selector_all("tr")
        for row in rows:
            th = row.query_selector("th")
            td = row.query_selector("td")
            if th and td:
                key = normalize_key(th.text_content())
                value = clean_text(td.inner_text())
                if value.lower() not in ["n.d.", "-"]:
                    data[key] = value
    
    pprint(f"Extracted version data: {data}")

    return data



def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def normalize_key(key):
    return clean_text(key).lower().replace(" ", "_")


def map_version_data(raw_data: dict) -> dict:
    mapped = {}

    for k, v in raw_data.items():
        key = KEY_MAPPING.get(k.strip())
        if not key:
            continue

        # conversioni smart
        clean_value = v.strip()

        if key.startswith("seat_height") or "travel" in key or "size" in key or "bore" in key or "stroke" in key:
            mapped[key] = parse_mm(clean_value)
        elif key.endswith("_weight"):
            mapped[key] = parse_kg(clean_value)
        elif key in ["displacement", "fuel_capacity"]:
            mapped[key] = parse_float(clean_value)
        elif key in ["ride_by_wire", "traction_control", "abs"]:
            mapped[key] = parse_boolean(clean_value)
        elif key in ["price"]:
            mapped[key] = parse_price(clean_value)
        elif key == "raw_power":
            mapped.update(parse_power(clean_value))
        elif key == "raw_torque":
            mapped.update(parse_torque(clean_value))
        else:
            mapped[key] = clean_value

    return mapped


def save_version_on_db(version_data: dict):
    print(f"Saving version data to DB: {version_data}")
    # Qui si dovrebbe implementare la logica per salvare i dati della versione nel database

def save_brand_on_db(brand_data: dict):
    print(f"Saving brand data to DB: {brand_data}")
    # Qui si dovrebbe implementare la logica per salvare i dati del brand nel database

def save_model_on_db(model_data: dict):
    print(f"Saving model data to DB: {model_data}")
    # Qui si dovrebbe implementare la logica per salvare i dati del modello nel database

app = create_app()    

if __name__ == "__main__":
    with app.app_context():
        scrape_with_playwright()
