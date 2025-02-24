import json

# File paths
delete_file = "../../../data/future_development/delete_v1.txt"
json_file = "../../../data/processed/sites.json"

# Load the list of names to delete
with open(delete_file, "r", encoding="utf-8") as f:
    delete_names = set(line.strip() for line in f if line.strip())  # Remove empty lines

# Load the JSON data
with open(json_file, "r", encoding="utf-8") as f:
    sites = json.load(f)

# Filter out entries that match the deletion criteria
filtered_sites = [site for site in sites if not (site["name"] in delete_names and site.get("category") == "landmarks")]

# Save the updated JSON file
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(filtered_sites, f, indent=2)

print(f"Updated {json_file}: Removed entries from 'landmarks' category matching delete_v1.txt")
