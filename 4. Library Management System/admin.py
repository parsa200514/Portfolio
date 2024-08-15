#This file is designed for admin(bookclerk) panel logic

import sqlite3
import requests

database_path = 'app/database.db'

#weather_data description
'''
    The function starts by attempting to get the user's location based on their IP address using the ipinfo.io API. If successful, it extracts the city name. If there's an exception during this process, it defaults to 'new york' as the location.
The function then sets up the Tomorrow.io API key and prepares the URL for the weather forecast request. It converts the location to lowercase and replaces spaces with '%20' to ensure proper URL formatting.
It makes a request to the Tomorrow.io API using the prepared URL and API key. If the response status code is 200 (OK), it extracts relevant weather information for the next 5 days, including date, average temperature, and average humidity.
If the response status code is 400, it sets the result to "N/A" to indicate that the data is not available. If there's an error or an exception during the API request, it sets the result to specific error messages.
Finally, the function returns a list containing the weather information for the specified location and days. The list includes the location name in uppercase and a series of lines for each day's date, average temperature, and average humidity.
'''
def weather_data():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        location = data.get('city')
    except Exception as e:
        print(f"Error: {e}")
        location = 'new york'
        
    result=[]
    api_key = "Nw2B9zObq40Q6OTFe2eqFhP3Dkjhu1FN"
    
    edited_location = (location.lower()).replace(' ','%20')
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={edited_location}&apikey={api_key}"
    headers = {"accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
        
            location = data['location']['name']
            result.append("location : "+ location.upper())
            for day in range(0,5):
                date = data['timelines']['daily'][day]['time']
                temprature = data['timelines']['daily'][day]['values']['temperatureAvg']
                humidity = data['timelines']['daily'][day]['values']['humidityAvg']

                line = f'Date : {date} / Temprature (avg) : {temprature} / Humidity : {humidity}'
                result.append(line)

        elif response.status_code == 400:
            result="N/A"
        
        else: result="Something went Wrong! please retry."
    except Exception:
        result="Turn on your VPN."
        
    return result


#book_management description
'''
    The function starts by connecting to the SQLite database using the provided database_path and initializing a cursor.
If the edit parameter is False, indicating that the user wants to view existing books, the function executes a SELECT query on the books table to retrieve all books. It then formats the result into a string.
If the edit parameter is True, indicating that the user wants to add or remove a book, the function checks the action parameter. If the action is "add," it prompts the user for information about the new book (author, subject, year) and adds it to the books table. If the action is "remove," it prompts the user for the name of the book to remove and deletes it from the books table.
After performing the specified action, the function fetches all rows from the books table and formats the result into a string.
Finally, the function closes the database connection and returns the formatted result.
'''
def book_management(edit,action,name,author,subject,year):
    result=''
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    
    if not edit:
        
        cur.execute(f"SELECT * FROM books")

        # Fetch all the rows returned by the query
        rows = cur.fetchall()

        # Print the results
        for row in rows:
            result+=str(row)+"\n"
    
    elif edit:
        
        if action=="add":

            newBook = True;
            cur.execute(f"SELECT name FROM books")
            library = cur.fetchall()
            for book in library:
                if book[0] == name:
                    result+="We have this book already in our library."
                    newBook = False
                    break
            if newBook:    
        
                cur.execute(f"INSERT INTO books (name,author,subject,year) VALUES ('{name}','{author}','{subject}','{year}')")
                conn.commit()
                cur.execute(f"SELECT * FROM books")

                # Fetch all the rows returned by the query
                rows = cur.fetchall()

                # Print the results
                for row in rows:
                    result+=str(row)+"\n"
        
        elif action=="remove":
                
                
                cur.execute(f"SELECT name FROM books")
                haveBook = False
                library = cur.fetchall()
                for book in library:
                    if str(book[0]) == name:
                        haveBook = True
                        break
                    
                if haveBook:
                
                    cur.execute(f"DELETE FROM books WHERE name='{name}'")
                    conn.commit()
                    cur.execute(f"SELECT * FROM books")

                    # Fetch all the rows returned by the query
                    rows = cur.fetchall()

                    # Print the results
                    for row in rows:
                        result+=str(row)+"\n"
                        
                else:
                 result+=f"We don't have this book in our library."
    
    conn.close()
    return result
    

#report_management description
'''
    The function starts by connecting to the SQLite database using the provided database_path and initializing a cursor.
It executes a SELECT query on the reports table to retrieve all reports with a "pending" status.
The function prints the results (each row) of the SELECT query.
If the edit parameter is True, indicating that the user wants to edit a report, the function proceeds with further actions.
It checks the validity of the inputted report_id by comparing it with the IDs and status in the reports table.
If the report_id is valid and the status is "pending," the function checks the provided action (either "accept" or "reject").
Depending on the action, the function updates the report's status in the reports table, records the admin who made the decision, and commits the changes to the database.
The function executes another SELECT query on the reports table and prints the updated results.
If the report_id is not valid or the status is not "pending," the function appends a message to the result indicating the issue.
Finally, the function closes the database connection and returns the formatted result.
'''
def report_management(edit,report_id,action,admin):
    
    result=''
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM reports WHERE status='pending'")

    # Fetch all the rows returned by the query
    rows = cur.fetchall()

    # Print the results
    for row in rows:
        result+=str(row)+"\n"
    
    if edit:
        
        cur.execute(f"SELECT id,status FROM reports")
        validID = False
        pending = False
        reports = cur.fetchall()
        for report in reports:
            if report[0] == report_id:
                validID = True
                if report[1] == "pending":
                    pending = True
                    
                else: result+=f"The status of this report (ID: {report_id}) has been determined earlier."
                break

        if validID:
            
            if pending:
            
                if action=="accept":
                    cur.execute(f"UPDATE reports SET admin='{admin}',status = 'accepted' WHERE id = {report_id}")
                elif action=="reject":
                    cur.execute(f"UPDATE reports SET admin='{admin}',status = 'rejected' WHERE id = {report_id}")
                conn.commit()  
            
                cur.execute(f"SELECT * FROM reports")
                # Fetch all the rows returned by the query
                rows = cur.fetchall()
                # Print the results
                for row in rows:
                    result+=str(row)+"\n"
                
        else:
            result+="Invalid ID!"
    
                
            
    
    conn.close()
    return result
    

#test_functions description
'''
    A testing function that evaluates the functionality of the other functions,
printing the results or errors encountered during the process.
'''
def test_functions():
    try:
        # Test weather_data
        weather_data_result = weather_data()
        if isinstance(weather_data_result, list):
            print("weather_data Results:")
            for line in weather_data_result:
                print(line)
        else:
            print(f"weather_data Error: {weather_data_result}")

        # Test book_management
        edit_books_result = book_management(edit=False, action="", name="", author="", subject="", year="")
        print("\nView Existing Books Results:")
        print(edit_books_result)

        add_book_result = book_management(edit=True, action="add", name="New Book", author="New Author", subject="New Subject", year="2022")
        print("\nAdd New Book Results:")
        print(add_book_result)

        remove_book_result = book_management(edit=True, action="remove", name="New Book", author="", subject="", year="")
        print("\nRemove Book Results:")
        print(remove_book_result)

        # Test report_management
        edit_reports_result = report_management(edit=False, report_id="", action="", admin="")
        print("\nView Pending Reports Results:")
        print(edit_reports_result)

        accept_report_result = report_management(edit=True, report_id=1, action="accept", admin="admin")
        print("\nAccept Report Results:")
        print(accept_report_result)

        reject_report_result = report_management(edit=True, report_id=2, action="reject", admin="admin")
        print("\nReject Report Results:")
        print(reject_report_result)

    except Exception as e:
        print(f"Test Error: {e}")
