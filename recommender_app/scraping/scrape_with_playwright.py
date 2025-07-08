from playwright.sync_api import sync_playwright

def scrape_with_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.autoevolution.com/moto/")
        content = page.content()
        print(content[:1000])  # stampa i primi 1000 char per test
        browser.close()

if __name__ == "__main__":
    scrape_with_playwright()
