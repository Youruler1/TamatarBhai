"""
Comprehensive error handling for Tamatar-Bhai MVP
"""

import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)

class TamatarBhaiError(Exception):
    """Base exception for Tamatar-Bhai application"""
    def __init__(self, message: str, error_code: str = "GENERAL_ERROR", details: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class ExternalAPIError(TamatarBhaiError):
    """Exception for external API failures"""
    def __init__(self, service: str, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"{service} API error: {message}",
            error_code=f"{service.upper()}_API_ERROR",
            details=details
        )
        self.service = service

class DatabaseError(TamatarBhaiError):
    """Exception for database operations"""
    def __init__(self, operation: str, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"Database {operation} error: {message}",
            error_code="DATABASE_ERROR",
            details=details
        )
        self.operation = operation

class ValidationError(TamatarBhaiError):
    """Exception for data validation errors"""
    def __init__(self, field: str, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"Validation error for {field}: {message}",
            error_code="VALIDATION_ERROR",
            details=details
        )
        self.field = field

class CacheError(TamatarBhaiError):
    """Exception for cache operations"""
    def __init__(self, operation: str, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"Cache {operation} error: {message}",
            error_code="CACHE_ERROR",
            details=details
        )

def create_error_response(
    error: Exception,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    fallback_used: bool = False
) -> Dict[str, Any]:
    """Create standardized error response"""
    
    error_response = {
        "error": True,
        "message": str(error),
        "timestamp": datetime.utcnow().isoformat(),
        "fallback_used": fallback_used
    }
    
    # Add specific error details for custom exceptions
    if isinstance(error, TamatarBhaiError):
        error_response["error_code"] = error.error_code
        if error.details:
            error_response["details"] = error.details
    else:
        error_response["error_code"] = "INTERNAL_ERROR"
    
    return error_response

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            Exception(exc.detail),
            status_code=exc.status_code
        )
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    logger.error(f"Validation Error: {exc.errors()}")
    
    error_details = {
        "validation_errors": exc.errors(),
        "body": exc.body if hasattr(exc, 'body') else None
    }
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=create_error_response(
            ValidationError("request", "Invalid request data", error_details),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unhandled Exception: {type(exc).__name__}: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    # Don't expose internal errors in production
    error_message = "An internal server error occurred"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_error_response(
            Exception(error_message),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    )

async def tamatar_bhai_exception_handler(request: Request, exc: TamatarBhaiError):
    """Handle custom Tamatar-Bhai exceptions"""
    logger.error(f"Tamatar-Bhai Error: {exc.error_code} - {exc.message}")
    
    # Determine appropriate status code based on error type
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if isinstance(exc, ValidationError):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, ExternalAPIError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    elif isinstance(exc, DatabaseError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    elif isinstance(exc, CacheError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    return JSONResponse(
        status_code=status_code,
        content=create_error_response(exc, status_code)
    )

def setup_error_handlers(app):
    """Setup all error handlers for the FastAPI app"""
    
    # Custom exception handlers
    app.add_exception_handler(TamatarBhaiError, tamatar_bhai_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    logger.info("✅ Error handlers configured")

# Utility functions for common error scenarios
def handle_external_api_failure(service: str, operation: str, error: Exception, fallback_data: Any = None):
    """Handle external API failures with fallback"""
    logger.warning(f"🔄 {service} API failed for {operation}: {error}")
    
    if fallback_data is not None:
        logger.info(f"✅ Using fallback data for {service} {operation}")
        return fallback_data
    
    raise ExternalAPIError(
        service=service,
        message=f"Failed to {operation}",
        details={"original_error": str(error)}
    )

def handle_database_failure(operation: str, error: Exception, fallback_action: Optional[callable] = None):
    """Handle database failures with optional fallback"""
    logger.error(f"💾 Database {operation} failed: {error}")
    
    if fallback_action:
        try:
            return fallback_action()
        except Exception as fallback_error:
            logger.error(f"❌ Fallback action also failed: {fallback_error}")
    
    raise DatabaseError(
        operation=operation,
        message=str(error),
        details={"original_error": str(error)}
    )

def validate_dish_name(dish_name: str) -> str:
    """Validate and sanitize dish name"""
    if not dish_name or not dish_name.strip():
        raise ValidationError("dish_name", "Dish name cannot be empty")
    
    # Sanitize input
    sanitized = dish_name.strip()
    
    if len(sanitized) > 100:
        raise ValidationError("dish_name", "Dish name too long (max 100 characters)")
    
    # Check for potentially harmful characters
    forbidden_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
    if any(char in sanitized for char in forbidden_chars):
        raise ValidationError("dish_name", "Dish name contains invalid characters")
    
    return sanitized

def validate_meal_type(meal_type: str) -> str:
    """Validate meal type"""
    valid_meals = ['breakfast', 'lunch', 'dinner', 'snack']
    
    if not meal_type or meal_type.lower() not in valid_meals:
        raise ValidationError(
            "meal_type", 
            f"Invalid meal type. Must be one of: {', '.join(valid_meals)}"
        )
    
    return meal_type.lower()

def validate_date_range(start_date: str, end_date: str) -> tuple:
    """Validate date range for weekly snapshots"""
    try:
        from datetime import datetime
        
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        if start > end:
            raise ValidationError("date_range", "Start date must be before end date")
        
        # Check if date range is reasonable (not more than 1 year)
        if (end - start).days > 365:
            raise ValidationError("date_range", "Date range too large (max 1 year)")
        
        return start, end
        
    except ValueError as e:
        raise ValidationError("date_range", f"Invalid date format: {e}")

# Logging configuration
def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('tamatar_bhai.log')
        ]
    )
    
    # Set specific log levels for external libraries
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    logger.info("✅ Logging configured")