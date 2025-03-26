import requests
import json
from datetime import datetime, timedelta

# GETTING THE TARIFF DATA

label = "552e906a5357a3435940adda"

# API Request to Get Utility Tariff Data
url = (
    "https://api.openei.org/utility_rates?"
    "api_key=zeJdwINd2qmx2RhRnrNH7e375hBFGfOCtwOVitgy"
    "&version=8"
    "&format=json"
    "&detail=full"
    f"&getpage={label}"
)

# Fetching Tariff Data
response = requests.get(url)
if response.ok:

    # SAVING THE DATA IN THE Second_Response FOR DEBUG PURPOSE
    data = response.json()
    with open("Second_Response.json", "w") as f:
        json.dump(data, f, indent=2)

else:
    print("Error fetching API:", response.status_code)
    print(response.text)
    exit(1)  # Stop execution if API CALL FAILS

# Extract energy schedules from the API response
try:
    energyweekdayschedule = data["items"][0].get("energyweekdayschedule", None)
    energyweekendschedule = data["items"][0].get("energyweekendschedule", None)
    energyratestructure = data["items"][0].get("energyratestructure", None)
    
    if energyweekdayschedule is None or energyweekendschedule is None or energyratestructure is None:
        print("Data Not Available for the Given Tariff")
        exit(1)


    flatdemandstructure = data["items"][0].get("flatdemandstructure",[])
    # Extract all available rates safely

    flatdemand_rates = [ tier[0].get("rate", 0) if tier and isinstance(tier[0], dict) else 0
    for tier in flatdemandstructure ]

    highest_rate = max(flatdemand_rates, default="Flat Demand Structure Not Available Use the Default Value !!!")
    print(highest_rate)

    # Extract tariff rates dynamically, including adjustment if available
    tariff_rates = [ tier[0]["rate"] + tier[0].get("adj", 0)  # Add "adj" if it exists, otherwise use 0
    for tier in energyratestructure ]

except KeyError as e:
    print(f"Error: Missing key in API response - {e}")
    exit(1)  # Stop execution if required data is missing

# Generating the 525,600-minute Tariff List
start_time = datetime(2025, 1, 1, 0, 0)  # Start of the year
end_time = datetime(2025, 12, 31, 23, 59)  # End of the year

minute_tariff_list = []

current_time = start_time
while current_time <= end_time:
    month_index = current_time.month - 1  # Months are 1-indexed
    hour = current_time.hour
    weekday = current_time.weekday()  # Monday = 0, Sunday = 6

    # Choose correct schedule based on weekend or weekday
    schedule = energyweekdayschedule if weekday < 5 else energyweekendschedule

    # Prevent IndexError with safety checks
    if 0 <= month_index < len(schedule) and 0 <= hour < len(schedule[month_index]):
        tariff_index = schedule[month_index][hour]
        if 0 <= tariff_index < len(tariff_rates):  # Ensure valid index
            minute_tariff_list.append(tariff_rates[tariff_index])
        else:
            print(f"Warning: Invalid tariff index {tariff_index} at {current_time}")
            minute_tariff_list.append(0)  # Default to 0 if invalid
    else:
        print(f"Error: Invalid month_index={month_index} or hour={hour}")
        minute_tariff_list.append(0)  # Default value in case of error

    current_time += timedelta(minutes=1)  # Move to the next minute

# Save the list to a file
with open("minute_tariff_list.json", "w") as f:
    json.dump(minute_tariff_list, f)

print("Successfully generated the 525,600-minute tariff list using real data.")
