import pandas as pd
import random

# Load all three CSVs
df_weather = pd.read_csv(r"/home/nivetha-g/Tourist application/data/final_merged.csv")
df_city_info = pd.read_csv(r"/home/nivetha-g/Tourist application/data/enhanced_city_info.csv")
df_summary = pd.read_csv(r"/home/nivetha-g/Tourist application/data/city_summary_enriched.csv")

# Normalize city names
for df in [df_weather, df_city_info, df_summary]:
    df['city'] = df['city'].str.strip().str.lower()

# Merge weather + city info
merged1 = pd.merge(df_weather, df_city_info, on='city', how='left')

# Merge + summary
final_df = pd.merge(merged1, df_summary, on='city', how='left')

# Random fallback descriptions
fallbacks = [
    "A beautiful city worth visiting!",
    "A must-visit place with rich culture!",
    "An amazing destination for all travelers!",
    "Famous for its unique vibe and attractions.",
    "An unforgettable spot full of wonders!"
]

# Replace missing or invalid summaries
final_df['summary'] = final_df['summary'].apply(
    lambda x: random.choice(fallbacks) if pd.isna(x) or "no summary available" in str(x).lower() else x
)

# Restore title case city names
final_df['city'] = final_df['city'].str.title()

# Save to CSV
final_df.to_csv(r"/home/nivetha-g/Tourist application/data/final.csv", index=False)

print("✅ Enriched and cleaned data saved to: data/final_city_data_combined.csv")
