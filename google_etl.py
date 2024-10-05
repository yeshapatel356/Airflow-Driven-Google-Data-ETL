import pandas as pd
import json 
import requests
from datetime import datetime
import s3fs
from dotenv import load_dotenv
import os

import requests

# Load environment variables from .env file
load_dotenv(".dotenv")

def geocode(address):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print("Geocoding failed:", data['status'])
        return None

# Usage example
address = "1600 Pennsylvania Ave NW, Washington, DC"
latitude, longitude = geocode(address)
print(latitude, longitude)