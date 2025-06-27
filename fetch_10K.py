# fetch_10k.py
from sec_edgar_downloader import Downloader
from loguru import logger
import os

def fetch_10k(companies, year, output_dir="10k_filings"):
    try:
        dl = Downloader("M&A_AnalystGPT", "user@example.com", output_dir)
        os.makedirs(output_dir, exist_ok=True)
        for company, cik in companies.items():
            logger.info(f"Fetching 10-K for {company} (CIK: {cik}, year: {year})")
            dl.get("10-K", cik, after=f"{year}-01-01", before=f"{year}-12-31")
    except Exception as e:
        logger.error(f"Failed to fetch 10-K: {e}")

if __name__ == "__main__":
    companies = {
        "walmart": "0000104169",
        "tesla": "0001318605",
        "coca-cola": "0000021344",
        "pepsico": "0000077476",
        "amazon": "0001018724",
        "alphabet": "0001652044"
    }
    fetch_10k(companies, 2024)