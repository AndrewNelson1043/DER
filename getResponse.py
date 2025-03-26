import requests
import json

# Function to validate latitude and longitude
def validate_coordinates(lat, lon):
    if lat < -90 or lat > 90:
        raise ValueError(f"Invalid coordinates: latitude of {lat} must be between -90 and 90 degrees.")
    if lon < -180 or lon > 180:
        raise ValueError(f"Invalid coordinates: longitude of {lon} must be between -180 and 180 degrees.")

# DEFINE THE VARIABLES

# API KEY 
api_key = "vmbWXI9uCmhdEUcjZJ8GhcPWM5PQEKk6PCxkJNae"

# LATITUDE AND LONGITUDE FROM THE GOOGLE MAP LOCATION
lat =   	35.419872
lon =      -79.469442

# Validate coordinates
validate_coordinates(lat, lon)
# SELECT THE SECTORS FROM THE 4 GIVEN 
sector = "Commercial"  # Residential, Commercial, Industrial, or Lighting

# ORDER OF THE DATA
order = "asc"

# Construct URL using variables
url = (
    f"https://api.openei.org/utility_rates?"
    f"version=8"
    f"&format=json"
    f"&api_key={api_key}"
    f"&lat={lat}"
    f"&lon={lon}"
    f"&sector={sector}"
    f"&order ={order}"
)

# MAKE THE API REQUEST
response = requests.get(url)

# CHECK THE RESPONSE 
if response.ok:
    data = response.json()

    # Check FOR THE ERRORS IN THE RESPONSE
    if "errors" in data and data["errors"]:
        print("API Error:", data["errors"])
        error_response = {"items": [], "errors": data["errors"]}
        
        # SAVE THE ERROR RESPONSE IN THE JSON FILE
        with open("First_Response.json", "w") as f:
            json.dump(error_response, f, indent=2)

        print("Error response saved to First_Response.json !!!")
        exit(1)  # STOP THE EXECUTION

    # CHECK IF THE RESPONSE CONTAIN THE TARIFF DATA
    if "items" not in data or not data["items"]:
        print("No tariff data available for the given parameters.")
        empty_response = {"items": [], "errors": ["No tariff data available for the given location !!!"]}
        
        # Save empty response to a JSON file
        with open("First_Response.json", "w") as f:
            json.dump(empty_response, f, indent=2)

        print("Empty response saved to First_Response.json !!!")
        exit(1)

    unique_tariffs = {}

    # item is a DICT

    for item in data["items"]:
        utility = item.get("utility", "Unknown Utility")
        name = item.get("name", "Unknown Name")
        enddate = item.get("enddate", None)  # Can be None

        # Create a unique key based on utility and name
        key = (utility, name)

        # If the tariff has no enddate, treat it as the latest, or if it's the first for this key
        if key in unique_tariffs:
            del unique_tariffs[key]
            unique_tariffs[key] = item  # Store the no-enddate tariff
        else:
            # If there's no existing tariff OR the new tariff has a later enddate, update it
            existing_tariff = unique_tariffs.get(key, None)
            if not existing_tariff or (existing_tariff.get("enddate") and existing_tariff["enddate"] < enddate):
                unique_tariffs[key] = item

    # Convert the dictionary values to a list
    latest_tariffs = list(unique_tariffs.values())

    # Save the filtered data to a new JSON file
    with open("First_Response.json", "w") as f:
        json.dump({"items": latest_tariffs}, f, indent=2)

    print("Latest tariff data saved to First_Response.json !!!")

else:
    print("Error fetching API:", response.status_code)
    error_response = {"items": [], "errors": [response.text]}

    # Save API error response to a JSON file
    with open("First_Response.json", "w") as f:
        json.dump(error_response, f, indent=2)

    print("API error response saved to First_Response.json !!!")
