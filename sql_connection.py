import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    host="foodbridge-db.cryuoe8i27vm.us-west-2.rds.amazonaws.com",
    port=5432,
    database="postgres",
    user="postgres",
    password="M7RG5CF2KFP9Nvm1n77W"
)

# Create a cursor
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        type VARCHAR(50),
        name VARCHAR(100),
        address VARCHAR(200),
        website VARCHAR(100),
        username VARCHAR(100),
        password VARCHAR(100)
    );
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id SERIAL PRIMARY KEY,
        food VARCHAR(256),
        quantity INTEGER,
        expiry_date DATE,
        details VARCHAR(256)             
    );    
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bridges (
        post_id INTEGER,
        bank_id INTEGER,
        resto_id INTEGER,
        quantity INTEGER              
    );    
""")

conn.commit()

def add_restaurant(name, address, website, username, password):
    cursor.execute("""
        INSERT INTO users (type, name, address, website, username, password)
        VALUES ('restaurant', %s, %s, %s, %s, %s);
    """, (type, name, address, website, username, password))
    conn.commit()

def add_food_bank(name, address, website, username, password):
    cursor.execute("""
        INSERT INTO users (type, name, address, website, username, password)
        VALUES ('foodbank', %s, %s, %s, %s, %s);
    """, (type, name, address, website, username, password))
    conn.commit()
    
def add_post(food, quantity, expiry_date, details):
    cursor.execute("""
        INSERT INTO posts (food, quantity, expiry_date, details)
        VALUES (%s, %s, %s, %s);
    """, (food, quantity, expiry_date, details))
    conn.commit()

def get_all_posts():
    cursor.execute("SELECT * FROM posts")

def get_restaurant_by_name(name):
    cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
    return cursor.fetchone()

def get_food_bank_by_name(name):
    cursor.execute("SELECT * FROM users WHERE name = %s", (name, ))
    return cursor.fetchone()

cursor.close()
conn.close()