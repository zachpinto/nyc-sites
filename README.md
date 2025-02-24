[LIVE HERE](https://zachpinto.com/projects/visualizations/nyc_sites/sites.html)

# NYC Sites Visualization

 - Interactive visualization of all landmarks, registered historical places, tourist attractions, museums, libraries, performing arts centers, zoos/gardens, and skyscrapers in New York City, soured from several Wikipedia lists.

 - Also contains a checklist for me to track which sites I've visited. (Anyone can clone to replicate for their own checklist)
   
## Features

- **Interactive Map**: Displays sites with categorized markers and popups.
- **Checklist View**: Allows users to track which sites they have visited.
- **Offline Geocoding**: Pre-fetches latitude and longitude data to reduce API costs.
- **Data Cleaning**: Ensures accurate site information, removes duplicates, and normalizes locations.
- **Minimalist UI**: Clean and intuitive interface.

## Project Structure
```
NYC_Sites_Visualization/
│── data/
│   ├── processed/
│   │   ├── sites.json
│   ├── raw/
│   │   ├── raw_sites.json
│
│── emoji/
│   ├── city.png
│
│── src/data/
│   ├── scrapers/
│   │   ├── designated_landmarks.py
│   │   ├── museums.py
│   │   ├── national_historical_landmarks.py
│   │   ├── national_register_historical_places.py
│   │   ├── skyscrapers.py
│   ├── checklist/
│   │   ├── add_visit_state.py
│   ├── clean/
│   │   ├── clean.py
│   │   ├── duplicate_images.py
│   ├── geocode/
│   │   ├── pre_geocode.py
│   ├── image_url/
│   │   ├── image_url.py
│   ├── map/
│   │   ├── lat_lng_adjustments.py
│   ├── aggregate/
│   │   ├── aggregate.py
│   │   ├── tidy_locations.py
│
│── favicon.ico
│── index.html
│── my_checklist.html
│── requirements.txt
│── README.md
```

## How to Run

This project is designed as a **static website** and can be hosted on **GitHub Pages** or any other static hosting provider.

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/nyc_visits.git

2. **Navigate to directory**
   ```sh
   cd nyc_visits

3. **Open index.html in browser**

## Data Processing
- Contains five scripts to scrape site data in json format.
- Other data was manually input from their respecitive sources
  


### Scrapers
    python scrapers/designated_landmarks.py
    python scrapers/museums.py
    python scrapers/national_historical_landmarks.py
    python scrapers/national_register_historical_places.py
    python scrapers/skyscrapers.py

### Aggregation
    python aggregate/aggregate.py

### Geocoding
    python geocode/pre_geocode.py

### Location Adjustments
    python map/lat_lng_adjustments.py

### Image URL Fixing
    python image_url/image_url.py

### Cleaning and Deduplication
    python clean/clean.py
    python clean/duplicate_images.py

### Creating new json key: values for checklist page
    python checklist/add_visit_state.py


#### Deployed on GitHub Pages as a static page on [GitHub](https://github.com/zachpinto/zachpinto.github.io) and [my site](https://zachpinto.com/projects/visualizations/nyc_sites/sites.html)


