from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright
import re
from urllib.parse import urlparse
import requests

def is_valid_url(url):
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_data(url, option_or_selector, is_custom=False):
    # Validate URL
    if not url or not is_valid_url(url):
        raise ValueError("Please enter a valid URL")
    
    html = None
    browser = None
    
    # Try Playwright first (for JavaScript-heavy sites)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set longer timeout and better error handling
            page.goto(url, timeout=120000, wait_until="networkidle")
            page.wait_for_load_state("networkidle", timeout=30000)
            
            html = page.content()
            
    except Exception as e:
        print(f"Playwright failed: {e}")
        # Fallback to requests for simpler sites
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            html = response.text
        except Exception as req_error:
            raise Exception(f"Failed to load webpage with both Playwright and requests: {str(e)} | {str(req_error)}")
    finally:
        if browser:
            browser.close()

    if not html:
        raise Exception("No HTML content received")

    soup = BeautifulSoup(html, "lxml")

    try:
        if is_custom:
            elements = soup.select(option_or_selector)
            if not elements:
                return pd.DataFrame(columns=["Extracted Data"])
            data = [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]
            return pd.DataFrame(data, columns=["Extracted Data"])

        elif option_or_selector == "All Tables":
            tables = pd.read_html(html)
            if not tables:
                return pd.DataFrame(columns=["No tables found"])
            return tables[0] if tables else pd.DataFrame(columns=["No data"])

        elif option_or_selector == "Headings":
            headings = soup.find_all(["h1", "h2", "h3", "h4"])
            if not headings:
                return pd.DataFrame(columns=["Heading Level", "Text"])
            data = [(tag.name, tag.get_text(strip=True)) for tag in headings if tag.get_text(strip=True)]
            return pd.DataFrame(data, columns=["Heading Level", "Text"])

        elif option_or_selector == "Specific Row/Column":
            tables = pd.read_html(html)
            if not tables:
                return pd.DataFrame(columns=["No tables found"])
            return tables[0].iloc[[0], :] if len(tables[0]) > 0 else pd.DataFrame(columns=["No data"])

        return pd.DataFrame(columns=["No data found"])
        
    except Exception as e:
        raise Exception(f"Error processing data: {str(e)}")
