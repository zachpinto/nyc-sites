import json

# File path
sites_file = "../../../data/processed/sites.json"

# Load sites.json
with open(sites_file, "r", encoding="utf-8") as f:
    sites = json.load(f)

# Create a dictionary mapping names to their image URLs
image_lookup = {site["name"]: site["image"] for site in sites if site["image"]}

# Update missing images
updated_count = 0
for site in sites:
    if site["image"] == "" and site["name"] in image_lookup:
        site["image"] = image_lookup[site["name"]]
        updated_count += 1

# Save the updated JSON
with open(sites_file, "w", encoding="utf-8") as f:
    json.dump(sites, f, indent=2)

print(f"Updated {updated_count} missing images in {sites_file}")
