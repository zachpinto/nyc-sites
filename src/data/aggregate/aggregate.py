import json
import os

def main():
    # 1) Define the mapping of filenames to categories
    file_category_map = {
        "designated_landmarks.json": "landmarks",
        "libraries.json": "libraries",
        "museums.json": "museums",
        "national_historic_landmarks.json": "landmarks",
        "national_monuments.json": "monuments",
        "national_register_historical_places.json": "historical places",
        "performing_arts.json": "performing arts",
        "tourist_attractions.json": "tourist attractions",
        "zoos_gardens.json": "zoos and gardens"
    }

    # 2) Paths to raw data and processed data
    raw_dir = os.path.join("..", "..", "..", "data", "raw")
    processed_dir = os.path.join("..", "..", "..", "data", "processed")
    output_file = os.path.join(processed_dir, "sites.json")

    # Ensure processed_dir exists
    os.makedirs(processed_dir, exist_ok=True)

    # 3) Accumulate data in a single list
    all_sites = []

    for filename, category in file_category_map.items():
        filepath = os.path.join(raw_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    # data is expected to be a list of site entries
                    for entry in data:
                        # Build a new entry that ensures we have
                        # the five expected keys: name, image, location, wikipedia_link, category
                        new_entry = {
                            "name": entry.get("name", "Unknown"),
                            "image": entry.get("image", ""),  # or None
                            "location": entry.get("location", ""),  # can be address or lat/lon
                            "wikipedia_link": entry.get("wikipedia_link", ""),
                            "category": category
                        }

                        # Append to the master list
                        all_sites.append(new_entry)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON from file {filepath}. Skipping.")
        else:
            print(f"Warning: {filepath} not found. Skipping.")

    # 4) Write the aggregated sites to sites.json
    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(all_sites, out, indent=2, ensure_ascii=False)

    print(f"Aggregated {len(all_sites)} entries into {output_file}")

if __name__ == "__main__":
    main()
