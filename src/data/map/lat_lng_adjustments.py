import json
from collections import defaultdict

# File path
sites_file = "../../../data/processed/sites.json"

# Load JSON data
with open(sites_file, "r", encoding="utf-8") as f:
    sites = json.load(f)

# Step 1: Find duplicate coordinates
coord_groups = defaultdict(list)

for site in sites:
    key = (site["latitude"], site["longitude"])
    coord_groups[key].append(site)

# Step 2: Adjust coordinates for duplicates
adjustment_step = 0.00005  # Small shift per entry
updated_count = 0

for (lat, lng), group in coord_groups.items():
    if len(group) > 1:
        print(f"Adjusting {len(group)} entries at ({lat}, {lng})")

        # Apply small shifts to all but the first entry
        for i, site in enumerate(group[1:], start=1):
            site["longitude"] = round(lng + ((i * adjustment_step) if i % 2 == 0 else -(i * adjustment_step)), 6)
            updated_count += 1

# Step 3: Save updated JSON
with open(sites_file, "w", encoding="utf-8") as f:
    json.dump(sites, f, indent=2)

print(f"🎉 Adjusted {updated_count} overlapping coordinates.")
