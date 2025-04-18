import requests
import json
import re

# DEFINE THE VARIABLES
api_key = "vmbWXI9uCmhdEUcjZJ8GhcPWM5PQEKk6PCxkJNae"
lat = 35.782169
lon = -80.793457
sector = "Commercial"

# Construct URL
url = (
    f"https://api.openei.org/utility_rates?"
    f"version=7&format=json&api_key={api_key}"
    f"&lat={lat}&lon={lon}&sector={sector}&direction=asc"
)

# Send Request
response = requests.get(url)

# Handle response
if response.ok:
    try:
        data = response.json()
        with open("Test_All_Response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("✅ Tariff data saved to Test_All_Response.json")
    except json.JSONDecodeError:
        print("⚠️ JSON decode failed. Trying to clean and re-parse...")

        # Try cleaning control characters from the text
        clean_text = re.sub(r'[\x00-\x1F\x7F]', '', response.text)
        try:
            data = json.loads(clean_text)
            with open("Test_All_Response.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("✅ Cleaned and saved to Test_All_Response.json")
        except json.JSONDecodeError as e2:
            print("❌ Still failed to parse JSON. Saving raw text for review.")
            with open("Test_All_Response_RAW.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("📝 Raw response saved to Test_All_Response_RAW.txt")
else:
    print("❌ Request failed with status code:", response.status_code)
    print("Response text preview:", response.text[:1000])
