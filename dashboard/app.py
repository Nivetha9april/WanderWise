import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# --- CONFIG ---
st.set_page_config(page_title="WanderWise", layout="wide")

# --- STYLING ---
with open("/home/nivetha-g/Tourist application/dashboard/03d9d08c5706f25d81034ac77992cd68.jpg", "rb") as file:
    encoded = file.read()
b64 = f"data:image/jpg;base64,{encoded.hex()}"

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: url("data:image/jpg;base64,{encoded.hex()}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
.block-container {{
    background-color: rgba(255, 255, 255, 0.9);
    padding: 2rem;
    border-radius: 10px;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- LOAD DATA ---
df = pd.read_csv("/home/nivetha-g/Tourist application/data/final.csv")
df.columns = df.columns.str.strip().str.lower()

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['summary'] = df['summary'].fillna("No summary available.")
df['temperature'] = df['temperature'].fillna(0.0)
df['country'] = df['country'].fillna("Unknown")

# --- HEADER ---
st.markdown("<h1 style='text-align:center;'>🌍 WanderWise</h1>", unsafe_allow_html=True)
st.markdown("#### Discover handpicked destinations, events & vibes that suit your style!")

# --- QUOTES ---
quotes = [
    "📌 New place, new memories waiting!",
    "🌞 Life’s better when you travel.",
    "✈️ Pack your bags, WanderWise has you covered!",
    "📍 Go where your heart feels light.",
]
st.info(random.choice(quotes))

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.header("🔍 Filter Explorer")
    city = st.selectbox("City", ["All"] + sorted(df['city'].dropna().unique()))
    min_temp = st.slider("Min Temp (°C)", 0, 50, 0)
    max_temp = st.slider("Max Temp (°C)", 0, 50, 50)

# --- FILTER LOGIC ---
filtered_df = df[
    (df['temperature'] >= min_temp) &
    (df['temperature'] <= max_temp)
]
if city != "All":
    filtered_df = filtered_df[filtered_df['city'] == city]

# --- HIGHLIGHT TOP CITIES FIRST ---
st.subheader("🔥 Trending Cities")
top_city_counts = df['city'].value_counts().head(5)
cols = st.columns(len(top_city_counts))

for i, (city_name, count) in enumerate(top_city_counts.items()):
    with cols[i]:
        st.metric(label=f"🏙️ {city_name}", value=f"{count} Events")

# --- CHARTS ---
st.subheader("📊 Travel Insights")

col1, col2 = st.columns(2)

with col1:
    top_cities = df['city'].value_counts().head(7)
    fig1, ax1 = plt.subplots()
    top_cities.plot(kind='barh', ax=ax1, color='skyblue')
    ax1.set_title("Top Cities")
    ax1.set_xlabel("Event Count")
    st.pyplot(fig1)

with col2:
    top_temp = df.groupby('city')['temperature'].mean().sort_values(ascending=False).head(7)
    fig2, ax2 = plt.subplots()
    top_temp.plot(kind='bar', ax=ax2, color='orange')
    ax2.set_title("Cities with Warmest Weather")
    ax2.set_ylabel("Avg Temp (°C)")
    st.pyplot(fig2)

# --- DESTINATION CARDS ---
st.subheader("🧭 Explore Events & Places")

if filtered_df.empty:
    st.warning("No events found! Try changing filters.")
else:
    for city_name in filtered_df['city'].unique():
        city_events = filtered_df[filtered_df['city'] == city_name]
        st.markdown(f"### 📍 {city_name}")
        for _, row in city_events.iterrows():
            with st.expander(f"🗓️ {row['name']} — {row['date'].date() if pd.notnull(row['date']) else 'No Date'}"):
                st.write(f"**🌡 Temperature:** {row['temperature']} °C")
                st.write(f"**☁ Weather:** {row['description']}")
                st.write(f"**🌐 Country:** {row['country']}")
                st.write(f"**🗺 Coordinates:** {row['latitude']}, {row['longitude']}")
                st.write(f"**🧳 Summary:** {row['summary']}")

# --- Footer ---
st.markdown("---")
st.markdown("<center>🌐 WanderWise • Powered by Nivetha's Travel Engine</center>", unsafe_allow_html=True)
