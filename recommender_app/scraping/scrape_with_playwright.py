from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
import re
from recommender_app.scraping.mappings_key import KEY_MAPPING
from recommender_app.utils.parsing_utils import extract_float, extract_int

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

        # print("effective brands found: ", len(brands))     

        for brand in brands:
            print(f"Brand: {brand['name']}, URL: {brand['url']}")
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
                        if not any(m['url'] == href.replace("..", url_base) for m in model_versions):
                            model_versions.append({
                                "name": title,
                                "url": href.replace("..", url_base)
                            })

            for url in multi_version_model_urls:
                page.goto(url)
                page.wait_for_selector("a")


                links = page.query_selector_all('a')
                for link in links:
                    title_span = link.query_selector('span[style*="font-size:18px"] b')
                    if title_span:
                        href = link.get_attribute('href')
                        title = title_span.text_content().strip()
                        # print(f"Model title: {title}, URL: {href}")
                        if not any(m['url'] == href.replace("..", url_base) for m in model_versions):
                            model_versions.append({
                                "name": title,
                                "url": href.replace("..", url_base)
                            })


            # print(f"Found {len(model_versions)} total model versions for brand {brand['name']}")

            # Ora VISITA le versioni UNA ALLA VOLTA (eviti perdita di contesto)
            for model in model_versions:
                # print(f"Visiting model version: {model['name']} ({model['url']})")
                page.goto(model['url'])
                page.wait_for_selector("table")

                specs = parse_specs(page)

                # print(f"Specs for {model['name']}: {specs}")



        browser.close()

def model_with_multiple_versions():
    pass

def save_bike_data():
    pass

def parse_specs(page: Page) -> dict:

    try:

        rows = page.query_selector_all("table.Grid tr")
        final_data = {}
        data = {}

        for row in rows:
            tds = row.query_selector_all("td")
            if len(tds) == 2:
                raw_key = tds[0].text_content().strip()
                raw_value = tds[1].text_content().strip()
                if raw_key and raw_value:
                    data[raw_key] = raw_value

        # print("Raw data extracted: ", data)

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
        return final_data
   
    except Exception as e:
        print(f"Error parsing specs: {e}")
        print("")
        return {}

    

if __name__ == "__main__":
    scrape_with_playwright()
