from playwright.sync_api import sync_playwright

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

        print("effective brands found: ", len(brands))

        

        models_urls = []
        

        for brand in brands:
            count += 1
            print(f"Brand: {brand['name']}, URL: {brand['url']}")
            page.goto(brand['url'])
            page.wait_for_timeout(1000)

            models = page.query_selector_all("tr.even")
            model_data = []

            for model in models:
                tds = []
                tds = model.query_selector_all("td")
                if tds[0]:
                    if tds[0].query_selector("a"):
                        # modello con più versioni
                        model_url = tds[1].query_selector("a").get_attribute("href")
                        model_url = model_url.replace("..", url_base)

                        models_urls.append(model_url)
                        
                        # Vai nella pagina del modello per estrarre le versioni
                            
                    else:
                        # modello con una sola versione
                        model_url = tds[1].query_selector("a").get_attribute("href")
                        model_url = model_url.replace("..", url_base)
                        model_name = tds[1].text_content().strip()

                        # aggiungi la singola versione alla lista
                        model_data.append({
                            "name": model_name,
                            "url": model_url
                        })

            for url in models_urls:
                page.goto(url)
                page.wait_for_timeout(1000)


                links = page.query_selector_all('a')
                for link in links:
                    title_span = link.query_selector('span[style*="font-size:18px"] b')
                    if title_span:
                        href = link.get_attribute('href')
                        title = title_span.text_content().strip()
                        print(f"Model title: {title}, URL: {href}")
                        model_data.append({
                            "name": title,
                            "url": href.replace("..", url_base)
                        })


            print(f"Found {len(model_data)} total model versions for brand {brand['name']}")

            # Ora VISITA le versioni UNA ALLA VOLTA (eviti perdita di contesto)
            for model in model_data:
                print(f"Visiting model version: {model['name']} ({model['url']})")
                page.goto(model['url'])
                page.wait_for_timeout(1000)

                # Qui estrai i dettagli tecnici del modello (specifiche) e salvali su DB
                # Esempio:
                # specs = page.query_selector_all("table.specs tr")
                # parse specs...

            if count >= 2:
                break


        browser.close()

def model_with_multiple_versions():
    pass

def save_bike_data():
    pass

if __name__ == "__main__":
    scrape_with_playwright()
