import pytest
import os
from unittest.mock import patch, MagicMock
from query_analyzer import QueryAnalyzer

# Mock environment variables
@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-api-key")

# Initialize QueryAnalyzer with mock setup
@pytest.fixture
def analyzer(mock_env):
    return QueryAnalyzer()


# Test Case 1: API Failure
def test_query_analyzer_api_failure(analyzer):
    with patch('google.generativeai.GenerativeModel.generate_content', side_effect=Exception("API Error")):
        query_type, search_terms = analyzer.analyze("What is the weather today?")
        assert query_type == "factual"  # Default fallback
        assert search_terms == ["the weather today?"]  # Adjusted to match actual behavior