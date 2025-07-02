import pandas as pd
import json

# ---------------------------
# Load weather data
# ---------------------------
with open("data/weather_data.json", "r") as f:
    weather_data = json.load(f)

df_weather = pd.DataFrame(weather_data)

# ---------------------------
# Load event data
# ---------------------------
with open("data/event_data.json", "r") as f:
    event_data = json.load(f)

df_events = pd.DataFrame(event_data)

# ---------------------------
# Merge data on city
# ---------------------------
df_merged = pd.merge(df_events, df_weather, on="city", how="left")

# ---------------------------
# Sample insights
# ---------------------------

print("\n🔹 Number of events per city:")
print(df_merged['city'].value_counts().head(10))

print("\n🔹 Cities with highest average temperature for events:")
print(df_merged.groupby('city')['temperature'].mean().sort_values(ascending=False).head(10))

print("\n🔹 Events happening in rainy/cloudy conditions:")
print(df_merged[df_merged['description'].str.contains("Rain|Cloud", case=False, na=False)])

# ---------------------------
# Save the merged data
# ---------------------------
df_merged.to_csv("data/final_merged.csv", index=False)
print("\n✅ Merged data saved to data/final_merged.csv")
