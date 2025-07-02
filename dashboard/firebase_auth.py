import pyrebase4 as pyrebase

import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# ----------------------------
# 🔐 Pyrebase Configuration
# ----------------------------
firebaseConfig = {
    "apiKey": st.secrets["firebase"]["apiKey"],
    "authDomain": st.secrets["firebase"]["authDomain"],
    "projectId": st.secrets["firebase"]["projectId"],
    "storageBucket": st.secrets["firebase"]["storageBucket"],
    "messagingSenderId": st.secrets["firebase"]["messagingSenderId"],
    "appId": st.secrets["firebase"]["appId"],
    "databaseURL": st.secrets["firebase"]["databaseURL"]
}

# ✅ Initialize Pyrebase Auth
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# ----------------------------
# 🔐 Firebase Admin (for Firestore)
# ----------------------------
if not firebase_admin._apps:  # ✅ Prevent multiple initializations
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ----------------------------
# 👤 Auth Functions
# ----------------------------
def register_user(email, password):
    return auth.create_user_with_email_and_password(email, password)

def login_user(email, password):
    return auth.sign_in_with_email_and_password(email, password)

def anon_sign_in():
    return {"localId": "anonymous_user"}

# ----------------------------
# 📦 Wishlist Firestore Handling
# ----------------------------
def save_wishlist(user_id, item):
    ref = db.collection("users").document(user_id)
    doc = ref.get()
    if doc.exists:
        current_list = doc.to_dict().get("wishlist", [])
    else:
        current_list = []
    current_list.append(item)
    ref.set({"wishlist": current_list})

def get_wishlist(user_id):
    doc = db.collection("users").document(user_id).get()
    if doc.exists:
        return doc.to_dict().get("wishlist", [])
    return []
