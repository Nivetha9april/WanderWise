import os, re
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from firebase_auth import anon_sign_in, register_user, login_user, save_wishlist, get_wishlist
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

# --- CONFIG & BACKGROUND ---
st.set_page_config("WanderWise", layout="wide")
bg = "https://images.unsplash.com/photo-1486012563054-a205a26e389b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHRyYXZlbCUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D"
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
  background-image: url("{bg}");
  background-size: cover;
  background-attachment: fixed;
  background-position: center;
}}
.block-container {{
  background-color: rgba(255,255,255,0.88);
  padding: 1rem 2rem;
  border-radius: 8px;
}}
</style>""", unsafe_allow_html=True)

# --- LOAD DATA ---
df = pd.read_csv(r"/home/nivetha-g/Tourist application/data/final.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['summary'] = df['summary'].fillna("No summary available.")
df['temperature'] = df['temperature'].fillna(0.0)

# --- SIDEBAR ---
st.sidebar.image(
    "https://plus.unsplash.com/premium_photo-1681488267974-2e8438b60d4f?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    use_container_width=True
)
st.sidebar.title("🔐 WanderWise Login")
mode = st.sidebar.radio("Mode:", ("Guest", "Login", "Register"))
email = st.sidebar.text_input("Email")
pw = st.sidebar.text_input("Password", type="password")

# --- AUTHENTICATION ---
if 'user' not in st.session_state:
    st.session_state.user = anon_sign_in()

if mode == "Guest":
    if st.sidebar.button("Continue as Guest"):
        st.session_state.user = anon_sign_in()
        st.sidebar.success("Signed in as Guest")

elif mode == "Register":
    if st.sidebar.button("Register"):
        try:
            register_user(email, pw)
            st.sidebar.success("Registered! Now login.")
        except Exception as e:
            st.sidebar.error(str(e))

elif mode == "Login":
    if st.sidebar.button("Login"):
        try:
            st.session_state.user = login_user(email, pw)
            st.sidebar.success(f"Logged in as {email}")
        except Exception as e:
            st.sidebar.error("❌ Invalid email or password.")

uid = st.session_state.user.get('localId', None)

# --- HEADER ---
st.title("🌍 WanderWise")
st.markdown("### Discover destinations, events & travel vibes — filter, explore, save!")

# --- FILTER SECTION ---
search = st.text_input("🔎 Search events", "")
city_sel = st.selectbox("🏙️ Choose City", ["All"] + sorted(df['city'].dropna().unique()))
min_t, max_t = st.slider("🌡️ Temp Range (°C)", 0, 50, (0, 50))

filtered = df.copy()
if city_sel != "All":
    filtered = filtered[filtered['city'] == city_sel]
filtered = filtered[(filtered['temperature'] >= min_t) & (filtered['temperature'] <= max_t)]
if search:
    filtered = filtered[filtered['name'].str.contains(search, case=False, na=False)]

# --- CHARTS ---
st.subheader("📈 Travel Insights")
col1, col2 = st.columns(2)
with col1:
    top_cities = df['city'].value_counts().head(5)
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    top_cities.plot(kind='barh', color='skyblue', ax=ax1)
    ax1.set_title("Top Cities by Events")
    st.pyplot(fig1)

with col2:
    avg_temp = df.groupby('city')['temperature'].mean().nlargest(5)
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    avg_temp.plot(kind='bar', color='salmon', ax=ax2)
    ax2.set_title("Avg Temp per City")
    st.pyplot(fig2)

# --- MAP ---
if not filtered.empty:
    st.subheader("🗺️ Explore on Map")
    st.map(filtered[['latitude', 'longitude']].dropna())

# --- EVENT SECTION ---
st.subheader("🧭 Discover Events")
for _, row in filtered.iterrows():
    with st.expander(f"{row['name']} — {row['city']} on {row['date'].date()}"):
        st.write(f"🌡️ Temp: {row['temperature']} °C")
        st.write(f"📍 Location: {row['city']}")
        st.write(f"🧳 Summary: {row['summary']}")
        if uid:
            key = f"{row['name']}_{row['date'].date()}"
            if st.button("❤️ Save to Wishlist", key=key):
                save_wishlist(uid, row.to_dict())
                st.success("Saved!")

# --- WISHLIST SECTION ---
st.subheader("📚 My Wishlist")
wishlist = get_wishlist(uid) if uid else []

def export_pdf(wishlist):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "🌍 WanderWise Wishlist")

    c.setFont("Helvetica", 12)
    y = height - 80

    if not wishlist:
        c.drawString(50, y, "No events saved in wishlist.")
    else:
        for item in wishlist:
            event = f"{item['name']} — {item['city']} on {item['date']}"
            event = re.sub(r'[^\x00-\x7F]+', '', event)  # remove emojis/symbols
            c.drawString(50, y, event)
            y -= 20
            if y < 100:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 50

    c.save()
    buffer.seek(0)
    return buffer

if wishlist:
    pdf_data = export_pdf(wishlist)
    st.download_button("📥 Download Wishlist as PDF", data=pdf_data, file_name="wishlist.pdf", mime="application/pdf")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center>🌐 WanderWise • Powered by Nivetha 🚀</center>", unsafe_allow_html=True)
