import re
import json
import requests
from urllib.parse import quote

def get_direct_image_url(file_name):
    """
    Given a 'File:...' string, call the Wikipedia/Wikimedia API
    to get the direct upload URL. Returns the upload link, or None if not found.
    """
    base_api = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
        "titles": file_name
    }
    try:
        resp = requests.get(base_api, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # The 'pages' dict has some pageid key, e.g. '-1' or '12345'
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            imageinfo = page_data.get("imageinfo")
            if imageinfo and isinstance(imageinfo, list):
                # Usually there's just one 'imageinfo' with "url"
                return imageinfo[0].get("url")
    except Exception as e:
        print(f"Error fetching direct URL for {file_name}: {e}")

    return None

def extract_file_part(image_url):
    """
    Given a URL like:
      https://en.wikipedia.org/wiki/Something#/media/File:48-wall-street.jpg
    Return the File:... portion ("File:48-wall-street.jpg") if present, else None.
    """
    # Regex to capture /media/File:some_filename
    match = re.search(r"#/media/(File:[^?#]+)", image_url)
    if match:
        return match.group(1).strip()
    return None

def main():
    json_path = "../../../data/processed/sites.json"  # Adjust path if needed
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    count_updated = 0
    for entry in data:
        image_url = entry.get("image", "")
        if not image_url:
            continue

        # 1) Extract 'File:...' from the existing image URL
        file_part = extract_file_part(image_url)
        if file_part:
            # 2) Use the API to get the direct upload URL
            direct_link = get_direct_image_url(file_part)
            if direct_link:
                print(f"Updating: {image_url}  ->  {direct_link}")
                entry["image"] = direct_link
                count_updated += 1

    # Write updated data back
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Done. Updated {count_updated} image URL(s).")

if __name__ == "__main__":
    main()
