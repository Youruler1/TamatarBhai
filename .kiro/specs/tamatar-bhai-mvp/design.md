# Design Document

## Overview

Tamatar-Bhai MVP is a containerized full-stack web application that provides AI-powered food insights with a friendly "bhai style" personality. The system integrates with OpenAI for text generation and StabilityAI for image generation, while maintaining local caching and fallback mechanisms for reliability.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │  External APIs  │
│   (React)       │◄──►│   (FastAPI)     │◄──►│  OpenAI/Stability│
│   Port: 3000    │    │   Port: 8000    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       
         │                       │                       
         ▼                       ▼                       
┌─────────────────┐    ┌─────────────────┐              
│   Static Files  │    │   Data Layer    │              
│   (Nginx)       │    │   (SQLite)      │              
└─────────────────┘    └─────────────────┘              
```

### Component Architecture

**Frontend Layer (React + Vite)**
- Tab-based navigation (Daily Preview, Switch-up, Weekly)
- Component-based architecture with reusable UI elements
- State management for API calls and caching
- Loading states and error handling

**Backend Layer (FastAPI)**
- RESTful API endpoints
- External API integration layer
- Caching and database management
- Image processing and storage

**Data Layer**
- SQLite database for structured data
- File system storage for images and charts
- CSV-based nutrition lookup
- Caching mechanism for performance

## Components and Interfaces

### Frontend Components

#### Core Components
```typescript
// App.tsx - Main application container
interface AppProps {
  theme?: 'light' | 'dark';
}

// TabNavigation.tsx - Top-level navigation
interface TabNavigationProps {
  activeTab: 'preview' | 'compare' | 'weekly';
  onTabChange: (tab: string) => void;
}

// DailyPreview.tsx - Main preview feature
interface DailyPreviewProps {
  onPreviewGenerate: (dish: string, meal: string) => Promise<PreviewResponse>;
}

// SwitchupDiff.tsx - Comparison feature
interface SwitchupDiffProps {
  onCompare: (dishA: string, dishB: string) => Promise<CompareResponse>;
}

// WeeklySnapshot.tsx - Weekly analytics
interface WeeklySnapshotProps {
  onWeeklyGenerate: (startDate: string, endDate: string) => Promise<WeeklyResponse>;
}
```

#### Shared Components
```typescript
// LoadingSkeleton.tsx - Loading states
interface LoadingSkeletonProps {
  type: 'card' | 'chart' | 'text';
  count?: number;
}

// ErrorBoundary.tsx - Error handling
interface ErrorBoundaryProps {
  fallback: React.ComponentType<{error: Error}>;
  children: React.ReactNode;
}

// ImageWithFallback.tsx - Image handling
interface ImageWithFallbackProps {
  src: string;
  alt: string;
  fallbackSrc?: string;
  className?: string;
}
```

### Backend API Interfaces

#### API Response Types
```python
# Preview Response
class PreviewResponse(BaseModel):
    dish: str
    calories: int
    image_url: str
    captions: Dict[str, str]  # {"bhai": "...", "formal": "..."}
    meta: Dict[str, str]      # {"model": "openai-gpt-4o-mini"}

# Compare Response  
class CompareResponse(BaseModel):
    dishA: Dict[str, Any]     # {"name": "...", "calories": 320}
    dishB: Dict[str, Any]     # {"name": "...", "calories": 280}
    suggestion: str           # Bhai-style recommendation
    meta: Dict[str, str]

# Weekly Response
class WeeklyResponse(BaseModel):
    total_calories: int
    chart_url: str
    summary: str
    date_range: Dict[str, str]  # {"start": "...", "end": "..."}
    meta: Dict[str, str]
```

#### Core API Endpoints
```python
# Daily Preview
@app.post("/api/preview")
async def generate_preview(request: PreviewRequest) -> PreviewResponse

# Dish Management
@app.get("/api/dishes")
async def get_dishes() -> List[Dict[str, Any]]

# Comparison
@app.post("/api/compare") 
async def compare_dishes(request: CompareRequest) -> CompareResponse

# Weekly Analytics
@app.get("/api/weekly")
async def get_weekly_snapshot(start: str, end: str) -> WeeklyResponse

# Admin Functions
@app.post("/admin/dish")
async def add_dish(dish: DishModel) -> Dict[str, str]

@app.post("/admin/cache/clear")
async def clear_cache(dish_name: str) -> Dict[str, str]
```

### External API Integration

#### OpenAI Integration
```python
class OpenAIService:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    async def generate_bhai_caption(self, dish: str, calories: int) -> str:
        """Generate bhai-style caption with explicit persona definition"""
        
    async def generate_formal_caption(self, dish: str, calories: int) -> str:
        """Generate formal caption"""
        
    async def generate_comparison_suggestion(self, dish_a: str, dish_b: str, 
                                           calories_a: int, calories_b: int) -> str:
        """Generate bhai-style comparison suggestion"""
        
    async def generate_weekly_summary(self, total_calories: int, 
                                    date_range: str) -> str:
        """Generate formal weekly summary"""
```

#### StabilityAI Integration
```python
class StabilityAIService:
    def __init__(self, api_key: str, engine: str = "stable-diffusion-2"):
        self.api_key = api_key
        self.engine = engine
        self.base_url = "https://api.stability.ai"
    
    async def generate_dish_image(self, dish: str) -> bytes:
        """Generate dish image using Stability API"""
        
    async def save_generated_image(self, image_data: bytes, 
                                 dish_name: str) -> str:
        """Save image to data/images/ and return path"""
```

### Database Schema

#### SQLite Tables
```sql
-- Dishes table
CREATE TABLE dishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    calories INTEGER,
    meal_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cache table for generated content
CREATE TABLE cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dish_name TEXT NOT NULL,
    cache_type TEXT NOT NULL, -- 'preview', 'image', 'caption'
    cache_data TEXT NOT NULL, -- JSON data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    UNIQUE(dish_name, cache_type)
);

-- User interactions for weekly tracking
CREATE TABLE user_meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dish_name TEXT NOT NULL,
    meal_type TEXT NOT NULL,
    calories INTEGER NOT NULL,
    consumed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Data Models

### Nutrition Lookup System
```python
class NutritionLookup:
    def __init__(self, csv_path: str = "data/nutrition_lookup.csv"):
        self.df = pd.read_csv(csv_path)
    
    def fuzzy_match_dish(self, dish_name: str, threshold: float = 0.8) -> Optional[Dict]:
        """Use fuzzy string matching to find closest dish"""
        
    def get_calories(self, dish_name: str) -> int:
        """Get calories for dish with fuzzy matching fallback"""
```

### Caching System
```python
class CacheManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    async def get_cached_preview(self, dish_name: str) -> Optional[Dict]:
        """Retrieve cached preview data"""
        
    async def cache_preview(self, dish_name: str, preview_data: Dict, 
                          ttl_hours: int = 24):
        """Cache preview data with TTL"""
        
    async def invalidate_cache(self, dish_name: str, cache_type: str = None):
        """Clear cache for specific dish/type"""
```

## Error Handling

### Fallback Mechanisms
```python
class FallbackManager:
    @staticmethod
    async def get_fallback_image(dish_name: str) -> str:
        """Return placeholder or web-scraped image"""
        
    @staticmethod
    def get_fallback_caption(dish_name: str, style: str) -> str:
        """Return template-based caption"""
        
    @staticmethod
    async def handle_api_failure(service: str, operation: str, 
                                fallback_data: Any) -> Any:
        """Generic API failure handler with logging"""
```

### Error Response Format
```python
class ErrorResponse(BaseModel):
    error: bool = True
    message: str
    error_code: str
    fallback_used: bool = False
    timestamp: str
```

## Testing Strategy

### Unit Testing
- API endpoint testing with FastAPI TestClient
- React component testing with Jest and React Testing Library
- External API mocking for reliable tests
- Database operations testing with in-memory SQLite

### Integration Testing
- End-to-end API workflow testing
- Docker container integration testing
- External API integration testing (with rate limiting)

### Performance Testing
- API response time benchmarking
- Image generation and caching performance
- Database query optimization testing

## Security Considerations

### API Key Management
- Environment variable storage for all API keys
- No hardcoded credentials in codebase
- Secure key rotation capability

### Input Validation
- Sanitize all user inputs for dish names
- Validate date ranges for weekly queries
- Rate limiting on API endpoints

### Data Privacy
- No personal data storage beyond meal tracking
- Local-only data processing
- Clear cache functionality for data removal

## Deployment Configuration

### Docker Setup
```yaml
# docker-compose.yml structure
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    depends_on: [backend]
    
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - STABILITY_KEY=${STABILITY_KEY}
    volumes:
      - ./data:/app/data
      
  nginx:
    image: nginx:alpine
    ports: ["80:80"]
    depends_on: [frontend, backend]
```

### Environment Configuration
```bash
# .env.example
OPENAI_API_KEY=your_openai_key_here
STABILITY_KEY=your_stability_key_here
DATABASE_URL=sqlite:///./data/tamatar_bhai.db
CACHE_TTL_HOURS=24
MAX_IMAGE_SIZE_MB=5
DEBUG=false
```

This design provides a robust, scalable foundation for the Tamatar-Bhai MVP while maintaining simplicity for the 1-day development timeline.