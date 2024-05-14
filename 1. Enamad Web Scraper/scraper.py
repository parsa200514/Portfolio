import xlsxwriter  # Library for creating Excel files
import requests  # Library for making HTTP requests
from bs4 import BeautifulSoup  # Library for web scraping
import threading  # Library for parallel execution
import time  # Library for time-related functions

responses = []  # List to store HTTP responses


# Function to asynchronously fetch HTTP responses for multiple pages.
def get_response():
    global responses

    # Loop to send GET requests to multiple pages (in Enamad site, page 2 = page 1) 
    for i in range(2, 6668):
        # Construct the URL for the page
        url = f'https://www.enamad.ir/DomainListForMIMT/Index/{i}'

        # Send a GET request to the URL and append the response to the list
        responses.append(requests.get(url))


# Function to scrape data from the website and write it to an Excel file
def scraper():
    global responses

    # Create a new Excel workbook and worksheet
    workbook = xlsxwriter.Workbook('data.xlsx')
    worksheet = workbook.add_worksheet()

    # Initialize a list to store star ratings
    rates = [0]

    # Initialize index for companies
    company_index = 1

    # Loop through pages
    for i in range(0, 6666):
        print(f"Let's go to page {i + 1}\n")

        # Wait until the response for the current page is available
        while len(responses) < i + 1:
            time.sleep(1)

        # Parse the HTML content of the page
        soup = BeautifulSoup(responses[i].text, 'html.parser')

        # Find the main content div
        div_content = soup.find("div", {"id": "Div_Content"})

        # Find all columns containing ratings
        cols = soup.find_all("div", {"class": "col-sm-12 col-md-2"})

        # Extract star ratings from the columns
        for col in cols:
            if col("img"):
                stars = 0
                for img in col("img"):
                    stars += 1

                rates.append(stars)

        # Initialize a counter for lines of text
        lines = 0

        # Extract and write company data to the worksheet
        for line in div_content.text.splitlines():
            if line != '':
                lines += 1

                # Write data to respective columns
                if lines == 1:
                    worksheet.write(f'A{company_index}', f'{line}')
                    continue
                elif lines == 2:
                    worksheet.write(f'B{company_index}', f'{line}')
                    continue
                elif lines == 3:
                    worksheet.write(f'C{company_index}', f'{line}')
                    continue
                elif lines == 4:
                    worksheet.write(f'D{company_index}', f'{line}')
                    continue
                elif lines == 5:
                    worksheet.write(f'E{company_index}', f'{line}')
                    continue
                elif lines == 6:
                    # Write rating to the worksheet
                    worksheet.write(f'F{company_index}', f'{str(rates[company_index])}')
                    lines += 1
                if lines == 7:
                    worksheet.write(f'G{company_index}', f'{line}')
                    continue
                else:
                    worksheet.write(f'H{company_index}', f'{line}')
                    lines = 0
                    company_index += 1

    # Close the workbook
    workbook.close()


# Exception handling
try:
    # Create a thread to fetch responses asynchronously
    thread = threading.Thread(target=get_response)
    thread.start()
    # Call the scraper function
    scraper()
except Exception as e:
    print(f"An exception occurred: {e}")
