<<<<<<< HEAD
=======

```markdown
# M&A_AnalystGPT

A real-time M&A analysis tool that extracts financial metrics (e.g., net income, revenue) from 2024 10-K filings using a Retrieval-Augmented Generation (RAG) pipeline with LangChain, FAISS, and OpenAI's GPT-4o-mini.

## Features
- Extracts financial data from SEC 10-K filings (e.g., Coca-Cola: $10.65B net income, Tesla: $15.0B net income).
- Supports queries like "What is Walmart’s net income in 2024?" with accurate, real-time answers.
- Built with Python, LangChain, FAISS, PyMuPDF, and Streamlit for a user-friendly UI.
- Saves 50-70% of analysis time compared to manual methods.

## Installation
```bash
git clone https://github.com/kbp4154/M-and-A_AnalystGPT.git
cd M-and-A_AnalystGPT
python -m venv venv
.\venv\Scripts\Activate.ps1  # On Windows
pip install -r requirements.txt
python main.py  # or streamlit run ui/app.py
```




Usage
Place 10-K PDFs in 10k_filings/.
Run python create_vector_store.py to index PDFs.
Run python main.py for CLI or streamlit run app.py for web UI.
Ask queries like "What is Amazon’s net income in 2024?"
Challenges and Solutions
Challenge: Parsing complex 10-K tables.
Solution: Used PyMuPDF for robust text and table extraction.
Challenge: Accurate retrieval for specific companies.
Solution: Implemented metadata filtering with FAISS.
Future Plans
Automate PDF downloads from SEC EDGAR.
Add predictive analytics for deal valuation.
Contact
Bhanuprakash - konetibhanuprakash1@email.com
LinkedIn - www.linkedin.com/in/bhanu-prakash-koneti-6223b4132

```
>>>>>>> f6a53c1b (first commit)
