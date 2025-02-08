# Triluxo_Internship

## Project Overview
This project is a web scraping, document processing, and AI-powered chatbot system designed to extract and organize data from the Brainlox website. The application provides meaningful responses by leveraging embeddings and vector storage for efficient data retrieval and querying.

### Key Features:
1. **Web Scraper:** Uses Selenium and BeautifulSoup to crawl the Brainlox website, extracting and storing relevant information.
2. **Data Processing:** Text splitting and embedding generation using Hugging Face models.
3. **Vector Store:** FAISS (Facebook AI Similarity Search) integration for optimized document search and retrieval.
4. **Chatbot Integration:** Query processing via API for interactive chatbot responses.

---

## Usage
### Scraper (`scraper.py`)
- Extracts text from multiple pages on the Brainlox website.
- Cleans and saves content to `data/all_info.txt`.

### Vector Store (`vector_store.py`)
- Splits the text into manageable chunks.
- Generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
- Saves the FAISS vector index.

### Chatbot
- Interactive client (`client.py`) sends queries to the backend.
- Returns structured responses based on the scraped data.


