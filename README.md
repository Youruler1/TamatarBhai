# 🍅 Tamatar-Bhai MVP

A 1-day MVP web application that provides AI-powered food insights with a friendly "bhai style" personality. Get nutritional information, visual representations of dishes, and personalized recommendations using OpenAI and StabilityAI.

## ✨ Features

- **Daily Preview**: AI-generated dish images, calories, and dual captions (bhai style + formal)
- **Switch-up Diff**: Compare two dishes with bhai-style recommendations  
- **Weekly Snapshot**: Visual charts and summaries of your eating patterns
- **Admin Panel**: Manage dishes and clear cache

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key
- StabilityAI API key

### Setup

1. **Clone and navigate to the repository**
   ```bash
   git clone <repository-url>
   cd tamatar-bhai-mvp
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # OPENAI_API_KEY=your_openai_key_here
   # STABILITY_KEY=your_stability_key_here
   ```

3. **Run the demo**
   ```bash
   ./run_demo.sh
   ```

   Or manually:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🎯 Demo Flow

1. **Daily Preview Tab**
   - Enter dish: "aloo paratha"
   - Select meal: "lunch"
   - Get AI-generated image, calories, and bhai + formal captions

2. **Switch-up Diff Tab**
   - Compare: "rajma" vs "dal"
   - Get calorie comparison and bhai-style recommendation

3. **Weekly Snapshot Tab**
   - Select date range
   - View calorie chart and formal summary

## 🏗️ Architecture

```
Frontend (React + Vite) ←→ Backend (FastAPI) ←→ External APIs
     ↓                           ↓                (OpenAI + StabilityAI)
Static Files              SQLite Database
                         + File Storage
```

### Tech Stack
- **Frontend**: React, TypeScript, Vite, TailwindCSS
- **Backend**: FastAPI, SQLAlchemy, SQLite
- **AI Services**: OpenAI (gpt-4o-mini), StabilityAI (stable-diffusion-2)
- **Charts**: Matplotlib
- **Containerization**: Docker + Docker Compose

## 📁 Project Structure

```
tamatar-bhai-mvp/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── models/                # Database models
│   ├── services/              # External API services
│   ├── Dockerfile
│   ├── requirements.txt
│   └── model_routes.json      # API routing config
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   └── services/         # API client
│   ├── Dockerfile
│   └── package.json
├── data/
│   ├── nutrition_lookup.csv   # Nutrition database
│   └── images/               # Generated images
├── docker-compose.yml
├── .env.example
├── run_demo.sh
└── README.md
```

## 🔧 API Endpoints

### Core Endpoints
- `POST /api/preview` - Generate daily preview with image, calories, and captions
- `GET /api/dishes` - List all dishes in the database
- `POST /api/compare` - Compare two dishes with bhai-style recommendation
- `GET /api/weekly` - Get weekly snapshot with chart and summary

### Admin Endpoints
- `POST /admin/dish` - Add or edit dish information
- `POST /admin/cache/clear` - Clear cached data for specific dish

### System Endpoints
- `GET /health` - Health check endpoint for monitoring
- `GET /docs` - Interactive API documentation (Swagger UI)

### Request/Response Examples

**Daily Preview Request:**
```json
{
  "dish": "butter chicken",
  "meal": "lunch"
}
```

**Daily Preview Response:**
```json
{
  "dish": "Butter Chicken",
  "calories": 400,
  "image_url": "/data/images/butter_chicken_123.png",
  "captions": {
    "bhai": "Bhai, yeh butter chicken full creamy aur tasty hai! 400 calories ka maza le lo! 🤤",
    "formal": "Butter chicken is a rich and creamy North Indian dish with tender chicken in tomato-based sauce."
  },
  "meta": {
    "model": "openai-gpt-4o-mini",
    "generated_at": "2024-01-15T10:30:00Z",
    "matched_dish": "Butter Chicken",
    "confidence": 0.95
  }
}
```

## 🎨 "Bhai Style" Personality

The app uses a friendly Indian college student persona:
- **Hinglish**: Mix of English and Hindi
- **Casual tone**: "Bhai, yeh dish full mazedaar hai!"
- **Light humor**: Informal but respectful
- **Short & punchy**: 1-2 lines max

## 🛠️ Development

### Local Development
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app:app --reload

# Frontend  
cd frontend
npm install
npm run dev
```

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_key
STABILITY_KEY=your_stability_key
DATABASE_URL=sqlite:///./data/tamatar_bhai.db
CACHE_TTL_HOURS=24
MAX_IMAGE_SIZE_MB=5
DEBUG=false
```

## 🔍 Troubleshooting

### Common Issues

**Docker not starting?**
- Ensure Docker Desktop is running
- Check port availability (3000, 8000)

**API keys not working?**
- Verify keys in .env file
- Check API key permissions and quotas

**Services not responding?**
- Wait 30-60 seconds for full startup
- Check logs: `docker-compose logs -f`

**Database issues?**
- Delete data/tamatar_bhai.db and restart
- Check file permissions in data/ directory

### Logs and Debugging
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Clean rebuild
docker-compose down
docker-compose up --build
```

## 📊 Sample Data

The app includes 50+ Indian dishes in `data/nutrition_lookup.csv`:
- Aloo Paratha (320 cal)
- Rajma (245 cal)  
- Dal Tadka (180 cal)
- Butter Chicken (400 cal)
- And many more...

## 🚫 Limitations

- **1-day MVP scope**: Basic functionality only
- **External API dependency**: Requires internet and API keys
- **Local deployment**: Not production-ready
- **Sample data**: Limited nutrition database

## 🧪 Testing

### Validation Script
Run the built-in validation to check project setup:
```bash
python test_simple.py
```

### Manual Testing
1. **Health Checks**
   - Backend: http://localhost:8000/health
   - Frontend: http://localhost:3000

2. **API Testing**
   - Interactive docs: http://localhost:8000/docs
   - Test endpoints with sample data

3. **Feature Testing**
   - Try different dish names and meal types
   - Test error scenarios (invalid inputs)
   - Verify image generation and fallbacks

## 🔒 Security Notes

- API keys are stored in environment variables
- Non-root users in Docker containers
- Input validation on all endpoints
- No sensitive data in logs or responses

## 📈 Performance

- **Caching**: SQLite-based caching for API responses
- **Images**: Local storage with fallback mechanisms  
- **Loading**: Skeleton screens for better UX
- **Timeouts**: 30-second API timeouts with retry logic

## 🌐 External Dependencies

### Required APIs
- **OpenAI**: Text generation (captions, summaries, recommendations)
- **StabilityAI**: Image generation for dishes

### Fallback Behavior
- Images: Placeholder when StabilityAI fails
- Text: Template responses when OpenAI fails
- Data: Fuzzy matching for dish names

## 🤝 Contributing

This is a 1-day MVP. For production use:
1. Add comprehensive error handling
2. Implement user authentication
3. Add data validation and sanitization
4. Scale database and caching
5. Add comprehensive testing
6. Implement rate limiting
7. Add monitoring and logging
8. Optimize for mobile devices

## 📄 License

MIT License - See LICENSE file for details

---

**Built with ❤️ for the Tamatar-Bhai community**

*"Bhai, khana khao aur mast raho!" 🍽️*