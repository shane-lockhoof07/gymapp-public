import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text
from utils.db import engine, init_db
from models.base import Base
from models.users import UsersDB

load_dotenv()

def create_database():
    """Create database if it doesn't exist"""
    from sqlalchemy_utils import database_exists, create_database
    
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Created database: {engine.url.database}")

def create_schema():
    """Create schema if it doesn't exist"""
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS gym"))
        conn.commit()
    print("Schema 'gym' created successfully")

def create_tables():
    """Create all tables"""
    init_db()
    print("Tables created successfully")

def main():
    print("Starting database migration...")
    
    try:
        create_database()
        
        create_schema()
        
        create_tables()
        
        print("Migration completed successfully")
    except Exception as e:
        print(f"Migration error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()