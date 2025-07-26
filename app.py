import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import bcrypt
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Initialize geocoder and sentence transformer model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()
geolocator = Nominatim(user_agent="food_share_app")

def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None
    except GeocoderTimedOut:
        return None

# Database setup
def init_db():
    conn = sqlite3.connect('food_share.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, 
                  user_type TEXT, name TEXT, address TEXT, lat REAL, lng REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS food_listings
                 (id INTEGER PRIMARY KEY, provider_id INTEGER, 
                  food_item TEXT, quantity TEXT, expiry DATETIME,
                  description TEXT, status TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY, listing_id INTEGER,
                  bank_id INTEGER, requested_quantity TEXT,
                  status TEXT, request_date DATETIME)''')
    
    conn.commit()
    conn.close()

# User authentication
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def signup(email, password, user_type, name, address):
    coords = geocode_address(address)
    if not coords:
        return False, "Could not verify address. Please enter a valid address."
    
    lat, lng = coords
    conn = sqlite3.connect('food_share.db')
    c = conn.cursor()
    hashed = hash_password(password)
    try:
        c.execute('''INSERT INTO users (email, password, user_type, name, address, lat, lng)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (email, hashed, user_type, name, address, lat, lng))
        conn.commit()
        return True, "Signup successful!"
    except:
        return False, "Signup failed. Email might already exist."
    finally:
        conn.close()

def login(email, password):
    conn = sqlite3.connect('food_share.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    
    if user and verify_password(password, user[2]):
        return user
    return None

# Food listing functions
def add_food_listing(provider_id, food_item, quantity, expiry, description):
    conn = sqlite3.connect('food_share.db')
    c = conn.cursor()
    c.execute('''INSERT INTO food_listings 
                 (provider_id, food_item, quantity, expiry, description, status)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (provider_id, food_item, quantity, expiry, description, 'available'))
    conn.commit()
    conn.close()

def get_provider_listings(provider_id):
    conn = sqlite3.connect('food_share.db')
    df = pd.read_sql_query('''
        SELECT f.*, 
               COUNT(r.id) as request_count,
               GROUP_CONCAT(u.name) as requestor_names
        FROM food_listings f
        LEFT JOIN requests r ON f.id = r.listing_id
        LEFT JOIN users u ON r.bank_id = u.id
        WHERE f.provider_id = ?
        GROUP BY f.id
        ORDER BY f.id DESC
    ''', conn, params=(provider_id,))
    conn.close()
    return df

def get_food_listings():
    conn = sqlite3.connect('food_share.db')
    df = pd.read_sql_query('''
        SELECT f.*, u.name as provider_name, u.address
        FROM food_listings f
        JOIN users u ON f.provider_id = u.id
        WHERE f.status = 'available'
        ORDER BY f.id DESC
    ''', conn)
    conn.close()
    return df

def get_bank_requests(bank_id):
    conn = sqlite3.connect('food_share.db')
    df = pd.read_sql_query('''
        SELECT r.*, f.food_item, f.quantity as available_quantity, 
               f.expiry, u.name as provider_name, u.address
        FROM requests r
        JOIN food_listings f ON r.listing_id = f.id
        JOIN users u ON f.provider_id = u.id
        WHERE r.bank_id = ?
        ORDER BY r.request_date DESC
    ''', conn, params=(bank_id,))
    conn.close()
    return df

def create_request(listing_id, bank_id, requested_quantity):
    conn = sqlite3.connect('food_share.db')
    c = conn.cursor()
    c.execute('''INSERT INTO requests 
                 (listing_id, bank_id, requested_quantity, status, request_date)
                 VALUES (?, ?, ?, ?, ?)''',
              (listing_id, bank_id, requested_quantity, 'pending', datetime.now()))
    conn.commit()
    conn.close()

# AI search function
def search_listings(query, listings_df):
    if listings_df.empty:
        return listings_df
    
    query_embedding = model.encode([query])
    listing_embeddings = model.encode(listings_df['description'].tolist())
    
    similarities = cosine_similarity(query_embedding, listing_embeddings)
    listings_df['similarity'] = similarities[0]
    
    return listings_df[listings_df['similarity'] > 0.3].sort_values('similarity', ascending=False)

# Main Streamlit app
def main():
    st.title("Food Share Platform")
    
    if 'user' not in st.session_state:
        st.session_state.user = None

    if not st.session_state.user:
        tab1, tab2 = st.tabs(["Login", "Signup"])
        
        with tab1:
            with st.form("login_form"):
                st.header("Login")
                login_email = st.text_input("Email")
                login_password = st.text_input("Password", type="password")
                login_submitted = st.form_submit_button("Login")
                if login_submitted:
                    user = login(login_email, login_password)
                    if user:
                        st.session_state.user = user
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")

        with tab2:
            with st.form("signup_form"):
                st.header("Signup")
                signup_email = st.text_input("Email")
                signup_password = st.text_input("Password", type="password")
                user_type = st.selectbox("User Type", ["Food Provider", "Food Bank"])
                name = st.text_input("Name")
                address = st.text_input("Full Address")
                signup_submitted = st.form_submit_button("Signup")
                
                if signup_submitted:
                    success, message = signup(signup_email, signup_password, user_type, name, address)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

    else:
        st.write(f"Welcome, {st.session_state.user[4]}!")
        
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

        # Food Provider Interface
        if st.session_state.user[3] == "Food Provider":
            tabs = st.tabs(["New Listing", "My Listings"])
            
            with tabs[0]:
                with st.form(key='new_listing_form'):
                    food_item = st.text_input("Food Item")
                    quantity = st.text_input("Quantity")
                    expiry = st.date_input("Expiry Date")
                    description = st.text_area("Description")
                    submit_button = st.form_submit_button("Add Listing")
                    
                    if submit_button:
                        add_food_listing(
                            st.session_state.user[0],
                            food_item,
                            quantity,
                            expiry,
                            description
                        )
                        st.success("Listing added successfully!")

            with tabs[1]:
                listings = get_provider_listings(st.session_state.user[0])
                if not listings.empty:
                    for _, row in listings.iterrows():
                        with st.expander(f"{row['food_item']} - {row['status']}"):
                            st.write(f"Quantity: {row['quantity']}")
                            st.write(f"Expiry: {row['expiry']}")
                            st.write(f"Description: {row['description']}")
                            st.write(f"Requests: {row['request_count']}")
                            if row['requestor_names']:
                                st.write(f"Requested by: {row['requestor_names']}")
                else:
                    st.write("No listings yet")

        # Food Bank Interface
        else:
            tabs = st.tabs(["Available Food", "My Requests"])
            
            with tabs[0]:
                st.header("Available Food Listings")
                
                search_query = st.text_input("How can I help you find food today?", 
                    placeholder="e.g., 'I'm looking for fresh vegetables' or 'Need bread items'")
                
                listings = get_food_listings()
                
                if not listings.empty:
                    if search_query:
                        listings = search_listings(search_query, listings)
                        if listings.empty:
                            st.write("I couldn't find any matching items. Try different search terms?")
                    
                    for _, row in listings.iterrows():
                        with st.expander(f"{row['food_item']} - {row['provider_name']}"):
                            st.write(f"Available Quantity: {row['quantity']}")
                            st.write(f"Expiry: {row['expiry']}")
                            st.write(f"Description: {row['description']}")
                            st.write(f"Address: {row['address']}")
                            
                            with st.form(key=f"request_form_{row['id']}"):
                                requested_qty = st.text_input("How much would you like to request?", 
                                                            key=f"qty_{row['id']}")
                                submit_request = st.form_submit_button("Submit Request")
                                
                                if submit_request:
                                    create_request(row['id'], st.session_state.user[0], requested_qty)
                                    st.success("Request sent to provider!")
                else:
                    st.write("No listings available")
            
            with tabs[1]:
                st.header("My Requests")
                requests = get_bank_requests(st.session_state.user[0])
                
                if not requests.empty:
                    for _, row in requests.iterrows():
                        with st.expander(f"{row['food_item']} - {row['status']}"):
                            st.write(f"Requested Quantity: {row['requested_quantity']}")
                            st.write(f"Available Quantity: {row['available_quantity']}")
                            st.write(f"Provider: {row['provider_name']}")
                            st.write(f"Address: {row['address']}")
                            st.write(f"Expiry: {row['expiry']}")
                            st.write(f"Request Date: {row['request_date']}")
                else:
                    st.write("No requests yet")


if __name__ == "__main__":
    init_db()
    main()
