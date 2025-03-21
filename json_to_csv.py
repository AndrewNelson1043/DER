import json
import csv

def json_to_csv(json_filename, csv_filename):
    """Convert a JSON file to a CSV file and count the rows."""
    try:
        with open(json_filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_filename} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: {json_filename} is not a valid JSON file.")
        return

    # Ensure data contains items
    if "items" not in data or not isinstance(data["items"], list) or not data["items"]:
        print(f"No valid data found in {json_filename} to convert to CSV.")
        return

    # Collect all possible keys dynamically
    all_keys = set()
    for item in data["items"]:
        all_keys.update(item.keys())

    # Convert set to sorted list for consistent column order
    fieldnames = sorted(all_keys)

    # Write to CSV file
    row_count = 0
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Fill missing fields with empty values and count rows
        for item in data["items"]:
            writer.writerow({key: item.get(key, "") for key in fieldnames})
            row_count += 1  # Count rows written

    print(f"CSV file '{csv_filename}' has been created successfully with {row_count} rows!")

# Convert both JSON files to CSV
json_to_csv("First_Response.json", "First_Response.csv")
json_to_csv("Test_All_Response.json", "Test_All_Response.csv")
json_to_csv("Second_Response.json", "Second_Response.csv")
