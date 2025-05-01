# 🔍 Web Research Agent

A powerful and autonomous web research assistant that can:

- Analyze user queries using **Google Gemini API**
- Perform smart web searches via **SerpAPI**
- Scrape and extract relevant content (with respect to `robots.txt`)
- Score and summarize website content for relevance and reliability
- Generate organized, concise research reports
- Offer a Streamlit-powered chatbot interface for interactive querying

> 🧠 Built to automate deep research with minimal human effort.

---

## 🚀 Getting Started Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/web-research-agent.git
cd web-research-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the root directory with the following:

```env
GOOGLE_API_KEY=your-google-api-key
SERPAPI_API_KEY=your-serpapi-key
```

### 4. Run the Streamlit app
```bash
streamlit run app.py
```

#### Optional: Run on a specific port
```bash
streamlit run app.py --server.port 8507
```

---

## 🌐 Live Demo

👉 [**Web Research Agent Live**](https://your-live-demo-link.com)

---

## ⚙️ Key Features

- ✅ **Query Understanding**  
  Handles factual, opinion-based, exploratory, and procedural queries

- ✅ **Smart Search Strategy**  
  Prefers scrapable domains and filters out low-quality results

- ✅ **Respectful Scraping**  
  Adheres to `robots.txt` and ethical crawling practices

- ✅ **Content Scoring & Summarization**  
  Evaluates content quality and condenses it into a clear summary

- ✅ **Interactive Interface**  
  Streamlit-based chatbot UI for a smooth research experience

---

## 🧪 Testing

Run unit tests with `pytest`:
```bash
pytest tests.py
```

---

## 🛡️ Notes

- Make sure your API keys are valid and active.
- SerpAPI has free usage tiers but may have limits.
- Google Gemini usage may incur billing based on quota.
- You can replace Gemini with any LLM (like OpenAI or Claude) if preferred.

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).
