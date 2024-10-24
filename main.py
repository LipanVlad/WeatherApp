import requests
import time
import sys

# OpenWeatherMap API Key
API_KEY = "fdc49f8b5ddd924243144c5f03becf72"
RESULT_LIMIT = 5

def get_user_input():
    print("Country name (ISO code): ", end="")
    country = input().strip()
    print("City name: ", end="")
    city = input().strip()
    return country, city

def fetch_geocode_data(city):
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={RESULT_LIMIT}&appid={API_KEY}"
    response = requests.get(geocode_url)
    return response.json()

# Makes sure that the user inputs a valid city. If not the user can retry or exit the program.
def validate_city(city, country):
    geocode_data = fetch_geocode_data(city)
    
    while not geocode_data:
        print(f"{city} does not exist. Please input a valid city name (or type 'exit' to quit): ", end="")
        city = input().strip()
        if city.lower() == "exit":
            sys.exit("Program exited.")
        geocode_data = fetch_geocode_data(city)

    return geocode_data, city

# Checks if the city is part of the provided country
def validate_country(geocode_data, country, city):
    while True:
        for result in geocode_data:
            if result["country"].lower() == country.lower():
                return country

        print(f"The city {city} is not in {country}. Please input the correct country (or type 'exit' to quit): ", end="")
        country = input().strip()
        if country.lower() == "exit":
            sys.exit("Program exited.")

# Gets the coordinates for an inputed city and country.
def get_coordinates(city, country):
    geocode_data = fetch_geocode_data(city)

    # Validate city and country if no data is found initially
    if not geocode_data:
        geocode_data, city = validate_city(city, country)
    
    country = validate_country(geocode_data, country, city)

    for result in geocode_data:
        if result["country"].lower() == country.lower():
            return (result["lat"], result["lon"]), city

    raise ValueError("Could not find valid coordinates.")

# Gets and displays the weather information for the provided city.
def fetch_weather_data(lat, lon, city):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=en"
    response = requests.get(weather_url)
    weather_data = response.json()

    # Extract sunrise and sunset times in a readable format
    sunrise_time = time.strftime("%H:%M", time.localtime(weather_data["sys"]["sunrise"]))
    sunset_time = time.strftime("%H:%M", time.localtime(weather_data["sys"]["sunset"]))

    print()
    print(f"In {city}, the temperature is: {weather_data['main']['temp']}°C")
    print(f"Weather: {weather_data['weather'][0]['description']}")
    print(f"Humidity: {weather_data['main']['humidity']}%")
    print(f"Sunrise: {sunrise_time} | Sunset: {sunset_time}")

def main():
    country, city = get_user_input()
    coordinates, city = get_coordinates(city, country)
    lat, lon = coordinates
    fetch_weather_data(lat, lon, city)

if __name__ == "__main__":
    main()