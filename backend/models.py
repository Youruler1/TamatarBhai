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
            "example": {
                "dish": "aloo paratha",
                "meal": "lunch"
            }
        }


class PreviewResponse(BaseModel):
    """Response model for daily preview"""
    dish: str
    calories: int
    image_url: str
    captions: Dict[str, str]  # {"bhai": "...", "formal": "..."}
    meta: Dict[str, str]      # {"model": "openai-gpt-4o-mini"}
    
    class Config:
        schema_extra = {
            "example": {
                "dish": "aloo paratha",
                "calories": 320,
                "image_url": "/data/images/aloo_paratha_123456.png",
                "captions": {
                    "bhai": "Bhai, yeh aloo paratha full mazedaar hai - calories thodi zyada but worth it!",
                    "formal": "Aloo paratha is a nutritious stuffed flatbread providing good energy for lunch."
                },
                "meta": {
                    "model": "openai-gpt-4o-mini",
                    "generated_at": "2024-01-15T10:30:00Z"
                }
            }
        }


class CompareRequest(BaseModel):
    """Request model for dish comparison"""
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
    dishA: Dict[str, Any]     # {"name": "...", "calories": 320}
    dishB: Dict[str, Any]     # {"name": "...", "calories": 280}
    suggestion: str           # Bhai-style recommendation
    meta: Dict[str, str]
    
    class Config:
        schema_extra = {
            "example": {
                "dishA": {"name": "rajma", "calories": 245},
                "dishB": {"name": "dal tadka", "calories": 180},
                "suggestion": "Bhai, dal tadka is lighter - better choice if gym ka plan hai!",
                "meta": {
                    "model": "openai-gpt-4o-mini",
                    "generated_at": "2024-01-15T10:30:00Z"
                }
            }
        }


class WeeklyResponse(BaseModel):
    """Response model for weekly snapshot"""
    total_calories: int
    chart_url: str
    summary: str
    date_range: Dict[str, str]  # {"start": "...", "end": "..."}
    meta: Dict[str, str]
    
    class Config:
        schema_extra = {
            "example": {
                "total_calories": 14700,
                "chart_url": "/data/images/weekly_chart_20240115.png",
                "summary": "Your weekly intake shows consistent patterns with an average of 2100 calories per day. The distribution is well-balanced across meals with moderate variation.",
                "date_range": {
                    "start": "2024-01-08",
                    "end": "2024-01-14"
                },
                "meta": {
                    "model": "matplotlib",
                    "generated_at": "2024-01-15T10:30:00Z"
                }
            }
        }


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
    calories: int
    consumed_at: Optional[datetime] = None