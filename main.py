import os
from flask import Flask, request, jsonify
from query_analyzer import QueryAnalyzer
from web_search import WebSearch
from scraper import WebScraper
from content_analyzer import ContentAnalyzer
from report_generator import ReportGenerator
from dotenv import load_dotenv

load_dotenv()
os.environ['GOOGLE_API_KEY'] = "AIzaSyCXt_3R563rc4Blaec6xXl4m0II9QhGB8w"
os.environ['SERPAPI_API_KEY'] = "85a6b8c69cb95e0b4c9b73b00abdf9bea25677abc33a8da784dbbab0d531556b"

app = Flask(__name__)

def run_agent(query):
    try:
        query_analyzer = QueryAnalyzer()
        web_search = WebSearch()
        scraper = WebScraper()
        content_analyzer = ContentAnalyzer()
        report_generator = ReportGenerator()

        query_type, search_terms = query_analyzer.analyze(query)
        print(f"Query Type: {query_type}, Search Terms: {search_terms}")

        search_results = web_search.search(search_terms, query_type)
        print(f"Search Results: {len(search_results)} URLs")

        scraped_data = scraper.scrape(search_results)
        print(f"Scraped Data: {len(scraped_data)} pages")

        analyzed_data = content_analyzer.analyze(scraped_data, query)
        print(f"Analyzed Data: {len(analyzed_data)} items")

        report = report_generator.generate(query, analyzed_data, query_type)
        print(f"Report: {report}")

        return report
    except Exception as e:
        print(f"Agent error: {e}")
        return {"error": str(e), "status": "failed"}

@app.route('/research', methods=['POST'])
def research():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    result = run_agent(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)