from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
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
from recommender_app.services.version_service import VersionService
from recommender_app.services.brand_service import BrandService
from recommender_app.services.model_service import ModelService
from recommender_app.services.category_service import CategoryService


url_base = "https://www.moto.it"

def scrape_with_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(180000)  # Timeout di default per tutte le operazioni (30s)
        page.set_default_navigation_timeout(180000)  # Timeout di default per le navigazioni (60s)
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

        with ThreadPoolExecutor(max_workers=3) as executor:
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
                page.set_default_timeout(180000)
                page.set_default_navigation_timeout(180000)
                page.goto(url_base + brand['url'])

                extract_brand_infos(page, brand, browser)
                print(f"Brand {brand['name']} processed successfully.")

                browser.close()
            except Exception as e:
                print(f"Error processing brand {brand['name']}: {e}")


def extract_brand_infos(page: Page, brand: dict, browser):
    models = []

    brand_id = save_brand_on_db(brand)

    cards_models_in_list = page.query_selector_all("div.plist-pcard")

    if not cards_models_in_list:
        print(f"No models found for brand: {brand['name']}")
        return []
    
    for card in cards_models_in_list:
        try:
            anchor = card.query_selector("a.app-set-model")
            model_text = anchor.text_content() if anchor else ""
            model_name = clean_model_name((model_text or "").strip()) or "Unknown Model"
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

    category_id = None
    versions_ids = []
    
    for model in models:
        try:
            # Estrai le versioni (senza ancora salvarle)
            versions = extract_model_versions(model, browser)

            if not versions:
                print(f"No versions found for model: {model['name']}")
                continue

            # Aggiungi la categoria (una tantum)
            category_id = add_category_if_not_exists(versions[0].get("categoria", "Unknown Category"))

            # Salva il model PRIMA, senza le versioni
            model_data = {
                "name": model['name'],
                "brand_id": brand_id,
                "lower_price": model['lower_price'],
                "upper_price": model['upper_price'],
                "category_id": category_id
            }

            model_id = save_model_on_db(model_data)  # questa funzione deve ritornare l'id
            versions_ids = []

            # Ora salva le versioni, con il model_id corretto
            for version in versions:
                if not version:
                    print(f"No version data found for model: {model['name']}")
                    continue

                version['model_id'] = model_id  # 👉 QUI risolvi l'errore

                version_id = save_version_on_db(version)
                if version_id != -1:
                    versions_ids.append(version_id)
                else:
                    raise ValueError(f"Failed to save version for model: {model['name']}")

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
    model_page.set_default_timeout(180000)
    model_page.set_default_navigation_timeout(180000)
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

    for url in versions_urls:
        with model_page.context.new_page() as version_page:
            version_page.set_default_timeout(180000)
            version_page.set_default_navigation_timeout(180000)
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
    
    try:

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
    except Exception as e:
        print(f"Error extracting version data from {url}: {e}")
        return None

    return data


def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def normalize_key(key):
    return clean_text(key).lower().replace(" ", "_")


def map_version_data(raw_data: dict) -> dict:
    mapped = {}

    for k, v in raw_data.items():
        
        if not k or not v:
            continue
        
        key = KEY_MAPPING.get(k.strip().lower())
        if not key:
            continue

        if isinstance(v, str):
            clean_value = v.strip()
        elif v is not None:
            clean_value = str(v).strip()
        else:
            clean_value = ""


        if key.startswith("seat_height") or "travel" in key or "size" in key or "bore" in key or "stroke" in key or "weight" in key or "length" in key or "width" in key or "height" in key or "wheelbase" in key:
            mapped[key] = parse_mm(clean_value)
        elif key.endswith("_weight"):
            mapped[key] = parse_kg(clean_value)
        elif key in ["displacement", "fuel_capacity"]:
            mapped[key] = parse_float(clean_value)
        elif key in ["ride_by_wire", "traction_control", "abs", "depowered", "reverse_gear"]:
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


def save_version_on_db(version_data: dict) -> int:
    version_service = VersionService()
    dto = map_version_data(version_data)
    if not dto:
        print("No valid data to save.")
        return -1

    try:
        version = version_service.get_or_create_version(dto)
    except Exception as e:
        print(f"Error saving version data: {e}")
    
    

def save_brand_on_db(brand_data: dict) -> int:
    brand_service = BrandService()
    try:
        brand_id = brand_service.get_or_create_brand(brand_data)
        return brand_id
    except Exception as e:
        print(f"Error saving brand data: {e}")
        return -1

def save_model_on_db(model_data: dict):
    model_service = ModelService()
    try:
        model_id = model_service.get_or_create_model(model_data)
        return model_id
    except Exception as e:
        print(f"Error saving model data: {e}")

def add_category_if_not_exists(category_name: str) -> int:
    category_service = CategoryService()
    
    existing_category = category_service.get_category_by_name(category_name)
    if existing_category:
        return existing_category.id
    
    new_category_id = category_service.create_category({"name": category_name})
    return new_category_id


app = create_app()    

if __name__ == "__main__":
    with app.app_context():
        scrape_with_playwright()
