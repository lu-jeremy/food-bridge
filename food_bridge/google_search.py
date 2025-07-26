import requests
from bs4 import BeautifulSoup
from .constants import SEARCH_KEY, SEARCH_ENGINE_ID


class GoogleSearcher:
    def __init__(self):
        self.api_key = SEARCH_KEY
        self.search_engine_id = SEARCH_ENGINE_ID
    
    def search(self, query: str, num_results: int = 5) -> list:
        """Search Google and return list of URLs"""
        try:
            url = f"https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': num_results
            }
            
            print(f"Making request to: {url}")
            print(f"With params: {params}")
            
            response = requests.get(url, params=params)
            print(f"Response status: {response.status_code}")
            
            data = response.json()
            print(f"Response data keys: {data.keys()}")
            
            if 'error' in data:
                print(f"API Error: {data['error']}")
                return []
            
            urls = []
            if 'items' in data:
                for item in data['items']:
                    urls.append(item['link'])
                print(f"Found {len(urls)} URLs")
            else:
                print("No 'items' key in response")
            
            return urls
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def scrape_webpage(self, url: str) -> str:
        """Scrape content from a webpage"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
            
            text = soup.get_text(separator=' ', strip=True)
            return ' '.join(text.split())[:2000]  # Limit content length
        except Exception as e:
            print(f"Scraping error for {url}: {e}")
            return ""