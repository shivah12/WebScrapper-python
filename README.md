# AI Web Scraper with Streamlit

This project is a web-based tool built using Streamlit and BeautifulSoup that allows users to extract specific data (tables, headings, or rows) from webpages. The tool enables quick preview, visualization, and CSV export of the scraped data.

## Features

- Input any webpage URL
- Select the type of data to extract: full table, headings, or specific rows
- Visualize the extracted data using basic charts
- Export the data to a CSV file
- Simple and user-friendly interface

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-web-scraper.git
cd ai-web-scraper
````

### 2. Create and activate a virtual environment (recommended)

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

## Project Structure

```
app/
├── app.py               # Main Streamlit app
├── scraper.py           # Contains scraping logic
├── interpreter.py       # AI prompt → selector logic (optional)
├── utils.py             # CSV export, error handling
├── requirements.txt
```

## Secrets Setup (Optional)

If using an OpenAI API key or other environment variables, create `.streamlit/secrets.toml` like this:

```toml
[openai]
api_key = "your-openai-api-key"
```

Access it in your code as:

```python
st.secrets["openai"]["api_key"]
```

## Dependencies

* streamlit
* pandas
* beautifulsoup4
* lxml
* matplotlib

## Deployment

You can deploy this project on Streamlit Cloud. Just upload your code and add your `secrets.toml` in the Settings → Secrets section of your app.


Let me know if you’d like badges, Docker setup, or example screenshots added.
```
