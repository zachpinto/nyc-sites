import json

# Load the JSON file
with open("../../../data/processed/sites.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Process each entry
for entry in data:
    if entry.get("location") == "New York, NY":
        entry["location"] = f'{entry["name"]}, New York, NY'

# Save the updated JSON
with open("../../../data/processed/sites.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)

print("Update complete! Locations updated where necessary.")
