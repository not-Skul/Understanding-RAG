import requests
from bs4 import BeautifulSoup
import trafilatura

def fetch_links(base_url, allowed_prefix):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(base_url, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith(allowed_prefix):
                links.add(href if href.startswith('http') else base_url + href)
        print(f"Found {len(links)} links")
        return list(links)
    except Exception as e:
        print(f"Error fetching links: {e}")
        return []

def extract_text(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            return text
        else:
            print(f"Failed to download: {url}")
            return None
    except Exception as e:
        print(f"Error extracting from {url}: {e}")
        return None


print("Starting scraper...")
urls = fetch_links("https://www.startupindia.gov.in/", "/content/sih/en/")
print(f"Processing {len(urls)} URLs")

for url in urls:
    print(f"Processing URL: {url}")
    text = extract_text(url)
    if text:
        print(f"Scraped {url[:60]}... ({len(text)} chars)")
        with open("scraped_content.txt", "a", encoding="utf-8") as f:
            f.write(f"URL: {url}\n")
            f.write(text + "\n\n")
    else:
        print(f"No text extracted from {url}")