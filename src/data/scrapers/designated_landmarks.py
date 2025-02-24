import os
import json
import requests
from bs4 import BeautifulSoup

ADDITIONAL_WIKI_PAGES = [
    "https://en.wikipedia.org/wiki/List_of_New_York_City_Designated_Landmarks_in_Manhattan_below_14th_Street",
    "https://en.wikipedia.org/wiki/List_of_New_York_City_Designated_Landmarks_in_Manhattan_from_14th_to_59th_Streets",
    "https://en.wikipedia.org/wiki/List_of_New_York_City_Designated_Landmarks_in_Manhattan_from_59th_to_110th_Streets",
    "https://en.wikipedia.org/wiki/List_of_New_York_City_Designated_Landmarks_in_Manhattan_above_110th_Street",
    "https://en.wikipedia.org/wiki/List_of_New_York_City_Designated_Landmarks_in_Manhattan_on_smaller_islands",
    "https://en.wikipedia.org/wiki/List_of_New_York_City_Designated_Landmarks_in_Brooklyn",
    "https://en.wikipedia.org/wiki/List_of_New_York_City_Designated_Landmarks_in_Queens",
    "https://en.wikipedia.org/wiki/List_of_New_York_City_Designated_Landmarks_in_the_Bronx",
    "https://en.wikipedia.org/wiki/List_of_New_York_City_Designated_Landmarks_in_Staten_Island"
]

OUTPUT_JSON_PATH = os.path.join("../..", "..", "data", "raw", "designated_landmarks.json")


def parse_additional_wiki_page(url):
    """
    Scrapes a Wikipedia page that lists items across multiple <td> columns in each row.
    - We'll find all <tr> in the page.
    - For each row, we look at <td> blocks from left to right until we find:
       1) A name anchor (non-file) => <a href="/wiki/...">
       2) Then in subsequent <td> blocks, an image anchor => <a href="/wiki/File:...">
    """
    print(f"Scraping: {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # We'll parse the base page to build #/media links
    base_page = url.split("/wiki/")[-1].split("#", 1)[0]

    all_rows = soup.find_all("tr")
    records = []

    for row in all_rows:
        tds = row.find_all("td", recursive=False)
        if not tds:
            continue

        # --- STEP 1: Find the "name" anchor in the first relevant <td> ---
        name_anchor = None
        name = ""
        wikipedia_link = ""

        # We also track the index where we found that name, so we know where to start looking for the image next.
        name_td_index = None
        for i, td in enumerate(tds):
            anchor = td.find("a", href=True)
            if anchor:
                href = anchor["href"]
                # we only want non-file /wiki/ links
                if href.startswith("/wiki/") and not href.startswith("/wiki/File:"):
                    name = anchor.get_text(strip=True)
                    wikipedia_link = "https://en.wikipedia.org" + href
                    name_anchor = anchor
                    name_td_index = i
                    break  # stop searching for a name, we found it
        # If we didn't find a name, skip this row
        if not name_anchor:
            continue

        # --- STEP 2: Find the image anchor in the subsequent columns, if any ---
        image_url = ""
        for j in range(name_td_index + 1, len(tds)):
            # in each subsequent <td>, look for an anchor to /wiki/File:
            file_a = tds[j].find("a", href=lambda x: x and x.startswith("/wiki/File:"))
            if file_a:
                # Build the final link
                file_href = file_a["href"]
                file_part = file_href.split("/wiki/")[-1]
                image_url = f"https://en.wikipedia.org/wiki/{base_page}#/media/{file_part}"
                break

        # Build location
        location = f"{name}, New York, NY"

        # Put it all together
        record = {
            "name": name,
            "image": image_url,
            "location": location,
            "wikipedia_link": wikipedia_link
        }
        records.append(record)

    return records


def main():
    try:
        with open(OUTPUT_JSON_PATH, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    all_records = existing_data[:]

    for url in ADDITIONAL_WIKI_PAGES:
        try:
            new_records = parse_additional_wiki_page(url)
            all_records.extend(new_records)
        except requests.RequestException as e:
            print(f"Failed to scrape {url}: {e}")

    print(f"Scraped {len(all_records) - len(existing_data)} new records.")
    print(f"Total records: {len(all_records)}")

    # Save
    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=4)

    print(f"Data saved to {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
