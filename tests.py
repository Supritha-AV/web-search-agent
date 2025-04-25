import pytest
from query_analyzer import QueryAnalyzer
from web_search import WebSearch
from scraper import WebScraper
from content_analyzer import ContentAnalyzer
from report_generator import ReportGenerator

def test_query_analyzer():
    analyzer = QueryAnalyzer()
    query_type, search_terms = analyzer.analyze("What is the capital of France?")
    assert query_type == "factual"
    assert "capital of France" in search_terms

def test_web_search():
    web_search = WebSearch()
    results = web_search.search(["capital of France"], "factual")
    assert len(results) <= 5
    assert all("url" in r for r in results)

def test_scraper():
    scraper = WebScraper()
    results = [{"url": "https://en.wikipedia.org/wiki/France", "title": "France"}]
    scraped_data = scraper.scrape(results)
    assert len(scraped_data) > 0
    assert "content" in scraped_data[0]

def test_content_analyzer():
    analyzer = ContentAnalyzer()
    data = [{
        "url": "https://en.wikipedia.org/wiki/France",
        "title": "France",
        "content": "The capital of France is Paris."
    }]
    analyzed = analyzer.analyze(data, "What is the capital of France?")
    assert len(analyzed) > 0
    assert analyzed[0]["relevance_score"] > 0.5

def test_report_generator():
    generator = ReportGenerator()
    data = [{
        "url": "https://en.wikipedia.org/wiki/France",
        "title": "France",
        "content": "The capital of France is Paris.",
        "summary": "The capital is Paris.",
        "relevance_score": 0.9,
        "reliability_score": 0.9
    }]
    report = generator.generate("What is the capital of France?", data, "factual")
    assert "summary" in report
    assert "Paris" in report["summary"]

def test_report_generator_top5():
    generator = ReportGenerator()
    # Create 6 items to test the 5-item limit
    data = [
        {
            "url": f"https://example.com/{i}",
            "title": f"Title {i}",
            "content": f"Content {i}",
            "summary": f"Summary {i}: This is a brief description of content {i}.",
            "relevance_score": 0.9 - i * 0.1,
            "reliability_score": 0.9
        } for i in range(6)
    ]
    report = generator.generate("Test query", data, "factual")
    assert report["output_type"] == "Research Report"
    assert len(report["sources"]) <= 5
    assert all("description" in source for source in report["sources"])
    assert all("url" in source for source in report["sources"])
    assert all("title" in source for source in report["sources"])
    assert all("reliability_score" in source for source in report["sources"])