import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_all_info(base_url="https://brainlox.com"):
    visited = set()
    to_visit = [base_url]
    all_texts = []

    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Create a Service object with the ChromeDriver executable path.
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        try:
            print(f"Scraping: {url}")
            driver.get(url)
            # Wait for dynamic content to load
            time.sleep(3)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            # Extract all visible text from the page
            page_text = soup.get_text(separator=" ", strip=True)
            all_texts.append(f"URL: {url}\n{page_text}\n")
            visited.add(url)
            
            # Find all internal links (starting with "/" or the base_url)
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if href.startswith("/"):
                    href = base_url.rstrip("/") + href
                if href.startswith(base_url):
                    # Clean URL by removing fragments and query parameters for deduplication
                    href_clean = re.sub(r"[\?#].*$", "", href)
                    if href_clean not in visited and href_clean not in to_visit:
                        to_visit.append(href_clean)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    driver.quit()
    
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "all_info.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_texts))
    return file_path

if __name__ == "__main__":
    file_path = scrape_all_info("https://brainlox.com")
    print(f"Scraping complete. Data saved to {file_path}")
