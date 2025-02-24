import os
import json
import requests
from bs4 import BeautifulSoup

# The page to scrape
SOURCE_URL = (
    "https://en.wikipedia.org/wiki/"
    "List_of_National_Historic_Landmarks_in_New_York_City"
    "#National_Historic_Landmarks_in_New_York_City"
)

# Where to save the scraped JSON data
OUTPUT_JSON_PATH = os.path.join("../..", "..", "data", "raw", "national_historic_landmarks.json")


def extract_landmarks(html_content):
    """
    Parses the HTML content of the Wikipedia page for
    National Historic Landmarks in NYC.

    Returns a list of dicts with:
      - name
      - image
      - location (string, e.g. "40°44′30″N 73°59′01″W")
      - wikipedia_link (string)
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Each landmark is in a <tr class="vcard"> row
    rows = soup.find_all("tr", class_="vcard")

    results = []

    for row in rows:
        # Each row has:
        #   <th> (the #),
        #   <td> (name), <td> (image), <td> (date), <td> (location coords), ...
        tds = row.find_all("td", recursive=False)
        # We expect at least 5 <td> elements.
        # (0:name, 1:image, 2:date, 3:location, 4:... possibly county)
        if len(tds) < 4:
            # if the row doesn't have enough cells, skip
            continue

        # 1) Name: in the first <td> => tds[0].
        #    <a href="/wiki/69th_Regiment_Armory">69th Regiment Armory</a>
        name_td = tds[0]
        name_a = name_td.find("a")
        if not name_a:
            # skip if we can't find the anchor
            continue
        name = name_a.get_text(strip=True)

        # 2) Wikipedia link for the name
        wikipedia_link = (
                "https://en.wikipedia.org/wiki/" + name.replace(" ", "_")
        )

        # 3) Image: in the second <td> => tds[1].
        image_td = tds[1]
        image_a = image_td.find("a")
        if image_a and image_a.get("href", "").startswith("/wiki/File:"):
            image_url = "https://en.wikipedia.org" + image_a["href"]
        else:
            # fallback or skip if not found
            image_url = ""

        # 4) Location: in the fourth <td> => tds[3].
        location_td = tds[3]

        # Attempt to find a "geo-dms" span
        dms_span = location_td.find("span", class_="geo-dms")
        if dms_span:
            location = dms_span.get_text(" ", strip=True)
            # e.g. "40°44′30″N 73°59′01″W"
        else:
            # If no .geo-dms, try .geo-dec or just get the text
            dec_span = location_td.find("span", class_="geo-dec")
            if dec_span:
                location = dec_span.get_text(" ", strip=True)
            else:
                # fallback to the entire cell text, might be messy
                location = location_td.get_text(" ", strip=True)

        results.append({
            "name": name,
            "image": image_url,
            "location": location,
            "wikipedia_link": wikipedia_link
        })

    return results


def main():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        html_content = response.text
    except requests.RequestException as e:
        print(f"Error fetching data from {SOURCE_URL}: {e}")
        return

    landmarks = extract_landmarks(html_content)
    print(f"Found {len(landmarks)} landmarks.")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)

    # Write out the JSON
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(landmarks, f, indent=4)

    print(f"Data saved to {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
