import requests
from bs4 import BeautifulSoup
from .constants import SEARCH_KEY, SEARCH_ENGINE_ID


class GoogleSearcher:
    def __init__(self):
        self.api_key = SEARCH_KEY
        self.search_engine_id = SEARCH_ENGINE_ID
    
    def search(self, query: str, num_results: int = 5) -> list:
        """Search using Bing search which is less restrictive"""
        try:
            search_url = "https://www.bing.com/search"
            params = {'q': query, 'count': num_results}
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            print(f"Searching Bing for: {query}")
            response = requests.get(search_url, params=params, headers=headers)
            print(f"Response status: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            urls = []
            # Bing uses different selectors
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http') and 'bing.com' not in href and 'microsoft.com' not in href:
                    if len(urls) < num_results:
                        urls.append(href)
                        print(f"Found URL: {href}")
            
            print(f"Total found {len(urls)} URLs: {urls}")
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