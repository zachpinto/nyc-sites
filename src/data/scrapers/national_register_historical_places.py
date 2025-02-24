import os
import json
import requests
from bs4 import BeautifulSoup

# List of Wikipedia pages that share the same row format:
WIKI_PAGES = [
    "https://en.wikipedia.org/wiki/National_Register_of_Historic_Places_listings_in_Manhattan_below_14th_Street",
    "https://en.wikipedia.org/wiki/National_Register_of_Historic_Places_listings_in_Manhattan_from_14th_to_59th_Streets",
    "https://en.wikipedia.org/wiki/National_Register_of_Historic_Places_listings_in_Manhattan_from_59th_to_110th_Streets",
    "https://en.wikipedia.org/wiki/National_Register_of_Historic_Places_listings_in_Manhattan_above_110th_Street",
    "https://en.wikipedia.org/wiki/National_Register_of_Historic_Places_listings_in_Manhattan_on_islands",
    "https://en.wikipedia.org/wiki/National_Register_of_Historic_Places_listings_in_the_Bronx",
    "https://en.wikipedia.org/wiki/National_Register_of_Historic_Places_listings_in_Brooklyn",
    "https://en.wikipedia.org/wiki/National_Register_of_Historic_Places_listings_in_Queens,_New_York",
    "https://en.wikipedia.org/wiki/National_Register_of_Historic_Places_listings_in_Staten_Island"
]

# Output file: we will APPEND or REWRITE to this JSON
OUTPUT_JSON_PATH = os.path.join("../..", "..", "data", "raw", "national_register_historical_places.json")


def parse_wikipedia_page(url):
    """
    Given the URL to a Wikipedia page with <tr class='vcard'> rows,
    extract a list of items:
      - name
      - image (constructed link)
      - location
      - wikipedia_link (constructed from name)
    Returns a list of dicts.
    """
    print(f"Scraping: {url}")
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # We'll parse out the base page name to construct the #/media link
    base_page = url.split("/wiki/")[-1]
    # Remove any fragment (the '#' part)
    if "#" in base_page:
        base_page = base_page.split("#", 1)[0]

    # Each entry is in <tr class="vcard">
    rows = soup.find_all("tr", class_="vcard")

    records = []
    for row in rows:
        tds = row.find_all("td", recursive=False)
        # We expect at least 4 <td> cells: name (0), image (1), date(2), location(3)
        if len(tds) < 4:
            continue

        # 1) Name from tds[0]
        name_td = tds[0]
        a_tag = name_td.find("a")
        if not a_tag:
            # If we can't find a link, skip
            continue

        name = a_tag.get_text(strip=True)

        # 2) Construct the wikipedia_link from the displayed name
        wikipedia_link = "https://en.wikipedia.org/wiki/" + name.replace(" ", "_")

        # 3) Image from tds[1]. The <a href="/wiki/File:someimage.jpg"> tag.
        image_td = tds[1]
        image_a = image_td.find("a")
        if image_a and "href" in image_a.attrs:
            file_href = image_a["href"]  # e.g. "/wiki/File:75-murray-st.jpg"
            if file_href.startswith("/wiki/File:"):
                relative_file = file_href.split("/wiki/")[-1]  # "File:75-murray-st.jpg"
                # Now build the final
                image_url = f"https://en.wikipedia.org/wiki/{base_page}#/media/{relative_file}"
            else:
                # If for some reason it's not a File: link, fallback or set blank
                image_url = ""
        else:
            image_url = ""

        # 4) Location from tds[3].
        location_td = tds[3]
        location_text = []

        label_span = location_td.find("span", class_="label")
        if label_span:
            addr = label_span.get_text(strip=True)
            if addr:
                location_text.append(addr)

        dms_span = location_td.find("span", class_="geo-dms")
        if dms_span:
            coords = dms_span.get_text(" ", strip=True)
            location_text.append(coords)
        else:
            dec_span = location_td.find("span", class_="geo-dec")
            if dec_span:
                coords = dec_span.get_text(" ", strip=True)
                location_text.append(coords)

        if not location_text:
            location_text = [location_td.get_text(" ", strip=True)]

        location = ", ".join([part for part in location_text if part])

        record = {
            "name": name,
            "image": image_url,
            "location": location,
            "wikipedia_link": wikipedia_link
        }
        records.append(record)

    return records


def main():
    all_records = []

    # Iterate over all the Wikipedia pages
    for url in WIKI_PAGES:
        try:
            page_records = parse_wikipedia_page(url)
            all_records.extend(page_records)
        except requests.RequestException as e:
            print(f"Failed to scrape {url} - {e}")

    print(f"Total records scraped across all pages: {len(all_records)}")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)

    # Save combined results as JSON
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=4)

    print(f"Data saved to {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
