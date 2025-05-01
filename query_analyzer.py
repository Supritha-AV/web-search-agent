import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

class QueryAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.prompt_template = """
        Analyze the following query to determine its type and extract search terms:

        Query: {query}

        Output as JSON:
        {
            "query_type": "factual|opinion|exploratory|procedural",
            "search_terms": ["term1", "term2", ...]
        }

        Instructions:
        - Classify the query type:
          - factual: Seeks specific, verifiable information (e.g., "today temperature in Bangalore", "what is the date today", "capital of France")
          - opinion: Requests subjective views (e.g., "best restaurant in Bangalore")
          - exploratory: Broad, open-ended research (e.g., "history of Bangalore")
          - procedural: How-to or process-oriented (e.g., "how to check weather in Bangalore")
        - Extract concise, normalized search terms for web search. Remove redundant words (e.g., "in", "the"), lowercase terms, and combine relevant keywords (e.g., "today temperature in Bangalore" -> ["bangalore temperature today"], "what is the date today" -> ["current date today"]).
        - For time-sensitive queries (e.g., containing "today", "current"), ensure search terms include time-specific keywords.
        - Return valid JSON only, no extra text or markdown.
        """

    def analyze(self, query):
        try:
            prompt = self.prompt_template.format(query=query)
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            text = re.sub(r'^```json\s*|\s*```$|^```|\s*```$', '', text).strip()
            result = json.loads(text)
            query_type = result.get("query_type", "exploratory")
            search_terms = result.get("search_terms", [query.lower()])
            return query_type, search_terms
        except Exception as e:
            return "factual", [query.lower().replace("in ", "").replace("what is ", "")]  # Improved fallback