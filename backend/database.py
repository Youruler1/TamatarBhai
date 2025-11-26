"""
Database configuration and models for Tamatar-Bhai MVP
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database URL from environment or default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/tamatar_bhai.db")

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class Dish(Base):
    """Model for storing dish information"""
    __tablename__ = "dishes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    calories = Column(Integer, nullable=False)
    meal_type = Column(String, nullable=True)
    protein_g = Column(Float, nullable=True)
    carbs_g = Column(Float, nullable=True)
    fat_g = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Cache(Base):
    """Model for caching generated content"""
    __tablename__ = "cache"
    
    id = Column(Integer, primary_key=True, index=True)
    dish_name = Column(String, nullable=False, index=True)
    cache_type = Column(String, nullable=False)  # 'preview', 'image', 'caption'
    cache_data = Column(Text, nullable=False)  # JSON data
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


class UserMeal(Base):
    """Model for tracking user meal consumption"""
    __tablename__ = "user_meals"
    
    id = Column(Integer, primary_key=True, index=True)
    dish_name = Column(String, nullable=False)
    meal_type = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    consumed_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def populate_dishes_from_csv():
    """Populate dishes table from nutrition_lookup.csv"""
    import pandas as pd
    from sqlalchemy.orm import Session
    
    try:
        # Read CSV file
        df = pd.read_csv("data/nutrition_lookup.csv")
        
        # Create database session
        db = SessionLocal()
        
        # Check if dishes already exist
        existing_count = db.query(Dish).count()
        if existing_count > 0:
            print(f"📊 Dishes table already has {existing_count} entries")
            db.close()
            return
        
        # Add dishes from CSV
        dishes_added = 0
        for _, row in df.iterrows():
            dish = Dish(
                name=row['dish_name'],
                calories=int(row['calories']),
                meal_type=row['meal_type'],
                protein_g=float(row['protein_g']) if pd.notna(row['protein_g']) else None,
                carbs_g=float(row['carbs_g']) if pd.notna(row['carbs_g']) else None,
                fat_g=float(row['fat_g']) if pd.notna(row['fat_g']) else None,
                description=row['description'] if pd.notna(row['description']) else None
            )
            db.add(dish)
            dishes_added += 1
        
        db.commit()
        db.close()
        print(f"✅ Added {dishes_added} dishes to database")
        
    except Exception as e:
        print(f"❌ Error populating dishes: {e}")


if __name__ == "__main__":
    # Initialize database when run directly
    init_database()
    populate_dishes_from_csv()