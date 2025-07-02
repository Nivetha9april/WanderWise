import requests
from bs4 import BeautifulSoup
import json
import time
import csv
import os

API_KEY = "9d16953b995f4ddfa1933915250107"  # Replace with your WeatherAPI key

# -------------------------
# Scrape Top 100 Tourist Cities
# -------------------------
def scrape_all_cities():
    url = "https://en.wikipedia.org/wiki/List_of_cities_by_international_visitors#2018/2016_top_100_rankings"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find("table", class_="wikitable sortable")
    cities = []

    if table:
        rows = table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                city = cols[2].text.strip().split("[")[0]
                if city and city not in cities:
                    cities.append(city)

    print(f"✅ Scraped {len(cities)} international cities.")
    return cities

# -------------------------
# Add 50 Popular Indian Cities
# -------------------------
def add_indian_cities(city_list):
    indian_cities = [
        "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem",
        "Thanjavur", "Kanyakumari", "Rameswaram", "Tirunelveli", "Erode",  # TN
        "Bengaluru", "Mysore", "Mangalore", "Hubli", "Belgaum",  # KA
        "Hyderabad", "Warangal", "Vijayawada", "Visakhapatnam",  # TS/AP
        "Mumbai", "Pune", "Nagpur", "Nashik", "Shirdi",  # MH
        "Delhi", "Agra", "Jaipur", "Udaipur", "Jaisalmer",  # North India
        "Lucknow", "Varanasi", "Bhopal", "Indore", "Gwalior",  # UP/MP
        "Ahmedabad", "Surat", "Gandhinagar",  # Gujarat
        "Kolkata", "Darjeeling", "Siliguri",  # WB
        "Patna", "Bodh Gaya", "Guwahati",  # Bihar/NE
        "Srinagar", "Leh", "Manali", "Shimla", "Amritsar"  # North Mountains
    ]

    for city in indian_cities:
        if city not in city_list:
            city_list.append(city)

    print(f"✅ Added {len(indian_cities)} Indian cities.")
    return city_list

# -------------------------
# Save all cities to CSV
# -------------------------
def save_city_list_csv(cities):
    os.makedirs('data', exist_ok=True)
    with open('data/city_list.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['city'])
        for city in cities:
            writer.writerow([city])
    print("✅ Saved city list to data/city_list.csv")

# -------------------------
# Fetch Weather
# -------------------------
def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "temperature": data['current']['temp_c'],
            "description": data['current']['condition']['text']
        }
    else:
        print(f"❌ Failed for {city} | Code: {response.status_code}")
        return None

# -------------------------
# Fetch All Weather Data
# -------------------------
def fetch_all_weather():
    cities = scrape_all_cities()
    cities = add_indian_cities(cities)
    save_city_list_csv(cities)

    all_data = []
    for i, city in enumerate(cities):
        print(f"📡 ({i+1}/{len(cities)}) Fetching weather for {city}...")
        data = get_weather(city)
        if data:
            all_data.append(data)
        time.sleep(1)

    with open('data/weather_data.json', 'w') as f:
        json.dump(all_data, f, indent=2)

    print("✅ Weather data saved to data/weather_data.json")

# -------------------------
# RUN SCRIPT
# -------------------------
if __name__ == "__main__":
    fetch_all_weather()
