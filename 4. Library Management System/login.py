#This file is designed for login/signup panel logic

import sqlite3
import hashlib

database_path = 'app/database.db'


#signup description
'''
    The function starts by connecting to the SQLite database using the provided database_path and initializing a cursor.
It checks the availability of the provided username by executing a SELECT query on the users table to retrieve all usernames.
If the provided username is already taken, the function sets username_availability to False and returns a message indicating that the username is already taken.
If the username is available, the function proceeds to hash the provided password securely. It uses a combination of SHA-256 hashing and salting for added security.
The hashed password is then inserted into the users table along with the username and role.
If the user's role is "student," an additional record is inserted into the students table with the provided username.
The changes are committed to the database.
The function returns a success message if the sign-up process is completed successfully.
Finally, the function closes the database connection and resets the password variable to an empty string before returning the result.
'''
def signup(username,password,role):    
    result=''
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    
    username_availability = True
    cur.execute(f"SELECT username FROM users")
    taken_usernames = cur.fetchall()
    for taken_username in taken_usernames:
        if taken_username[0] == username:
            result = ("Username already taken.")
            username_availability = False
            break
        
    if username_availability: 
        hash_sha256 = hashlib.sha256()
        salt = "E>chaI_KarAk<3"
        password = salt+password+salt
        hash_sha256.update(bytes(password,'utf-8'))
        first_hash = hash_sha256.hexdigest()
        hash_sha256.update(bytes(first_hash,'utf-8'))
        password = hash_sha256.hexdigest()
    
        cur.execute(f"INSERT INTO users (username,password,role) VALUES ('{username}','{password}','{role}')")
        if role == "student":
            cur.execute(f"INSERT INTO students (username) VALUES ('{username}')")
        conn.commit()
        result = "Signed up Successfuly!"
    

    conn.close()
    password=""
    return result
    

#login description
'''
    The function starts by hashing the provided password securely using SHA-256 and salting.
It connects to the SQLite database using the provided database_path and initializes a cursor.
The function executes a SELECT query on the users table to retrieve usernames and passwords based on the provided role.
It iterates through the retrieved rows to check if the provided username exists.
If the username exists, it compares the hashed password from the database with the hashed password provided during login.
If the passwords match, the function returns a welcome message. If the passwords do not match, it returns an "Incorrect Password!" message.
If the username does not exist, the function returns a "User not found." message.
Finally, the function closes the database connection and returns the result.
'''
def login(username,password,role):
    result=''
    
    hash_sha256 = hashlib.sha256()
    salt = "E>chaI_KarAk<3"
    password = salt+password+salt
    hash_sha256.update(bytes(password,'utf-8'))
    first_hash = hash_sha256.hexdigest()
    hash_sha256.update(bytes(first_hash,'utf-8'))
    password = hash_sha256.hexdigest()


    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    cur.execute(f"SELECT username,password FROM users WHERE role='{role}'")

    res = cur.fetchall()
    
    username_existence=False
    for row in res:
        if row[0] == username:
            username_existence=True
            if row[1] == password:
                result = f"Welcome! {username}"
            else :
                result = "Incorrect Password!"
            break    
    
    if not username_existence:
        result = "User not found."
        
    conn.close()
    return result


#test_functions description
'''
    A testing function that evaluates the functionality of the other functions,
printing the results or errors encountered during the process.
'''
def test_functions():
    try:
        # Test signup
        signup_result = signup(username="test_user", password="test_password", role="student")
        print("Signup Result:")
        print(signup_result)

        # Test login
        login_result_correct = login(username="test_user", password="test_password", role="student")
        login_result_incorrect = login(username="test_user", password="incorrect_password", role="student")
        login_result_not_found = login(username="nonexistent_user", password="test_password", role="student")

        print("\nLogin Results:")
        print("Correct Password:", login_result_correct)
        print("Incorrect Password:", login_result_incorrect)
        print("User Not Found:", login_result_not_found)

    except Exception as e:
        print(f"Test Error: {e}")
