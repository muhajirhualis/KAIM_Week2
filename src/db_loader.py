import sys
import os

# Add the project root to the system path to allow imports from config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import psycopg2
import pandas as pd
from config import DATA_PATHS 
from dotenv import load_dotenv
import os

DB_CONFIG = {
    'host': os.getenv('PG_HOST'),
    'database': os.getenv('PG_DATABASE'),
    'user': os.getenv('PG_USER'),
    'password': os.getenv('PG_PASSWORD')
}

# --- File Configuration ---
INPUT_FILE_PATH = DATA_PATHS['final_results']
    
def load_data_to_postgres():
    """
    Connects to PostgreSQL, maps bank names to bank_ids, and inserts
    the final analyzed review data into the 'reviews' table.
    """
    if not os.path.exists(INPUT_FILE_PATH):
        print(f"ERROR: Input file not found at {INPUT_FILE_PATH}")
        return

    df = pd.read_csv(INPUT_FILE_PATH)
    print(f"Loaded {len(df)} records from {INPUT_FILE_PATH}.")

    conn = None
    try:
        # Establish connection
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # 1. Get Bank IDs (Mapping)
        # We need the bank_id to link the reviews table correctly.
        cur.execute("SELECT bank_name, bank_id FROM banks;")
        bank_map = {row[0]: row[1] for row in cur.fetchall()}
        
        # Add the bank_id column to the DataFrame for insertion
        df['bank_id'] = df['bank_name'].map(bank_map)

        # Check for successful mapping
        if df['bank_id'].isnull().any():
            print("WARNING: Some bank names could not be mapped to bank_id.")
            # Drop unmapped rows or raise error
            df.dropna(subset=['bank_id'], inplace=True)
            df['bank_id'] = df['bank_id'].astype(int)
        
        # 2. Prepare Data for Insertion
        # Define the order of columns to match the SQL table definition
        cols = ['review_id', 'bank_id', 'review_text', 'rating', 'sentiment_label', 'sentiment_score', 'theme']
        
        # Ensure all columns exist and handle missing 'review_date' if necessary
        # NOTE: If you scrape 'review_date', ensure it's in the CSV and included above.
        
        # Replace NaN values with None for SQL compatibility
        data_records = [tuple(row.where(pd.notnull(row), None)) for index, row in df[cols].iterrows()]
        
        # 3. Construct the SQL INSERT statement
        table = 'reviews'
        columns = ', '.join(cols)
        # Use a parameterized query for safety (%s placeholders)
        placeholders = ', '.join(['%s'] * len(cols))
        insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) ON CONFLICT (review_id) DO NOTHING;"

        # 4. Execute Insertion
        cur.executemany(insert_query, data_records)
        conn.commit()
        
        print(f"Successfully inserted/updated {cur.rowcount} records into the 'reviews' table.")

    except psycopg2.Error as e:
        print(f"Database Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_postgres()