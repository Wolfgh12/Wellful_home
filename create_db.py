import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg.connect(
        dbname="postgres",
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=os.getenv("DB_PORT", "5432"),
        autocommit=True,
    )
    with conn.cursor() as cur:
        cur.execute("CREATE DATABASE wellful_home_db;")
    print("Database 'wellful_home_db' created successfully!")
    conn.close()
except psycopg.errors.DuplicateDatabase:
    print("Database 'wellful_home_db' already exists.")
except Exception as e:
    print(f"Connection failed: {e}")