import os
import json
import re
import google.generativeai as genai
from urllib.parse import urlparse

class ContentAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.prompt_template = """
        Analyze the following content for relevance and reliability in relation to the query: "{query}"

        Content: {content}
        Source: {url}

        Output as JSON:
        {
            "relevance_score": 0.0,
            "reliability_score": 0.0,
            "summary": "Brief summary of the content (1000 words)",
            "is_relevant": true
        }

        Instructions:
        - relevance_score: 0.0 to 1.0, based on query relevance. Assign higher scores if content contains keywords like "temperature", "weather", "date", or query location.
        - reliability_score: 0.0 to 1.0, based on source credibility. Assign 0.9 for .edu/.gov, 0.8 for news/weather sites (e.g., bbc.com, indiatoday.in), else 0.7.
        - summary: Summarize key points relevant to the query, focusing on specific data (e.g., temperature, date).
        - is_relevant: true if content mentions query-related data, else false.
        - Return valid JSON only, no extra text or markdown.
        """

    def analyze(self, scraped_data, query):
        analyzed_data = []
        for item in scraped_data[:5]:
            try:
                domain = urlparse(item["url"]).netloc
                reliability = 0.9 if domain.endswith((".edu", ".gov")) else 0.8 if domain in ("www.bbc.com", "www.indiatoday.in", "timesofindia.indiatimes.com", "www.weather25.com") else 0.7
                prompt = self.prompt_template.format(
                    query=query,
                    content=item["content"][:1000],
                    url=item["url"]
                )
                response = self.model.generate_content(prompt)
                text = response.text.strip()
                text = re.sub(r'^```json\s*|\s*```$|^```|\s*```$|[\n\s]*"', '"', text).strip()
                result = json.loads(text)
                result["reliability_score"] = max(result["reliability_score"], reliability)
                if result["is_relevant"]:
                    analyzed_data.append({
                        "url": item["url"],
                        "title": item["title"],
                        "content": item["content"],
                        "summary": result["summary"],
                        "relevance_score": result["relevance_score"],
                        "reliability_score": result["reliability_score"]
                    })
            except Exception as e:
                
                analyzed_data.append({
                    "url": item["url"],
                    "title": item["title"],
                    "content": item["content"],
                    "summary": f"Content from {item['url']} related to the query.",
                    "relevance_score": 0.7,
                    "reliability_score": reliability
                })
        return sorted(analyzed_data, key=lambda x: x["relevance_score"], reverse=True)[:5]