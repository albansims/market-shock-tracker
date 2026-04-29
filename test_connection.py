from dotenv import load_dotenv
import psycopg2
import os

# Load the environment variables from the .env file
load_dotenv()
# Get the database connection parameters from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT') 
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Connect to the database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Execute a query
cur.execute("SELECT version()")
row = cur.fetchone()
print(row)

# Close communication
cur.close()
conn.close()

