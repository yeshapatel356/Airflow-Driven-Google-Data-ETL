import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
import pandas as pd
# Load environment variables from .env file
load_dotenv(".dotenv")

# Fetch API key from environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("Google API Key not found. Ensure that it's set in the .dotenv file.")

# Function to get geolocation from user input
def get_location(query):
    try:
        endpoint = 'https://maps.googleapis.com/maps/api/geocode/json?'
        params = {'address': query, 'key': API_KEY}
        response = requests.get(endpoint + urlencode(params))
        response.raise_for_status()  # Check for HTTP errors
        location_data = response.json()

        if location_data['status'] == 'OK':
            location = location_data['results'][0]['geometry']['location']
            return f"{location['lat']},{location['lng']}"
        else:
            print(f"Error: {location_data['status']}. Unable to get location.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

# Search for nearby restaurants
def search_restaurants(location, radius=1000):
    try:
        endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        params = {'location': location, 'radius': radius, 'type': 'restaurant', 'key': API_KEY}
        response = requests.get(endpoint + urlencode(params))
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

# Get detailed information including reviews
def get_place_details(place_id):
    try:
        endpoint = 'https://maps.googleapis.com/maps/api/place/details/json?'
        params = {'place_id': place_id, 'fields': 'name,rating,review,formatted_address', 'key': API_KEY}
        response = requests.get(endpoint + urlencode(params))
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

# Store restaurant data to CSV
def save_to_csv(restaurant_data, filename='restaurant_reviews.csv'):
    if restaurant_data:
        df = pd.DataFrame(restaurant_data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")
    

# Function to collect restaurant data and reviews
def collect_restaurant_data(user_input):
    location = get_location(user_input)
    
    if location:
        restaurants = search_restaurants(location)
        restaurant_data = []
        
        if restaurants and 'results' in restaurants:
            for restaurant in restaurants['results']:
                place_id = restaurant['place_id']
                details = get_place_details(place_id)
                
                if details and details['status'] == 'OK':
                    result = details['result']
                    reviews = result.get('reviews', [])
                    
                    for review in reviews:
                        restaurant_data.append({
                            'Name': result['name'],
                            'Address': result['formatted_address'],
                            'Rating': result['rating'],
                            'Review Author': review['author_name'],
                            'Review Text': review['text'],
                            'Review Rating': review['rating'],
                            'Relative Time': review['relative_time_description']
                        })
                    print(f"Details for {result['name']}:")
                    print(details)
                else:
                    print("Error fetching place details.")
        else:
            print("No restaurants found or error occurred.")
        
        if restaurant_data:
            save_to_csv(restaurant_data)
    else:
        print("Error: Location not found.")
        
# Main function
if __name__ == "__main__":
    try:
        user_input = input("Enter your query (e.g., Restaurants in Toronto): ")
        collect_restaurant_data(user_input)
    except Exception as e:
        print(f"An error occurred: {e}")