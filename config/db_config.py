import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    try:
        connection = psycopg2.connect(
            #host=localhost,  # Use this to connect to the local PostgreSQL server
            host="host.docker.internal",  # Use this to connect to the host machine's database
            database=os.getenv("DB_NAME"),
            user="postgres",
            password=os.getenv("DB_PASSWORD"),
            port=5432
        )
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Test the connection when running this script
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("✅ Connection test passed! Database is accessible.")
        conn.close()
    else:
        print("❌ Connection test failed!")