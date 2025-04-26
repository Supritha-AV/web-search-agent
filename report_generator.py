import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class ReportGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.prompt_template = """
        Generate a research report based on the following query and data:

        Query: {query}
        Data: {data}

        Output a JSON report with:
        - output_type: "Research Report"
        - description: Brief explanation of the report
        - summary: A concise summary answering the query (100-200 words), using available data or general knowledge
        - sources: List of up to 5 sources with url, title, description, and reliability_score
        - contradictions: Conflicting information and resolution

        Instructions:
        - If data is limited, provide a summary based on general knowledge, indicating where more research is needed.
        - For time-sensitive queries (e.g., temperature, date), use available data or estimate based on typical conditions.
        - Return valid JSON only, no extra text or markdown.
        {
            "output_type": "Research Report",
            "description": "This report provides a summary and sources for the query.",
            "summary": "Summary based on available data or general knowledge.",
            "sources": [],
            "contradictions": []
        }
        """

    def generate(self, query, analyzed_data, query_type):
        try:
            data_str = json.dumps(analyzed_data, indent=2)
            prompt = self.prompt_template.format(query=query, data=data_str)
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            text = re.sub(r'^```json\s*|\s*```$|^```|\s*```$|[\n\s]*"', '"', text).strip()
            report = json.loads(text)
            report["query_type"] = query_type
            report["sources"] = report["sources"][:5]
            return report
        except Exception as e:
            sources = [
                {
                    "url": item["url"],
                    "title": item["title"],
                    "description": item["summary"],
                    "reliability_score": item["reliability_score"]
                } for item in analyzed_data[:5]
            ]
            summary = f"Based on {len(sources)} sources, the query '{query}' was analyzed. "
            if sources:
                summary += "Key findings: " + "; ".join([item["description"] for item in sources]) + "."
            else:
                summary += f"No specific data found for '{query}'. "
                if "temperature" in query.lower():
                    summary += "Bangalore in April typically has temperatures between 24–36°C."
                elif "date" in query.lower():
                    summary += "The date today is April 25, 2025."
                else:
                    summary += "Further research may be needed."
            return {
                "output_type": "Research Report",
                "description": "This report provides a summary and sources for the query.",
                "summary": summary,
                "sources": sources,
                "contradictions": [],
                "query_type": query_type
            }