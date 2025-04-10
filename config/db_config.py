import psycopg2
from psycopg2 import Error

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="IntraSchoolEventDB",
            user="postgres",
            password="****",
            port=5432
        )
        print("✅ PostgreSQL connection established successfully!")
        
        # Test connection with a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("PostgreSQL Version:", version[0])

        return connection
    except (Exception, Error) as error:
        print("❌ Error while connecting to PostgreSQL:", error)
        return None
# Test the connection when running this script
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("✅ Connection test passed! Database is accessible.")
        conn.close()
    else:
        print("❌ Connection test failed!")