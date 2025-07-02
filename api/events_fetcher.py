import requests
import json
import time
import csv
import os

TICKETMASTER_API_KEY = "vDyIwOrFdMotyy07FA3hyt4Qxf1j6hrg"
 # Replace this with your actual key

# -------------------------------
# Load cities from CSV (same as Day 1 output)
# -------------------------------
def load_cities_from_csv():
    cities = []
    with open('data/city_list.csv', 'r') as f:
        next(f)  # skip header
        for line in f:
            city = line.strip()
            if city:
                cities.append(city)
    return cities

# -------------------------------
# Fetch events for a given city
# -------------------------------
def fetch_events_for_city(city):
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TICKETMASTER_API_KEY}&city={city}&size=5"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        events = []

        if '_embedded' in data:
            for event in data['_embedded']['events']:
                events.append({
                    "name": event['name'],
                    "date": event['dates']['start'].get('localDate', ''),
                    "city": city
                })
        return events
    else:
        print(f"❌ Failed for {city} | Code: {response.status_code}")
        return []

# -------------------------------
# Main fetch logic
# -------------------------------
def fetch_all_events():
    cities = load_cities_from_csv()
    all_events = []

    for i, city in enumerate(cities):
        print(f"🎟️ ({i+1}/{len(cities)}) Fetching events for {city}...")
        events = fetch_events_for_city(city)
        all_events.extend(events)
        time.sleep(1)

    os.makedirs('data', exist_ok=True)
    with open('data/event_data.json', 'w') as f:
        json.dump(all_events, f, indent=2)

    print("✅ Event data saved to data/event_data.json")

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    fetch_all_events()
