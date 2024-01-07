#This file is designed for student panel logic

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


#recommended_books description
'''
    The function starts by connecting to an SQLite database using the provided database_path and executing a SELECT query to retrieve the user's current book recommendations from the database.
If the user's current recommendations match their current MBTI, major, and favorite genre, the function returns the existing recommendations without further processing.
If the user's current recommendations do not match, the function initializes a dictionary (data) mapping book genres to corresponding criteria (MBTI, major, favorite). It then creates an empty list (recommended_keys) to store genres that match the user's input criteria.
The function iterates through the dictionary and appends genres to recommended_keys based on the user's MBTI, major, and favorite genre.
The function assigns weights to the genres in best_keys based on the matching criteria. The higher the weight, the more criteria match.
It sorts the genres in descending order of weight and retrieves book names from the database for each recommended genre.
The function updates the user's information in the database with the latest MBTI, major, favorite genre, and new recommendations.
Finally, it returns a string containing the recommended book names.
'''
def recommended_books(username,mbti,major,favorite):
    result=''
    
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    cur.execute(f"SELECT mbti,major,favorite,recommended FROM students WHERE username='{username}'")
    informations = cur.fetchall()
    if (informations[0][0] == mbti)and(informations[0][1] == major)and(informations[0][2] == favorite):
        conn.close()
        return informations[0][3]
    

    data = {
        "Mystery/Thriller": ["ISTJ", "ESTJ", "Law", "Computer Science", "Psychology", "Sociology"],
        "Science Fiction": ["INTP", "ENTP", "Physics", "Computer Science", "Engineering", "Mathematics"],
        "Fantasy": ["ISFP", "ESFP", "Art History", "English Literature"],
        "Historical Fiction": ["INFJ", "ENFJ", "History", "English Literature"],
        "Romance": ["INFP", "ENFP", "Psychology", "English Literature", "Sociology"],
        "Action/Adventure": ["ISTP", "ESTP", "Engineering", "Computer Science", "Physics"],
        "Non-Fiction": ["INTJ", "ENTJ", "History", "Business Administration", "Economics", "Law"],
        "Biography/Autobiography": ["ISFJ", "ESFJ", "Psychology", "Sociology", "Education"],
        "Dystopian": ["ENFP", "ENTP", "Sociology", "Political Science"],
        "Literary Fiction": ["INFJ", "INTJ", "English Literature", "Psychology", "Sociology"]
    }
    
    recommended_keys=[]

    for key, value in data.items():
        if favorite == key:
            recommended_keys.append(key)
        if mbti in value:
            recommended_keys.append(key)
        if major in value:
            recommended_keys.append(key)
        

    recommended_keys = set(recommended_keys)
    best_keys={}

    for key, value in data.items():
        if key in recommended_keys:
            if (mbti in value) and (major in value) and (key==favorite):
               best_keys.update({key : 5}) 
            elif (key==favorite) and ((mbti in value) or (major in value)):
               best_keys.update({key : 4}) 
            elif key==favorite:
               best_keys.update({key : 3}) 
            elif (mbti in value) and (major in value):
               best_keys.update({key : 2}) 
            else:
               best_keys.update({key : 1}) 
               
    sorted_keys_by_values = sorted(best_keys, key=lambda k: best_keys[k], reverse=True)
    
    
    for i in range (0,len(sorted_keys_by_values)):
        cur.execute(f"SELECT name FROM books WHERE subject='{sorted_keys_by_values[i]}'")

        # Fetch all the rows returned by the query
        rows = cur.fetchall()
        

        for row in rows:
            result+=row[0]+"\n"
            
    cur.execute(f"UPDATE students SET mbti='{mbti}',major = '{major}',favorite = '{favorite}',recommended = '{result}' WHERE username = '{username}'")
    conn.commit()
            
    
        
    conn.close()
    return result


#book_order description
'''
    The function starts by connecting to an SQLite database using the provided database_path and initializing a cursor.
If the borrow parameter is False, indicating that the user wants to view available books, the function executes a SELECT query to retrieve all books from the books table. It then formats the result into a string and returns it.
If the borrow parameter is True, indicating that the user wants to borrow a book, the function checks if the requested book exists in the library by executing a SELECT query on the books table. If the book exists, the function inserts a new record into the reports table with the student's information, the book's name, and a status of 'pending'. It then retrieves all records from the reports table and formats the result into a string.
If the requested book doesn't exist in the library, the function adds a message to the result string indicating that the book is not available.
Finally, the function closes the database connection and returns the result.
'''
def book_order(student,borrow,name):
    result=''
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    
    if not borrow:
        cur.execute(f"SELECT * FROM books")

        # Fetch all the rows returned by the query
        rows = cur.fetchall()

        # Print the results
        for row in rows:
            result+=row
            
        
        conn.close()
        return result
    
    elif borrow:
                
        cur.execute(f"SELECT name FROM books")
        haveBook = False
        library = cur.fetchall()
        for book in library:
            if book[0] == name:
                haveBook = True
                break
            
                    
        if haveBook:
                
            cur.execute(f"INSERT INTO reports (book,student,status) VALUES ('{name}','{student}','pending')")
            conn.commit()
            cur.execute(f"SELECT * FROM reports")

            # Fetch all the rows returned by the query
            rows = cur.fetchall()

            # Print the results
            for row in rows:
                result+=row
                
        
                        
        else:
            result+=f"We don't have this book in our library."
            
        
        conn.close()
        return result
    

#reports_check description
'''
    The function starts by connecting to the SQLite database using the provided database_path and initializing a cursor.
It executes a SELECT query on the reports table to retrieve all records associated with the specified student.
The function fetches all rows returned by the query and formats the result into a string.
Finally, it closes the database connection and returns the formatted result.
'''
def reports_check(student):
    result=''
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM reports WHERE student={student}")

    # Fetch all the rows returned by the query
    rows = cur.fetchall()

    # Print the results
    for row in rows:
        result+=row
    
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

        # Test recommended_books
        username = "test_user"
        mbti = "ISTJ"
        major = "Law"
        favorite_genre = "Mystery/Thriller"
        recommended_books_result = recommended_books(username, mbti, major, favorite_genre)
        print("\nrecommended_books Results:")
        print(recommended_books_result)

        # Test book_order
        student_name = "test_student"
        borrow_book_name = "Sample Book"
        borrow_result = book_order(student_name, borrow=True, name=borrow_book_name)
        print("\nbook_order Results:")
        print(borrow_result)

        # Test reports_check
        reports_check_result = reports_check(student_name)
        print("\nreports_check Results:")
        print(reports_check_result)

    except Exception as e:
        print(f"Test Error: {e}")
    
    

        
    
        
    
