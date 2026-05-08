import psycopg2
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
cur = conn.cursor()

cur.execute("SELECT ticker FROM assets;")
tickers = [row[0] for row in cur.fetchall()]

for ticker in tickers:
    try:
        print(f"Processing {ticker}...")

        # Download data
        df = yf.download(ticker, start="2025-01-01", end=(date.today()).isoformat(), auto_adjust=False)

        # Skip if empty
        if df.empty:
            print(f"No data for {ticker}")
            continue

        # Flatten columns (sometimes yfinance returns multi-index)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Loop through rows
        for date, row in df.iterrows():
            open_price = row['Open']
            high_price = row['High']
            low_price = row['Low']
            close_price = row['Close']
            adj_close_price = row['Adj Close']
            volume = row['Volume']

            cur.execute("""
                INSERT INTO prices (ticker, date, open, high, low, close, adj_close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ticker, date) DO NOTHING;
            """, (
                ticker,
                date.date(),
                float(open_price) if not pd.isna(open_price) else None,
                float(high_price) if not pd.isna(high_price) else None,
                float(low_price) if not pd.isna(low_price) else None,
                float(close_price) if not pd.isna(close_price) else None,
                float(adj_close_price) if not pd.isna(adj_close_price) else None,
                int(volume) if not pd.isna(volume) else None
            ))

        print(f"✅ Success: {ticker}")

    except Exception as e:
        print(f"❌ Failed: {ticker} | Error: {e}")
        continue

conn.commit()

cur.close()
conn.close()

