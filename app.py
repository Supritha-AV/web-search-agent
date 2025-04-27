import streamlit as st
from query_analyzer import QueryAnalyzer
from web_search import WebSearch
from scraper import WebScraper
from content_analyzer import ContentAnalyzer
from report_generator import ReportGenerator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
os.environ['SERPAPI_API_KEY'] = os.getenv("SERPAPI_API_KEY")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

def run_agent(query):
    try:
        query_analyzer = QueryAnalyzer()
        web_search = WebSearch()
        scraper = WebScraper()
        content_analyzer = ContentAnalyzer()
        report_generator = ReportGenerator()

        query_type, search_terms = query_analyzer.analyze(query)
        search_results = web_search.search(search_terms, query_type)
        scraped_data = scraper.scrape(search_results)
        analyzed_data = content_analyzer.analyze(scraped_data, query)
        report = report_generator.generate(query, analyzed_data, query_type)
        return report
    except Exception as e:
        return {"error": "An error occurred", "status": "failed"}

# Streamlit interface
st.title("Web Search Agent Chatbot")
st.markdown("Chat with me to search and analyze web content!")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
query = st.chat_input("Enter your query (e.g., What is the capital of France?):")

if query:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Process query and generate response
    with st.chat_message("assistant"):
        with st.spinner("Processing your query..."):
            report = run_agent(query)

        if "error" in report:
            response = "Unable to process the query. Please try again."
        else:
            # Format the report as a conversational response
            response = f"### Research Report\n\n**Description**: {report['description']}\n\n**Summary**: {report['summary']}\n\n### Sources\n"
            if report["sources"]:
                for i, source in enumerate(report["sources"], 1):
                    response += f"- **Source {i}: {source['title']}**  \n  URL: {source['url']}  \n  Description: {source['description']}  \n  Reliability Score: {source['reliability_score']:.2f}\n"
            else:
                response += "No sources found.\n"

            response += "\n### Contradictions\n"
            if report["contradictions"]:
                for contradiction in report["contradictions"]:
                    response += f"- {contradiction}\n"
            else:
                response += "No contradictions found.\n"

        # Display response
        st.markdown(response)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

