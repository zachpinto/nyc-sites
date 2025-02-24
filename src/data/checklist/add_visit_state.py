import json

# Load the sites.json file
with open("../../../data/processed/sites.json", "r", encoding="utf-8") as f:
    sites = json.load(f)

# Add "visited": "Not Visited" if missing
for site in sites:
    if "visited" not in site:
        site["visited"] = "Not Visited"

# Save the updated sites.json
with open("../../../data/processed/sites.json", "w", encoding="utf-8") as f:
    json.dump(sites, f, indent=2, ensure_ascii=False)

print("Updated sites.json with default 'Not Visited' status.")
