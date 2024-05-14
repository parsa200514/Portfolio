------------------------------------------------------------------------------------
# Enamad Web Scraper

    This Python script is designed and developed by parsa200514 to scrape data
    from Enamad's website and store it in an Excel file. It utilizes the `requests`
    library to send HTTP requests and the `BeautifulSoup` library for HTML parsing.

------------------------------------------------------------------------------------
## Installation

Install the required dependencies:

    pip install -r requirements.txt

------------------------------------------------------------------------------------
## Usage

1. Run the `scraper.py` script:

    python scraper.py

2. The script will scrape data from multiple pages of Enamad's website and write it
   to an Excel file named `data.xlsx`.

------------------------------------------------------------------------------------
## Dependencies

- `requests`: For sending HTTP requests to the Enamad website.
- `BeautifulSoup`: For parsing the HTML content of the website.
- `xlsxwriter`: For creating and writing data to Excel files.
