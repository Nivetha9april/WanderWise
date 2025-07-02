import requests
import time
import pandas as pd

cities_df = pd.read_csv('/home/nivetha-g/Tourist application/data/city_list.csv')
cities = cities_df['city'].tolist()


API_KEY = "97ba6e3c7dmsh6c13e1261b7de89p156ebejsn1b829bd9333b"
url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
}

city_info_list = []

for city in cities:
    params = {"namePrefix": city, "limit": 1, "countryIds": "IN"}  # Add more filters if needed
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if data['data']:
        city_data = data['data'][0]
        city_info = {
            "city": city_data.get("city"),
            "country": city_data.get("country"),
            "population": city_data.get("population"),
            "timezone": city_data.get("timezone"),
            "latitude": city_data.get("latitude"),
            "longitude": city_data.get("longitude")
        }
        city_info_list.append(city_info)
    
    time.sleep(1)  # avoid hitting rate limit on free tier

# Save to new CSV
pd.DataFrame(city_info_list).to_csv("enhanced_city_info.csv", index=False)
