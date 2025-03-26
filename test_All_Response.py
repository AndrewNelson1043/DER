
## FIRST API TO CALL ALL THE RELATED TARIFFS

import requests
import json

# DEFINE THE VARIABLES

# API KEY 
api_key = "vmbWXI9uCmhdEUcjZJ8GhcPWM5PQEKk6PCxkJNae"

# LATITUDE AND LONGITUDE FROM THE GOOGLE MAP LOCATION
lat =   	35.419872
lon =      -79.469442
# SELECT THE SECTORS FROM THE 4 GIVEN 
sector = "Commercial"  # Residential, Commercial, Industrial, or Lighting

# USE THE ADDRESS IF USING THE GOOGLE ENCODING API
#address = "37.77493,-122.419415"

# Construct URL using variables
url = (
    f"https://api.openei.org/utility_rates?"
    f"version=7"
    f"&format=json"
    f"&api_key={api_key}"
    f"&lat={lat}"
    f"&lon={lon}"
    f"&sector={sector}"
    f"&direction=asc"
)


response = requests.get(url)

if response.ok:
    data = response.json()
    # print("Retrieved utility rate data:")
    # print(data)
    # Save the JSON data into a file called response.json
    with open("Test_All_Response.json", "w") as f:
        json.dump(data, f, indent=2)
        print("Tariff Data saved to Test_All_Response.json !!!")
else:
    print("Error:", response.text)