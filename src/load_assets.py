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


assets = [
    # --- Commodities ---
    ('BZ=F', 'Brent Crude Oil', 'commodity', None, 'USD', 'ICE'),
    ('CL=F', 'WTI Crude Oil', 'commodity', None, 'USD', 'NYMEX'),
    ('NG=F', 'Natural Gas', 'commodity', None, 'USD', 'NYMEX'),
    ('GC=F', 'Gold', 'commodity', None, 'USD', 'COMEX'),

    # --- Defence ---
    ('LMT', 'Lockheed Martin', 'equity', 'defence', 'USD', 'NYSE'),
    ('RTX', 'RTX Corporation', 'equity', 'defence', 'USD', 'NYSE'),
    ('BA.L', 'BAE Systems', 'equity', 'defence', 'GBP', 'LSE'),

    # --- Airlines ---
    ('RYA.IR', 'Ryanair Holdings', 'equity', 'airlines', 'EUR', 'Euronext Dublin'),
    ('IAG.L', 'International Airlines Group', 'equity', 'airlines', 'GBP', 'LSE'),
    ('LHA.DE', 'Lufthansa', 'equity', 'airlines', 'EUR', 'XETRA'),
    ('DAL', 'Delta Air Lines', 'equity', 'airlines', 'USD', 'NYSE'),

    # --- Shipping ---
    ('MAERSK-B.CO', 'A.P. Moller-Maersk', 'equity', 'shipping', 'DKK', 'Nasdaq Copenhagen'),

    # --- Energy ---
    ('SHEL.L', 'Shell plc', 'equity', 'energy', 'GBP', 'LSE'),
    ('BP.L', 'BP plc', 'equity', 'energy', 'GBP', 'LSE'),
    ('XOM', 'Exxon Mobil', 'equity', 'energy', 'USD', 'NYSE'),

    # --- Indices ---
    ('^GSPC', 'S&P 500', 'index', None, 'USD', 'INDEX'),
    ('^FTSE', 'FTSE 100', 'index', None, 'GBP', 'INDEX'),
    ('^ISEQ', 'ISEQ All-Share', 'index', None, 'EUR', 'INDEX'),
    ('^VIX', 'CBOE Volatility Index', 'index', None, 'USD', 'CBOE'),

    # --- Currencies ---
    ('DX-Y.NYB', 'US Dollar Index', 'currency', None, 'USD', 'ICE'),
    ('EURUSD=X', 'EUR/USD', 'currency', None, 'USD', 'FX'),
]

cur.executemany("""
    INSERT INTO assets (ticker, name, asset_type, sector, currency, exchange)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (ticker) DO NOTHING;
""", assets)

conn.commit()
print(f"Inserted {len(assets)} assets into the database")
cur.close()
conn.close()