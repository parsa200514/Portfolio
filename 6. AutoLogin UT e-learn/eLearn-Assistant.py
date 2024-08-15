'''
    This project utilizes Selenium WebDriver for web automation,
specifically for logging into the "https://elearn4.ut.ac.ir" website. (University of Tehran e-learn)
It incorporates JSON for data persistence, allowing users to save and reuse their login credentials. (once forever)
Here's a summary of the key functionalities:


-Data Storage with JSON:
Utilizes JSON to store and retrieve login credentials persistently in the "data/data.json" file.

-Conditional Logic:
Checks whether the data file is empty. If it is, prompts the user to input their username and password, saves the data in JSON format, and proceeds with the login.
If the data file is not empty, retrieves the stored credentials from the JSON file and uses them for login.

-Web Automation with Selenium:
Initializes the Chrome WebDriver using WebDriver Manager and ChromeDriverManager to automate browser interactions.

-Logging into a Website:
Navigates to the "https://elearn4.ut.ac.ir/login/index.php" website.
Finds the username and password fields using WebDriver's explicit wait functionality.
Inputs the retrieved username and password into the respective fields.
Simulates pressing the "Enter" key to submit the login form.

-Exception Handling:
Implements exception handling to catch and print any exceptions that may occur during the automation process.

-Browser Cleanup:
Closes the browser using driver.quit() in the finally block to ensure proper cleanup.

-Delay for Page Loading:
Introduces delays using time.sleep() to allow for the website to load before performing actions.
'''

import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

#empty this file if you wanna use a new username or password. DO NOT DELETE the file!
data_path = "data/data.json"

if os.stat(data_path).st_size == 0 :
    # Enter your username and password here. (once forever)
    username=input("Username: ")
    password=input("Password: ")
    
    key = username+','+password
    with open(data_path, 'w') as f:
        json.dump(key, f)
        
else:
    print("preparing your data...")
    with open(data_path, 'r') as g:
        key = json.load(g)
        
    key = key.split(',')
    
    username = key[0]
    password = key[1]
    
    print("landing the browser...")
    # Initialize the Chrome WebDriver using WebDriver Manager and Service
    chrome_service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service)

    print("reaching elearn4.ut.ac.ir...")
    # Open the website
    driver.get("https://elearn4.ut.ac.ir/login/index.php")

    print("waiting 5 seconds for the site to load...")
    time.sleep(5)
    
    print("logging in...")

    # Perform actions
    try:
        # Find the username and password fields and input your credentials
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'Username'))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'password'))
        )

        username_field.send_keys(username)
        password_field.send_keys(password)

        # Simulate pressing Enter to submit the form
        password_field.send_keys(Keys.RETURN)

    except Exception as e:
        print(f"An exception occurred: {e}")

    finally:
        # Close the browser
        print("Done! app will close in 5 seconds")
        time.sleep(5)
        driver.quit()
