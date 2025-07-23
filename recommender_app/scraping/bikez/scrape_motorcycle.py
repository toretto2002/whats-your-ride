import requests
from bs4 import BeautifulSoup

url = "https://www.autoevolution.com/moto/"

def scrape_motorcycle_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    print("Starting web scraping for motorcycle data...")
    response = requests.get(url, headers=headers)
    print("response status code:", response)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        for brand_div in soup.find_all('div', class_='col2width fl bcol-white carman'):
            brand_name = brand_div.find('a').title.strip()
            print(f"Brand: {brand_name}")
    else:
        print("Failed to fetch page. Status code:", response.status_code)

if __name__ == "__main__":
    scrape_motorcycle_data()
