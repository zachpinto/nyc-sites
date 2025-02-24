import json
import time
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MapQuest API key from the environment
API_KEY = os.getenv("MAPQUEST_API_KEY")
if not API_KEY:
    raise ValueError("MAPQUEST_API_KEY not found in environment variables.")

SITES_JSON_PATH = "../../../data/processed/sites.json"

# Base URL for MapQuest Geocoding API
BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"


def geocode_address(address):
    """
    Given an address string, use MapQuest's API to return (lat, lng) tuple.
    Returns None if no result.
    """
    params = {
        "key": API_KEY,
        "location": address,
        "maxResults": 1  # We only need the top result
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        # Extract coordinates from the first location in the results
        locations = data.get("results", [])[0].get("locations", [])
        if not locations:
            print(f"No locations found for '{address}'")
            return None
        lat = locations[0]["latLng"]["lat"]
        lng = locations[0]["latLng"]["lng"]
        return (lat, lng)
    except Exception as e:
        print(f"Error geocoding '{address}': {e}")
        return None


def main():
    # Load the JSON file
    with open(SITES_JSON_PATH, "r", encoding="utf-8") as file:
        sites = json.load(file)

    updated_sites = []

    for site in sites:
        # If coordinates already exist, skip geocoding
        if "latitude" in site and "longitude" in site:
            updated_sites.append(site)
            continue

        address = site.get("location", "")
        if not address:
            updated_sites.append(site)
            continue

        # Use the MapQuest API to geocode the address
        result = geocode_address(address)
        if result:
            lat, lng = result
            site["latitude"] = lat
            site["longitude"] = lng
            print(f"Geocoded '{address}' => ({lat}, {lng})")
        else:
            print(f"Failed to geocode '{address}'")

        updated_sites.append(site)
        # Respect MapQuest's rate limit; delay at least 1 second per request
        time.sleep(1)

    # Save updated data back to sites.json
    with open(SITES_JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(updated_sites, file, indent=2)

    print("Pre-geocoding complete!")


if __name__ == "__main__":
    main()
