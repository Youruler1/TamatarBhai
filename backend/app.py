"""
FastAPI application for Tamatar-Bhai MVP
Main application entry point with API endpoints
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime, timedelta
import logging

# Import local modules
from database import get_db, init_database, populate_dishes_from_csv
from models import (
    PreviewRequest, PreviewResponse, 
    CompareRequest, CompareResponse,
    WeeklyResponse, DishModel, ErrorResponse, UserMealEntry
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Tamatar-Bhai MVP API",
    description="AI-powered food insights with bhai style personality",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for images
app.mount("/data", StaticFiles(directory="data"), name="data")

# Load model routes configuration
def load_model_routes():
    """Load model routing configuration"""
    try:
        with open("model_routes.json", "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load model_routes.json: {e}")
        return {}

model_routes = load_model_routes()


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        init_database()
        populate_dishes_from_csv()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🍅 Welcome to Tamatar-Bhai MVP API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "tamatar-bhai-api"
    }


# API Endpoints

@app.post("/api/preview", response_model=PreviewResponse)
async def generate_preview(
    request: PreviewRequest,
    db: Session = Depends(get_db)
):
    """
    Generate daily preview with image, calories, and captions
    """
    try:
        from services.service_manager import service_manager
        from services.nutrition_service import nutrition_service
        from services.cache_service import cache_service
        from database import UserMeal
        
        # Check cache first
        cached_preview = await cache_service.get_cached_preview(request.dish, db)
        if cached_preview:
            logger.info(f"✅ Returning cached preview for '{request.dish}'")
            return PreviewResponse(**cached_preview)
        
        # Get nutrition information
        dish_info = nutrition_service.get_dish_info(request.dish)
        calories = dish_info['calories']
        
        # Generate image (check cache first)
        cached_image = await cache_service.get_cached_image(request.dish, db)
        if cached_image:
            image_url = cached_image
            logger.info(f"✅ Using cached image for '{request.dish}'")
        else:
            image_url = await service_manager.generate_dish_image(request.dish)
            # Cache the generated image
            await cache_service.cache_image(request.dish, image_url, db)
        
        # Generate captions (check cache first)
        cached_captions = await cache_service.get_cached_captions(request.dish, db)
        if cached_captions:
            captions = cached_captions
            logger.info(f"✅ Using cached captions for '{request.dish}'")
        else:
            # Generate both bhai and formal captions
            bhai_caption = await service_manager.generate_bhai_caption(request.dish, calories)
            formal_caption = await service_manager.generate_formal_caption(request.dish, calories)
            
            captions = {
                "bhai": bhai_caption,
                "formal": formal_caption
            }
            
            # Cache the captions
            await cache_service.cache_captions(request.dish, captions, db)
        
        # Create response
        preview_data = {
            "dish": request.dish,
            "calories": calories,
            "image_url": image_url,
            "captions": captions,
            "meta": {
                "model": "openai-gpt-4o-mini",
                "generated_at": datetime.utcnow().isoformat(),
                "matched_dish": dish_info.get('matched_name', request.dish),
                "confidence": dish_info.get('confidence', 100)
            }
        }
        
        # Cache the complete preview
        await cache_service.cache_preview(request.dish, preview_data, db)
        
        # Track user meal consumption
        user_meal = UserMeal(
            dish_name=request.dish,
            meal_type=request.meal,
            calories=calories
        )
        db.add(user_meal)
        db.commit()
        
        logger.info(f"✅ Generated complete preview for '{request.dish}' ({calories} cal)")
        return PreviewResponse(**preview_data)
        
    except Exception as e:
        logger.error(f"Preview generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate preview: {str(e)}"
        )


@app.get("/api/dishes")
async def get_dishes(db: Session = Depends(get_db)):
    """
    Get list of all available dishes
    """
    try:
        from database import Dish
        dishes = db.query(Dish).all()
        
        return [
            {
                "id": dish.id,
                "name": dish.name,
                "calories": dish.calories,
                "meal_type": dish.meal_type,
                "description": dish.description
            }
            for dish in dishes
        ]
        
    except Exception as e:
        logger.error(f"Failed to fetch dishes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch dishes: {str(e)}"
        )
    

@app.get("/api/user_meals")
async def get_dishes(db: Session = Depends(get_db)):
    """
    Get list of all available user meals
    """
    try:
        from database import UserMeal
        user_meals = db.query(UserMeal).all()
        
        return [
            {
                "id": user_meal.id,
                "dish_name": user_meal.dish_name,
                "meal_type": user_meal.meal_type,
                "calories": user_meal.calories,
                "consumed_at": user_meal.consumed_at
            }
            for user_meal in user_meals
        ]
        
    except Exception as e:
        logger.error(f"Failed to fetch user_meals: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user_meals: {str(e)}"
        )


@app.post("/api/compare", response_model=CompareResponse)
async def compare_dishes(
    request: CompareRequest,
    db: Session = Depends(get_db)
):
    """
    Compare two dishes and provide bhai-style recommendation
    """
    try:
        from services.service_manager import service_manager
        from services.nutrition_service import nutrition_service
        
        # Get nutrition information for both dishes
        dish_a_info = nutrition_service.get_dish_info(request.dishA)
        dish_b_info = nutrition_service.get_dish_info(request.dishB)
        
        calories_a = dish_a_info['calories']
        calories_b = dish_b_info['calories']
        
        # Create dish data objects
        dish_a_data = {
            "name": request.dishA,
            "calories": calories_a,
            "matched_name": dish_a_info.get('matched_name', request.dishA),
            "confidence": dish_a_info.get('confidence', 100),
            "protein_g": dish_a_info.get('protein_g'),
            "carbs_g": dish_a_info.get('carbs_g'),
            "fat_g": dish_a_info.get('fat_g')
        }
        
        dish_b_data = {
            "name": request.dishB,
            "calories": calories_b,
            "matched_name": dish_b_info.get('matched_name', request.dishB),
            "confidence": dish_b_info.get('confidence', 100),
            "protein_g": dish_b_info.get('protein_g'),
            "carbs_g": dish_b_info.get('carbs_g'),
            "fat_g": dish_b_info.get('fat_g')
        }
        
        # Generate bhai-style comparison suggestion
        suggestion = await service_manager.generate_comparison_suggestion(
            request.dishA, request.dishB, calories_a, calories_b
        )
        
        # Create response
        response_data = {
            "dishA": dish_a_data,
            "dishB": dish_b_data,
            "suggestion": suggestion,
            "meta": {
                "model": "openai-gpt-4o-mini",
                "generated_at": datetime.utcnow().isoformat(),
                "calorie_difference": abs(calories_a - calories_b),
                "lighter_dish": request.dishA if calories_a < calories_b else request.dishB
            }
        }
        
        logger.info(f"✅ Compared '{request.dishA}' ({calories_a} cal) vs '{request.dishB}' ({calories_b} cal)")
        return CompareResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Comparison failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compare dishes: {str(e)}"
        )


@app.get("/api/weekly", response_model=WeeklyResponse)
async def get_weekly_snapshot(
    start: str,
    end: str,
    db: Session = Depends(get_db)
):
    """
    Get weekly snapshot with chart and summary
    """
    try:
        from services.service_manager import service_manager
        from services.chart_service import chart_service
        from database import UserMeal
        from datetime import datetime
        
        # Validate date format
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d')
            end_date = datetime.strptime(end, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD"
            )
        
        # Query user meals for the date range
        meals = db.query(UserMeal).filter(
            UserMeal.consumed_at >= start_date,
            UserMeal.consumed_at <= end_date + timedelta(days=1)  # Include end date
        ).all()
        
        # Convert to list of dictionaries
        meal_data = [
            {
                'dish_name': meal.dish_name,
                'meal_type': meal.meal_type,
                'calories': meal.calories,
                'consumed_at': meal.consumed_at
            }
            for meal in meals
        ]
        
        # Calculate total calories
        total_calories = sum(meal['calories'] for meal in meal_data)
        
        # Calculate average per day
        date_diff = (end_date - start_date).days + 1
        avg_per_day = total_calories // date_diff if date_diff > 0 else 0
        
        # Generate chart
        chart_url = await chart_service.generate_weekly_chart(meal_data, start, end)
        
        # Generate summary
        date_range_str = f"{start} to {end}"
        summary = await service_manager.generate_weekly_summary(
            total_calories, date_range_str, avg_per_day
        )
        
        # Prepare additional statistics
        meal_count = len(meal_data)
        unique_dishes = len(set(meal['dish_name'] for meal in meal_data))
        
        # Most consumed dish
        if meal_data:
            dish_counts = {}
            for meal in meal_data:
                dish_counts[meal['dish_name']] = dish_counts.get(meal['dish_name'], 0) + 1
            most_consumed = max(dish_counts.items(), key=lambda x: x[1])
        else:
            most_consumed = None
        
        # Create response
        response_data = {
            "total_calories": total_calories,
            "chart_url": chart_url,
            "summary": summary,
            "date_range": {"start": start, "end": end},
            "meta": {
                "model": "matplotlib",
                "generated_at": datetime.utcnow().isoformat(),
                "meal_count": meal_count,
                "unique_dishes": unique_dishes,
                "avg_calories_per_day": avg_per_day,
                "days_in_range": date_diff,
                "most_consumed_dish": most_consumed[0] if most_consumed else None,
                "most_consumed_count": most_consumed[1] if most_consumed else 0
            }
        }
        
        logger.info(f"✅ Generated weekly snapshot for {start} to {end}: {total_calories} total calories")
        return WeeklyResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Weekly snapshot failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate weekly snapshot: {str(e)}"
        )


# Admin Endpoints

@app.post("/admin/dish")
async def add_dish(
    dish: DishModel,
    db: Session = Depends(get_db)
):
    """
    Add or update a dish in the database
    """
    try:
        from database import Dish
        
        # Check if dish exists
        existing_dish = db.query(Dish).filter(Dish.name == dish.name).first()
        
        if existing_dish:
            # Update existing dish
            existing_dish.calories = dish.calories
            existing_dish.meal_type = dish.meal_type
            existing_dish.description = dish.description
            existing_dish.updated_at = datetime.utcnow()
            message = f"Updated dish: {dish.name}"
        else:
            # Create new dish
            new_dish = Dish(
                name=dish.name,
                calories=dish.calories,
                meal_type=dish.meal_type,
                description=dish.description
            )
            db.add(new_dish)
            message = f"Added new dish: {dish.name}"
        
        db.commit()
        return {"message": message, "status": "success"}
        
    except Exception as e:
        logger.error(f"Failed to add/update dish: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add/update dish: {str(e)}"
        )

@app.post("/admin/user_meal")
async def add_user_meal(
    user_meal: UserMealEntry,
    db: Session = Depends(get_db)
):
    """
    Add or update a user meal in the database
    """
    try:
        from database import UserMeal
        
        # Check if user_meal exists
        existing_entry = db.query(UserMeal).filter(UserMeal.name == user_meal.name).first()
        
        if existing_entry:
            # Update existing user_meal
            existing_entry.dish_name = user_meal.dish_name
            existing_entry.meal_type = user_meal.meal_type
            existing_entry.calories = user_meal.calories
            existing_entry.consumed_at = user_meal.consumed_at
            message = f"Updated user_meal: {user_meal}"
        else:
            # Create new user_meal
            new_entry = UserMeal(
                dish_name=user_meal.dish_name,
                meal_type=user_meal.meal_type,
                calories=user_meal.calories,
                consumed_at=user_meal.consumed_at
            )
            db.add(new_entry)
            message = f"Added new user_meal: {user_meal}"
        
        db.commit()
        return {"message": message, "status": "success"}
        
    except Exception as e:
        logger.error(f"Failed to add/update user_meal: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add/update user_meal: {str(e)}"
        )

@app.post("/admin/cache/clear")
async def clear_cache(
    dish_name: str,
    db: Session = Depends(get_db)
):
    """
    Clear cache for a specific dish
    """
    try:
        from database import Cache
        
        # Delete cache entries for the dish
        deleted_count = db.query(Cache).filter(
            Cache.dish_name == dish_name
        ).delete()
        
        db.commit()
        
        return {
            "message": f"Cleared {deleted_count} cache entries for {dish_name}",
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}"
        )


# Error handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "error_code": f"HTTP_{exc.status_code}",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)