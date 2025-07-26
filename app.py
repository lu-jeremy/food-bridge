import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect('foodbridge.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                  type TEXT,
                  name TEXT,
                  address TEXT,
                  username TEXT UNIQUE,
                  password TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY,
                  food TEXT,
                  quantity INTEGER,
                  expiry_date DATE,
                  details TEXT,
                  provider_id INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY,
                  post_id INTEGER,
                  bank_id INTEGER,
                  quantity INTEGER,
                  status TEXT)''')
    
    conn.commit()
    conn.close()

# Database functions
def create_user(type, name, address, username, password):
    conn = sqlite3.connect('foodbridge.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (type, name, address, username, password) VALUES (?, ?, ?, ?, ?)',
                 (type, name, address, username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('foodbridge.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

def create_post(food, quantity, expiry_date, details, provider_id):
    conn = sqlite3.connect('foodbridge.db')
    c = conn.cursor()
    c.execute('''INSERT INTO posts (food, quantity, expiry_date, details, provider_id)
                 VALUES (?, ?, ?, ?, ?)''',
              (food, quantity, expiry_date, details, provider_id))
    conn.commit()
    conn.close()

def get_posts():
    conn = sqlite3.connect('foodbridge.db')
    df = pd.read_sql_query('''
        SELECT posts.*, users.name as provider_name, users.address
        FROM posts 
        JOIN users ON posts.provider_id = users.id
        WHERE posts.quantity > 0
        ORDER BY posts.id DESC''', conn)
    conn.close()
    return df

def create_request(post_id, bank_id, quantity):
    conn = sqlite3.connect('foodbridge.db')
    c = conn.cursor()
    c.execute('INSERT INTO requests (post_id, bank_id, quantity, status) VALUES (?, ?, ?, ?)',
              (post_id, bank_id, quantity, 'pending'))
    c.execute('UPDATE posts SET quantity = quantity - ? WHERE id = ?',
              (quantity, post_id))
    conn.commit()
    conn.close()

def get_my_posts(provider_id):
    conn = sqlite3.connect('foodbridge.db')
    df = pd.read_sql_query('''
        SELECT p.*, COUNT(r.id) as request_count
        FROM posts p
        LEFT JOIN requests r ON p.id = r.post_id
        WHERE p.provider_id = ?
        GROUP BY p.id
        ORDER BY p.id DESC''', conn, params=[provider_id])
    conn.close()
    return df

def get_my_requests(bank_id):
    conn = sqlite3.connect('foodbridge.db')
    df = pd.read_sql_query('''
        SELECT r.*, p.food, p.expiry_date, u.name as provider_name, u.address
        FROM requests r
        JOIN posts p ON r.post_id = p.id
        JOIN users u ON p.provider_id = u.id
        WHERE r.bank_id = ?
        ORDER BY r.id DESC''', conn, params=[bank_id])
    conn.close()
    return df

# Main app
def main():
    st.set_page_config(page_title="FoodBridge", page_icon="🌉", layout="wide")
    
    if 'user' not in st.session_state:
        st.session_state.user = None

    if not st.session_state.user:
        st.title("🌉 FoodBridge")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                
                if submitted:
                    user = verify_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        with tab2:
            with st.form("signup_form"):
                type = st.selectbox("Type", ["restaurant", "foodbank"])
                name = st.text_input("Organization Name")
                address = st.text_input("Address")
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign Up")
                
                if submitted:
                    if create_user(type, name, address, new_username, new_password):
                        st.success("Account created! Please login.")
                    else:
                        st.error("Username already exists")

    else:
        # Sidebar
        with st.sidebar:
            st.write(f"Welcome, {st.session_state.user[2]}")
            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()

        # Restaurant Interface
        if st.session_state.user[1] == 'restaurant':
            tabs = st.tabs(["New Post", "My Posts"])
            
            with tabs[0]:
                st.header("Create Food Post")
                with st.form("post_form"):
                    food = st.text_input("Food Item")
                    quantity = st.number_input("Quantity", min_value=1, step=1)
                    expiry_date = st.date_input("Expiry Date")
                    details = st.text_area("Additional Details")
                    submitted = st.form_submit_button("Create Post")
                    
                    if submitted:
                        create_post(food, quantity, expiry_date, details, st.session_state.user[0])
                        st.success("Post created!")

            with tabs[1]:
                st.header("My Posts")
                posts = get_my_posts(st.session_state.user[0])
                if not posts.empty:
                    for _, row in posts.iterrows():
                        with st.expander(f"{row['food']} - Quantity: {row['quantity']}"):
                            st.write(f"Expiry Date: {row['expiry_date']}")
                            st.write(f"Details: {row['details']}")
                            st.write(f"Requests: {row['request_count']}")
                else:
                    st.info("No posts yet")

        # Food Bank Interface
        else:
            tabs = st.tabs(["Available Food", "My Requests"])
            
            with tabs[0]:
                st.header("Available Food")
                posts = get_posts()
                if not posts.empty:
                    for _, row in posts.iterrows():
                        with st.expander(f"{row['food']} - {row['provider_name']}"):
                            st.write(f"Quantity Available: {row['quantity']}")
                            st.write(f"Expiry Date: {row['expiry_date']}")
                            st.write(f"Details: {row['details']}")
                            st.write(f"Location: {row['address']}")
                            
                            with st.form(f"request_form_{row['id']}"):
                                request_qty = st.number_input("Request Quantity", 
                                                            min_value=1, 
                                                            max_value=row['quantity'],
                                                            step=1)
                                submitted = st.form_submit_button("Request Food")
                                
                                if submitted:
                                    create_request(row['id'], st.session_state.user[0], request_qty)
                                    st.success("Request sent!")
                else:
                    st.info("No food available")

            with tabs[1]:
                st.header("My Requests")
                requests = get_my_requests(st.session_state.user[0])
                if not requests.empty:
                    for _, row in requests.iterrows():
                        with st.expander(f"{row['food']} from {row['provider_name']}"):
                            st.write(f"Quantity: {row['quantity']}")
                            st.write(f"Status: {row['status']}")
                            st.write(f"Provider: {row['provider_name']}")
                            st.write(f"Location: {row['address']}")
                else:
                    st.info("No requests yet")

if __name__ == "__main__":
    init_db()
    main()
