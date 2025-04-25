import os
from serpapi import GoogleSearch

class WebSearch:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")

    def search(self, search_terms, query_type):
        try:
            results = []
            for term in search_terms:
                params = {
                    "q": term,
                    "api_key": self.api_key,
                    "num": 15,  # Increase to get more candidates
                    "gl": "in",
                    "hl": "en"
                }
                search = GoogleSearch(params)
                data = search.get_dict()
                organic_results = data.get("organic_results", [])
                for result in organic_results:
                    results.append({
                        "url": result.get("link"),
                        "title": result.get("title"),
                        "snippet": result.get("snippet"),
                        "date": result.get("date")
                    })
            # Prioritize scrapable domains
            scrapable_domains = ["bbc.com", "indiatoday.in", "timesofindia.indiatimes.com", "weather25.com"]
            filtered_results = [
                r for r in results if any(domain in r["url"] for domain in scrapable_domains)
            ] or results[:5]  # Fallback to top 5 if no scrapable domains
            return filtered_results[:5]
        except Exception as e:
            print(f"WebSearch error: {e}")
            return []