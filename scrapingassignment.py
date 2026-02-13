import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 1. Configuration
news_sites = [
    "https://kathmandupost.com",
    "https://thehimalayantimes.com",
    "https://english.onlinekhabar.com" # Using the English version for better keyword matching
]

# We can search for both English and Nepali terms to be thorough
keywords = ["Election", "Vote", "निर्वाचन"]

def scrape_site(url):
    articles_found = []
    seen_links = set() # To prevent duplicate entries of the same article

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # 2. Logic: Find all anchor tags
        for link in soup.find_all("a", href=True):
            title = link.get_text(strip=True)
            href = link["href"]
            
            # Skip empty titles or very short fragments
            if len(title) < 10:
                continue

            # 3. Keyword Check (checks if any of our keywords are in the title)
            if any(k.lower() in title.lower() for k in keywords):
                
                # Use urljoin to handle relative paths correctly
                full_url = urljoin(url, href)

                # 4. De-duplication
                if full_url not in seen_links:
                    articles_found.append({"title": title, "link": full_url})
                    seen_links.add(full_url)

        return articles_found

    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        return []

# --- Execution ---
print(f"🔎 Searching for election news in Nepal...\n")

for site in news_sites:
    print(f"Checking {site}...")
    results = scrape_site(site)
    
    if results:
        for idx, item in enumerate(results, 1):
            print(f"  {idx}. {item['title']}")
            print(f"     Link: {item['link']}\n")
    else:
        print("  No matching articles found on the homepage.\n")