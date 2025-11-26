"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime


class PreviewRequest(BaseModel):
    """Request model for daily preview generation"""
    dish: str = Field(..., min_length=1, max_length=100, description="Name of the dish")
    meal: str = Field(..., description="Meal type (breakfast, lunch, dinner, snack)")

    class Config:
        schema_extra = {
            "example": {"dish": "aloo paratha", "meal": "lunch"}
        }


class PreviewMeta(BaseModel):
    model: str
    generated_at: str  # ISO datetime string


class PreviewResponse(BaseModel):
    """Response model for daily preview"""
    dish: str
    calories: int
    image_url: str
    captions: Dict[str, str]
    meta: PreviewMeta


class CompareMeta(BaseModel):
    model: str
    generated_at: str
    calorie_difference: int  # changed to int for numeric semantics
    lighter_dish: Optional[str] = None


class CompareRequest(BaseModel):
    """Request model for dish comparision"""
    dishA: str = Field(..., min_length=1, max_length=100, description="First dish name")
    dishB: str = Field(..., min_length=1, max_length=100, description="Second dish name")

    class Config:
        schema_extra = {
            "example": {
                "dishA": "rajma",
                "dishB": "dal tadka"
            }
        }


class CompareResponse(BaseModel):
    """Response model for dish comparison"""
    dishA: Dict[str, Any]
    dishB: Dict[str, Any]
    suggestion: str
    meta: CompareMeta


class WeeklyMeta(BaseModel):
    model: str
    generated_at: str
    meal_count: int
    unique_dishes: int
    avg_calories_per_day: int
    days_in_range: int
    most_consumed_dish: Optional[str] = None
    most_consumed_count: int


class WeeklyResponse(BaseModel):
    """Response model for weekly snapshot"""
    total_calories: int
    chart_url: str
    summary: str
    date_range: Dict[str, str]
    meta: WeeklyMeta


class DishModel(BaseModel):
    """Model for dish data"""
    name: str = Field(..., min_length=1, max_length=100)
    calories: int = Field(..., gt=0, description="Calories per serving")
    meal_type: Optional[str] = Field(None, description="Preferred meal type")
    description: Optional[str] = Field(None, max_length=500, description="Dish description")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "paneer tikka",
                "calories": 320,
                "meal_type": "snack",
                "description": "Grilled cottage cheese with spices"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: bool = True
    message: str
    error_code: str
    fallback_used: bool = False
    timestamp: str
    
    class Config:
        schema_extra = {
            "example": {
                "error": True,
                "message": "External API temporarily unavailable",
                "error_code": "API_TIMEOUT",
                "fallback_used": True,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class CacheEntry(BaseModel):
    """Model for cache entries"""
    dish_name: str
    cache_type: str  # 'preview', 'image', 'caption'
    cache_data: str  # JSON string
    expires_at: Optional[datetime] = None


class UserMealEntry(BaseModel):
    """Model for user meal tracking"""
    dish_name: str
    meal_type: str
    calories: Optional[int] = None
    consumed_at: Optional[datetime] = None