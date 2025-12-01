# Tamatar-Bhai API Reference

**Base URL**: `http://localhost:8000`  
**Version**: 1.0.0  
**Documentation**: http://localhost:8000/docs

---

## 📋 Complete Endpoint List

### System Endpoints (3)
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Swagger documentation

### Core API Endpoints (5)
- `POST /api/preview` - Generate daily preview
- `GET /api/dishes` - List all dishes
- `GET /api/user_meals` - List all user meals
- `POST /api/compare` - Compare two dishes
- `GET /api/weekly` - Get weekly snapshot

### Admin Endpoints (3)
- `POST /admin/dish` - Add/edit dishes
- `POST /admin/user_meal` - Add/edit user meals
- `POST /admin/cache/clear` - Clear cache

**Total: 11 endpoints**

---

## 🔧 System Endpoints

### GET /
**Description**: Root endpoint with welcome message

**Response**:
```json
{
  "message": "🍅 Welcome to Tamatar-Bhai MVP API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### GET /health
**Description**: Health check endpoint for monitoring

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-12-01T10:30:00.000Z",
  "service": "tamatar-bhai-api"
}
```

---

### GET /docs
**Description**: Interactive Swagger API documentation

**Response**: HTML page with Swagger UI

---

## 🍽️ Core API Endpoints

### POST /api/preview
**Description**: Generate daily preview with image, calories, and captions

**Request Body**:
```json
{
  "dish": "aloo paratha",
  "meal": "lunch"
}
```

**Parameters**:
- `dish` (string, required): Name of the dish
- `meal` (string, required): Meal type (breakfast, lunch, dinner, snack)

**Response** (200 OK):
```json
{
  "dish": "Aloo Paratha",
  "calories": 320,
  "image_url": "/data/images/aloo_paratha_1733058600.png",
  "captions": {
    "bhai": "Bhai, yeh aloo paratha full mazedaar hai - calories thodi zyada but worth it!",
    "formal": "Aloo paratha is a nutritious stuffed flatbread providing good energy for lunch."
  },
  "meta": {
    "model": "openai/gpt-oss-120b",
    "generated_at": "2024-12-01T10:30:00.000Z",
    "matched_dish": "Aloo Paratha",
    "confidence": 95
  }
}
```

**Features**:
- Generates AI image using StabilityAI
- Looks up calories using fuzzy matching
- Generates bhai-style and formal captions using OpenAI
- Caches results for 24 hours
- Tracks meal in user_meals table

**Error Response** (500):
```json
{
  "error": true,
  "message": "Failed to generate preview: ...",
  "error_code": "HTTP_500",
  "timestamp": "2024-12-01T10:30:00.000Z"
}
```

---

### GET /api/dishes
**Description**: Get list of all available dishes from nutrition database

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Aloo Paratha",
    "calories": 320,
    "meal_type": "breakfast",
    "description": "Stuffed flatbread with spiced potato filling"
  },
  {
    "id": 2,
    "name": "Rajma",
    "calories": 245,
    "meal_type": "lunch",
    "description": "Red kidney beans curry"
  }
  // ... more dishes
]
```

**Use Case**: Display dish suggestions, autocomplete, or browse available dishes

---

### GET /api/user_meals
**Description**: Get list of all user meal entries (for weekly tracking)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "dish_name": "Aloo Paratha",
    "meal_type": "lunch",
    "calories": 320,
    "consumed_at": "2024-12-01T12:30:00.000Z"
  },
  {
    "id": 2,
    "dish_name": "Rajma",
    "meal_type": "dinner",
    "calories": 245,
    "consumed_at": "2024-12-01T19:00:00.000Z"
  }
  // ... more meals
]
```

**Use Case**: Display meal history, calculate statistics, or export data

---

### POST /api/compare
**Description**: Compare two dishes and get bhai-style recommendation

**Request Body**:
```json
{
  "dishA": "rajma",
  "dishB": "dal tadka"
}
```

**Parameters**:
- `dishA` (string, required): First dish name
- `dishB` (string, required): Second dish name

**Response** (200 OK):
```json
{
  "dishA": {
    "name": "rajma",
    "calories": 245,
    "matched_name": "Rajma",
    "confidence": 100,
    "protein_g": 15.0,
    "carbs_g": 35.0,
    "fat_g": 5.0
  },
  "dishB": {
    "name": "dal tadka",
    "calories": 180,
    "matched_name": "Dal Tadka",
    "confidence": 100,
    "protein_g": 12.0,
    "carbs_g": 28.0,
    "fat_g": 3.0
  },
  "suggestion": "Bhai, dal tadka is lighter at 180 calories - better choice if gym ka plan hai!",
  "meta": {
    "model": "openai/gpt-oss-120b",
    "generated_at": "2024-12-01T10:30:00.000Z",
    "calorie_difference": 65,
    "lighter_dish": "dal tadka"
  }
}
```

**Features**:
- Fuzzy matches both dish names
- Retrieves nutritional information
- Generates bhai-style comparison using OpenAI
- Calculates calorie difference

---

### GET /api/weekly
**Description**: Get weekly snapshot with chart and summary

**Query Parameters**:
- `start` (string, required): Start date in YYYY-MM-DD format
- `end` (string, required): End date in YYYY-MM-DD format

**Example Request**:
```
GET /api/weekly?start=2024-11-25&end=2024-12-01
```

**Response** (200 OK):
```json
{
  "total_calories": 14700,
  "chart_url": "/data/images/weekly_chart_20241201_103000.png",
  "summary": "Your weekly intake totaled 14,700 calories with an average of 2,100 calories per day. This shows a consistent eating pattern with moderate caloric consumption. The distribution is well-balanced across meals with moderate variation.",
  "date_range": {
    "start": "2024-11-25",
    "end": "2024-12-01"
  },
  "meta": {
    "model": "matplotlib",
    "generated_at": "2024-12-01T10:30:00.000Z",
    "meal_count": 21,
    "unique_dishes": 15,
    "avg_calories_per_day": 2100,
    "days_in_range": 7,
    "most_consumed_dish": "Aloo Paratha",
    "most_consumed_count": 3
  }
}
```

**Features**:
- Queries user_meals table for date range
- Generates bar chart using matplotlib
- Generates formal summary using OpenAI
- Calculates statistics (total, average, most consumed)

**Error Response** (400):
```json
{
  "error": true,
  "message": "Invalid date format. Use YYYY-MM-DD",
  "error_code": "HTTP_400",
  "timestamp": "2024-12-01T10:30:00.000Z"
}
```

---

## 🔐 Admin Endpoints

### POST /admin/dish
**Description**: Add or update a dish in the nutrition database

**Request Body**:
```json
{
  "name": "Paneer Tikka",
  "calories": 320,
  "meal_type": "snack",
  "description": "Grilled cottage cheese with spices"
}
```

**Parameters**:
- `name` (string, required): Dish name
- `calories` (integer, required): Calories per serving (must be > 0)
- `meal_type` (string, optional): Preferred meal type
- `description` (string, optional): Dish description (max 500 chars)

**Response** (200 OK):
```json
{
  "message": "Added new dish: Paneer Tikka",
  "status": "success"
}
```

**Behavior**:
- If dish exists: Updates existing entry
- If dish doesn't exist: Creates new entry
- Updates `updated_at` timestamp

---

### POST /admin/user_meal
**Description**: Add or update a user meal entry

**Request Body**:
```json
{
  "dish_name": "Aloo Paratha",
  "meal_type": "lunch",
  "calories": 320,
  "consumed_at": "2024-12-01T12:30:00.000Z"
}
```

**Parameters**:
- `dish_name` (string, required): Name of the dish
- `meal_type` (string, required): Meal type
- `calories` (integer, optional): Calories (auto-filled from dishes table if not provided)
- `consumed_at` (datetime, optional): When meal was consumed (defaults to now)

**Response** (200 OK):
```json
{
  "message": "Added new user_meal: ...",
  "status": "success"
}
```

**Use Case**: Manually add meal entries, import data, or correct entries

---

### POST /admin/cache/clear
**Description**: Clear cached data for a specific dish

**Query Parameters**:
- `dish_name` (string, required): Name of the dish to clear cache for

**Example Request**:
```
POST /admin/cache/clear?dish_name=aloo%20paratha
```

**Response** (200 OK):
```json
{
  "message": "Cleared 3 cache entries for aloo paratha",
  "status": "success"
}
```

**Behavior**:
- Deletes all cache entries (preview, image, captions) for the dish
- Returns count of deleted entries
- Case-insensitive matching

**Use Case**: Force regeneration of content, clear stale cache, or test API calls

---

## 🔄 Caching Behavior

### Cache Types
1. **Preview Cache**: Complete preview response (24 hour TTL)
2. **Image Cache**: Generated image URL (7 day TTL)
3. **Captions Cache**: Bhai and formal captions (24 hour TTL)

### Cache Keys
- Normalized dish name (lowercase, trimmed)
- Example: "Aloo Paratha" → "aloo paratha"

### Cache Flow
1. First request: Generate content → Cache → Return
2. Subsequent requests: Check cache → Return cached data
3. After TTL expires: Regenerate content → Update cache

---

## 🎯 Fuzzy Matching

### How It Works
- Uses `fuzzywuzzy` library with ratio scorer
- Threshold: 70% similarity
- Case-insensitive matching

### Examples
| User Input | Matched Dish | Confidence |
|------------|--------------|------------|
| "aloo paratha" | "Aloo Paratha" | 100% |
| "alo paratha" | "Aloo Paratha" | 92% |
| "butter chiken" | "Butter Chicken" | 93% |
| "rajma chawal" | "Rajma" | 75% |

### Fallback
If no match found (< 70% similarity):
- Estimates calories based on dish type patterns
- Returns confidence: 0
- Uses original dish name

---

## 🚨 Error Handling

### Error Response Format
```json
{
  "error": true,
  "message": "Error description",
  "error_code": "HTTP_XXX",
  "timestamp": "2024-12-01T10:30:00.000Z"
}
```

### Common Error Codes
- `400` - Bad Request (invalid input)
- `404` - Not Found (endpoint doesn't exist)
- `500` - Internal Server Error (API failure, database error)

### Fallback Behavior
When external APIs fail:
- **OpenAI fails**: Uses template-based captions
- **StabilityAI fails**: Uses placeholder image
- **Database fails**: Returns error with graceful message

---

## 🧪 Testing Endpoints

### Using curl

**Health Check**:
```bash
curl http://localhost:8000/health
```

**Generate Preview**:
```bash
curl -X POST http://localhost:8000/api/preview \
  -H "Content-Type: application/json" \
  -d '{"dish":"aloo paratha","meal":"lunch"}'
```

**Compare Dishes**:
```bash
curl -X POST http://localhost:8000/api/compare \
  -H "Content-Type: application/json" \
  -d '{"dishA":"rajma","dishB":"dal tadka"}'
```

**Get Weekly Snapshot**:
```bash
curl "http://localhost:8000/api/weekly?start=2024-11-25&end=2024-12-01"
```

**List Dishes**:
```bash
curl http://localhost:8000/api/dishes
```

**List User Meals**:
```bash
curl http://localhost:8000/api/user_meals
```

**Clear Cache**:
```bash
curl -X POST "http://localhost:8000/admin/cache/clear?dish_name=aloo%20paratha"
```

### Using Swagger UI
1. Open http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. View response

---

## 📝 Notes

### CORS Configuration
Backend is configured to allow requests from:
- `http://localhost:3000` (production frontend)
- `http://frontend:3000` (Docker frontend)
- `http://localhost:5173` (Vite dev server)

### Static Files
Images and charts are served at:
- `/data/images/` - Generated dish images
- `/data/images/` - Weekly chart PNGs

### Database
- SQLite database at `data/tamatar_bhai.db`
- 3 tables: `dishes`, `cache`, `user_meals`
- Initialized on startup

### Rate Limiting
- No rate limiting implemented (MVP)
- External APIs have their own rate limits

---

## 🔗 Related Documentation

- **CURRENT_STATUS.md** - Project status and overview
- **FRONTEND_QUICK_START.md** - Frontend setup guide
- **tasks.md** - Implementation tasks
- **design.md** - System architecture
- **requirements.md** - Feature requirements

---

**Last Updated**: December 2024  
**API Version**: 1.0.0
