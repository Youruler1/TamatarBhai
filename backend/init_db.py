#!/usr/bin/env python3
"""
Database initialization script for Tamatar-Bhai MVP
Run this to set up the database and populate initial data
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from database import init_database, populate_dishes_from_csv


def main():
    """Initialize database and populate with sample data"""
    print("🍅 Initializing Tamatar-Bhai Database...")
    
    # Ensure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    images_dir = data_dir / "images"
    images_dir.mkdir(exist_ok=True)
    
    # Initialize database tables
    print("📊 Creating database tables...")
    init_database()
    
    # Populate dishes from CSV
    print("🥘 Populating dishes from nutrition_lookup.csv...")
    populate_dishes_from_csv()
    
    print("✅ Database initialization complete!")
    print("   - Tables created: dishes, cache, user_meals")
    print("   - Sample dishes loaded from CSV")
    print("   - Ready for Tamatar-Bhai MVP!")


if __name__ == "__main__":
    main()