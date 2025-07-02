


import firebase_admin
from firebase_admin import credentials, firestore

import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests

# --- Initialize Firebase App only once ---
if not firebase_admin._apps:
    cred = credentials.Certificate(r"/home/nivetha-g/Tourist application/dashboard/firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Anonymous sign in placeholder
def anon_sign_in():
    return {"localId": "guest_user"}

# Register user using Firebase Identity REST API
def register_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={st.secrets['firebase']['apiKey']}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    res = requests.post(url, json=payload)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception(res.json()["error"]["message"])

# Login user using Firebase Identity REST API
def login_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={st.secrets['firebase']['apiKey']}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    res = requests.post(url, json=payload)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception(res.json()["error"]["message"])

# Save event to Firestore wishlist
def save_wishlist(uid, event_data):
    doc_ref = db.collection("wishlists").document(uid)
    doc_ref.set({event_data['name']: event_data}, merge=True)

# Get wishlist from Firestore
def get_wishlist(uid):
    doc = db.collection("wishlists").document(uid).get()
    if doc.exists:
        return list(doc.to_dict().values())
    return []
