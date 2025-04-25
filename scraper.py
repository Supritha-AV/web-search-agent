import requests
from bs4 import BeautifulSoup
import urllib.robotparser
import re  # Added import

class WebScraper:
    def __init__(self):
        self.user_agent = "MasonryWebAgent/1.0"

    def can_scrape(self, url):
        try:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"{url}/robots.txt")
            rp.read()
            return rp.can_fetch(self.user_agent, url)
        except:
            return True

    def scrape(self, search_results):
        scraped_data = []
        for result in search_results:
            url = result["url"]
            if not self.can_scrape(url):
                print(f"Blocked by robots.txt: {url}")
                continue
            try:
                response = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                content = (soup.find("article") or
                          soup.find("main") or
                          soup.find("section") or
                          soup.find("div", class_=re.compile("content|weather|forecast")) or
                          soup.find("body"))
                text = content.get_text(strip=True) if content else ""
                if text:
                    scraped_data.append({
                        "url": url,
                        "title": result["title"],
                        "content": text[:2000],
                        "date": result.get("date")
                    })
            except Exception as e:
                print(f"Scrape error for {url}: {e}")
                continue
        return scraped_data