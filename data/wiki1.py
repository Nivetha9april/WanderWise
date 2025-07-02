import pandas as pd
import wikipedia

# Set language to English
wikipedia.set_lang("en")

# Load your city list
df = pd.read_csv("data/city_list.csv")

# Create a new column for summaries
summaries = []

# Fetch summary for each city
for city in df['city']:
    try:
        summary = wikipedia.summary(city, sentences=2)
        print(f"✅ Fetched for {city}")
    except Exception as e:
        summary = "No summary available."
        print(f"❌ Failed for {city}: {e}")
    summaries.append(summary)

# Add summary column
df['summary'] = summaries

# Save the new CSV
df.to_csv("data/city_summary_enriched.csv", index=False)
print("✅ Done! File saved as city_summary_enriched.csv")
