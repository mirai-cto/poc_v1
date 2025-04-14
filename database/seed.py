#!/usr/bin/env python3
import os
import pandas as pd
import psycopg2
import csv
import sys
from datetime import datetime

# Database connection parameters
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'cnc_tool_recommender')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')

# CSV file paths
TOOLS_CSV = '/app/data/tools.csv'  # Path in container
MACHINES_CSV = '/app/data/machines.csv'  # Path in container

def connect_to_db():
    """Connect to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print(f"Connected to database {DB_NAME} on {DB_HOST}")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        sys.exit(1)

def import_tools(conn):
    """Import tools from CSV file"""
    try:
        df = pd.read_csv(TOOLS_CSV)
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("TRUNCATE TABLE tools CASCADE")
        
        # Prepare column names and placeholders for SQL insert
        columns = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        
        # Insert data
        for _, row in df.iterrows():
            values = tuple(None if pd.isna(x) else x for x in row)
            cursor.execute(f"INSERT INTO tools ({columns}) VALUES ({placeholders})", values)
        
        conn.commit()
        print(f"Successfully imported {len(df)} tools")
        
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(f"Error importing tools: {error}")
        sys.exit(1)

def import_machines(conn):
    """Import machines from CSV file"""
    try:
        df = pd.read_csv(MACHINES_CSV)
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("TRUNCATE TABLE machines CASCADE")
        
        # Prepare column names and placeholders for SQL insert
        columns = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        
        # Insert data
        for _, row in df.iterrows():
            values = tuple(None if pd.isna(x) else x for x in row)
            cursor.execute(f"INSERT INTO machines ({columns}) VALUES ({placeholders})", values)
        
        conn.commit()
        print(f"Successfully imported {len(df)} machines")
        
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(f"Error importing machines: {error}")
        sys.exit(1)

def main():
    """Main function to run the seed script"""
    print("Starting database seeding at", datetime.now())
    
    # Check if CSV files exist
    if not os.path.exists(TOOLS_CSV):
        print(f"Error: Tools CSV file not found at {TOOLS_CSV}")
        sys.exit(1)
    
    if not os.path.exists(MACHINES_CSV):
        print(f"Error: Machines CSV file not found at {MACHINES_CSV}")
        sys.exit(1)
    
    # Connect to database
    conn = connect_to_db()
    
    # Import data
    import_tools(conn)
    import_machines(conn)
    
    # Close connection
    conn.close()
    print("Database seeding completed at", datetime.now())

if __name__ == "__main__":
    main() 