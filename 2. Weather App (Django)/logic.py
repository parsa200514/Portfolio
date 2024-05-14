'''
The Logic how the app works.
'''
import requests

"""
    Weather_Data is called in views.py
    Retrieves weather forecast data for the specified location using the Tomorrow.io API.

    Parameters:
    - location (str): The name of the location for which weather data is requested.

    Returns:
    - result (list): A list containing weather information, including location, date, average temperature, and humidity.
                    The first element is the location, and subsequent elements contain daily weather details for the next 5 days.
                    In case of errors or exceptions, appropriate messages are returned.

    Note:
    - The Tomorrow.io API key used for authentication is specified within the function.
    - The location parameter is expected as a string, and it is processed to replace spaces with '%20' for the API request.
    - The function handles successful API responses, HTTP errors (400), and general exceptions gracefully.
    - If the response status is 200 (OK), the function extracts and formats weather data for the next 5 days.

    Example:
    result = Weather_Data("New York")
    print(result)
    """
def Weather_Data(location):
    
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
