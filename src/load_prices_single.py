import psycopg2
from dotenv import load_dotenv
import os
import yfinance as yf
import pandas as pd  # ADD THIS LINE

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

# Download returns a DataFrame
df = yf.download("LMT", start="2025-01-01", end="2026-04-30", auto_adjust=False)

# Flatten the column structure if it's multi-level
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Loop through rows:
for date, row in df.iterrows():
    open_price = float(row['Open'])
    high_price = float(row['High'])
    low_price = float(row['Low'])
    close_price = float(row['Close'])
    adj_close_price = float(row['Adj Close'])
    volume = int(row['Volume'])

    # Execute insert
    cur.execute("""
    INSERT INTO prices (ticker, date, open, high, low, close, adj_close, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (ticker, date) DO NOTHING;
""", ("LMT", date.strftime('%Y-%m-%d'), open_price, high_price, low_price, close_price, adj_close_price, volume))

conn.commit()
print(f"Loaded {len(df)} rows for LMT")
cur.close()
conn.close()