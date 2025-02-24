import os
import json
import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_tallest_buildings_in_New_York_City#"
OUTPUT_JSON_PATH = os.path.join("../..", "..", "data", "raw", "skyscrapers.json")

def scrape_tallest_buildings(url):
    """
    Scrapes the table of tallest buildings from the given Wikipedia URL.
    Returns a list of dicts with:
      - name
      - image (wiki /wiki/File:... link)
      - location (the building's address + " New York, NY")
      - wikipedia_link (the building's own wiki page)
    """
    print(f"Scraping: {url}")
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", class_="wikitable sortable")

    records = []

    for table in tables:
        # Each row in the table is <tr>. The first row might be headers, so we'll skip if <th> is found.
        rows = table.find_all("tr")
        for row in rows:
            tds = row.find_all("td", recursive=False)
            # We expect at least 7 columns, in order:
            #   [0]: rank
            #   [1]: name
            #   [2]: image
            #   [3]: height
            #   [4]: floors
            #   [5]: year
            #   [6]: address/location
            if len(tds) < 7:
                continue

            # --- 1) NAME & WIKIPEDIA LINK from tds[1] ---
            name_col = tds[1]
            name_anchor = name_col.find("a", href=True)
            if not name_anchor:
                # If we can't find an anchor for the name, skip
                continue

            name = name_anchor.get_text(strip=True)
            wikipedia_link = "https://en.wikipedia.org" + name_anchor["href"]

            # --- 2) IMAGE from tds[2] (may not exist) ---
            image_col = tds[2]
            image_anchor = image_col.find("a", href=True)
            image_url = ""
            if image_anchor and image_anchor["href"].startswith("/wiki/File:"):
                # e.g. "/wiki/File:New_York_(33224081040).jpg"
                image_url = "https://en.wikipedia.org" + image_anchor["href"]

            # --- 3) LOCATION from tds[6] + " New York, NY" ---
            location_col = tds[6]
            address_text = location_col.get_text(" ", strip=True)  # e.g. "285 Fulton Street"
            # Some cells may contain links or extra text, so we just grab the text content.
            # Then we append " New York, NY"
            location = f"{address_text} New York, NY"

            # Build the record
            record = {
                "name": name,
                "image": image_url,
                "location": location,
                "wikipedia_link": wikipedia_link
            }
            records.append(record)

    return records

def main():
    # Scrape the data
    buildings = scrape_tallest_buildings(URL)
    print(f"Found {len(buildings)} building entries.")

    # Save to JSON
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(buildings, f, indent=4)
    print(f"Data saved to {OUTPUT_JSON_PATH}")

if __name__ == "__main__":
    main()
