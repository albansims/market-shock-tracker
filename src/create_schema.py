import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Get connection details from .env
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT') 
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Connect
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# CREATE TABLE statements go here
cur.execute("""
    CREATE TABLE IF NOT EXISTS assets (
    ticker TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    sector TEXT,
    currency TEXT NOT NULL,
    exchange TEXT NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        ticker TEXT REFERENCES assets(ticker),
        date DATE,
        open NUMERIC,
        high NUMERIC,
        low NUMERIC,
        close NUMERIC,
        adj_close NUMERIC,
        volume BIGINT,
        PRIMARY KEY (ticker, date)
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        event_id SERIAL PRIMARY KEY,
        event_date DATE NOT NULL,
        event_name TEXT NOT NULL,
        description TEXT,
        event_type TEXT,
        source_url TEXT,
        severity INTEGER
    );
""")

# Commit and close
conn.commit()
print("Schema created successfully")
cur.close()
conn.close()