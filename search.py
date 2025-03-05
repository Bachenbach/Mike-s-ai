# core/search/google_search.py
import requests
from serpapi import GoogleSearch
from core.config import Config

class GoogleSearchEngine:
    def __init__(self):
        self.api_key = Config.GOOGLE_API_KEY
        self.cse_id = Config.GOOGLE_CSE_ID
        self.serpapi_key = Config.SERPAPI_API_KEY

    async def search(self, query, num_results=5):
        try:
            # Using official Google API
            params = {
                'key': self.api_key,
                'cx': self.cse_id,
                'q': query,
                'num': num_results
            }
            response = requests.get(Config.GOOGLE_SEARCH_URL, params=params)
            results = response.json()
            
            # Using SerpAPI as backup
            serpapi_params = {
                "api_key": self.serpapi_key,
                "engine": "google",
                "q": query,
                "num": num_results
            }
            serpapi_results = GoogleSearch(serpapi_params).get_dict()
            
            # Combine and process results
            combined_results = self._process_results(results, serpapi_results)
            return combined_results
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []

    def _process_results(self, google_results, serpapi_results):
        processed = []
        
        # Process Google API results
        if 'items' in google_results:
            for item in google_results['items']:
                processed.append({
                    'title': item.get('title'),
                    'link': item.get('link'),
                    'snippet': item.get('snippet'),
                    'source': 'Google API'
                })
                
        # Process SerpAPI results
        if 'organic_results' in serpapi_results:
            for item in serpapi_results['organic_results']:
                processed.append({
                    'title': item.get('title'),
                    'link': item.get('link'),
                    'snippet': item.get('snippet'),
                    'source': 'SerpAPI'
                })
                
        return processed
