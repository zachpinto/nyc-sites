import os
import json
import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://museumhack.com/museums-in-nyc/"

# Output JSON file path (relative to this script)
OUTPUT_JSON_PATH = os.path.join("../..", "..", "data", "raw", "museums.json")

# Placeholder image URL since this source doesn't include proper images
PLACEHOLDER_IMAGE_URL = ""


def extract_museum_data(html_content):
    """
    Parse the HTML content and extract museum details.
    Returns a list of dictionaries with keys:
      - name
      - image (placeholder)
      - location
      - wikipedia_link (empty string for now)
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all blocks with the museum info (identified by class "mh-block")
    blocks = soup.find_all("div", class_="mh-block")
    museums = []

    for block in blocks:
        container = block.find("div", class_="container")
        if not container:
            continue

        # First column (col-sm-8) contains the museum name.
        details_col = container.find("div", class_="col-sm-8")
        if not details_col:
            continue

        h3 = details_col.find("h3")
        name = h3.get_text(strip=True) if h3 else ""

        # Use placeholder for image and empty for wikipedia_link
        image = PLACEHOLDER_IMAGE_URL
        wikipedia_link = ""

        location = ""
        side_col = container.find("div", class_="col-sm-4")
        if side_col:
            for ul in side_col.find_all("ul"):
                for li in ul.find_all("li"):
                    li_text = li.get_text(strip=True)
                    if "📍" in li_text:
                        span = li.find("span", class_="small")
                        if span:
                            location = span.get_text(strip=True)
                        else:
                            # Remove the location emoji if no span is found
                            location = li_text.replace("📍", "").strip()
                        # If we have found a location, break out of loops
                        break
                if location:
                    break

        museum = {
            "name": name,
            "image": image,
            "location": location,
            "wikipedia_link": wikipedia_link
        }
        museums.append(museum)

    return museums


def main():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        html_content = response.text
    except requests.RequestException as e:
        print(f"Error fetching data from {SOURCE_URL}: {e}")
        return

    museums = extract_museum_data(html_content)
    print(f"Found {len(museums)} museums.")

    # Ensure the output directory exists.
    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(museums, f, indent=4)
    print(f"Data saved to {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
