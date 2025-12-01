# Frontend Quick Start Guide

This guide will help you build the Tamatar-Bhai frontend from scratch in the most efficient way possible.

---

## 🎯 Goal

Build a React + Vite + TypeScript frontend that connects to the existing, tested backend API.

---

## 📋 Prerequisites

- Node.js 18+ installed
- Backend running at http://localhost:8000
- Basic knowledge of React, TypeScript, and TailwindCSS

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Frontend Project

```bash
# From project root
npm create vite@latest frontend -- --template react-ts
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
npm install axios lucide-react date-fns
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Step 3: Configure TailwindCSS

**tailwind.config.js:**
```js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        tomato: {
          50: '#fff5f5',
          500: '#ef4444',
          600: '#dc2626',
        }
      }
    },
  },
  plugins: [],
}
```

**src/index.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer utilities {
  .fade-in {
    animation: fadeIn 0.3s ease-in;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
}
```

### Step 4: Create Environment File

**frontend/.env:**
```bash
VITE_API_BASE_URL=http://localhost:8000
```

---

## 📁 Folder Structure

Create this structure in `frontend/src/`:

```
src/
├── components/
│   ├── ErrorBoundary.tsx
│   ├── ImageWithFallback.tsx
│   ├── LoadingSkeleton.tsx
│   └── TabNavigation.tsx
├── pages/
│   ├── DailyPreview.tsx
│   ├── SwitchupDiff.tsx
│   └── WeeklySnapshot.tsx
├── services/
│   └── api.ts
├── types/
│   └── api.ts
├── App.tsx
├── App.css
├── main.tsx
└── index.css
```

---

## 🔌 API Service (Copy & Paste)

**src/types/api.ts:**
```typescript
export interface PreviewRequest {
  dish: string;
  meal: string;
}

export interface PreviewResponse {
  dish: string;
  calories: number;
  image_url: string;
  captions: {
    bhai: string;
    formal: string;
  };
  meta: {
    model: string;
    generated_at: string;
    matched_dish?: string;
    confidence?: number;
  };
}

export interface CompareRequest {
  dishA: string;
  dishB: string;
}

export interface CompareResponse {
  dishA: {
    name: string;
    calories: number;
    matched_name?: string;
    confidence?: number;
  };
  dishB: {
    name: string;
    calories: number;
    matched_name?: string;
    confidence?: number;
  };
  suggestion: string;
  meta: {
    model: string;
    generated_at: string;
    calorie_difference?: number;
    lighter_dish?: string;
  };
}

export interface WeeklyResponse {
  total_calories: number;
  chart_url: string;
  summary: string;
  date_range: {
    start: string;
    end: string;
  };
  meta: {
    model: string;
    generated_at: string;
    meal_count?: number;
    unique_dishes?: number;
    avg_calories_per_day?: number;
  };
}
```

**src/services/api.ts:**
```typescript
import axios from 'axios';
import type { PreviewRequest, PreviewResponse, CompareRequest, CompareResponse, WeeklyResponse } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Core API methods
  async generatePreview(request: PreviewRequest): Promise<PreviewResponse> {
    const response = await api.post<PreviewResponse>('/api/preview', request);
    return response.data;
  },

  async compareDishes(request: CompareRequest): Promise<CompareResponse> {
    const response = await api.post<CompareResponse>('/api/compare', request);
    return response.data;
  },

  async getWeeklySnapshot(startDate: string, endDate: string): Promise<WeeklyResponse> {
    const response = await api.get<WeeklyResponse>('/api/weekly', {
      params: { start: startDate, end: endDate }
    });
    return response.data;
  },

  // Data retrieval methods
  async getDishes(): Promise<any[]> {
    const response = await api.get('/api/dishes');
    return response.data;
  },

  async getUserMeals(): Promise<any[]> {
    const response = await api.get('/api/user_meals');
    return response.data;
  },

  // Admin methods (optional - for future admin panel)
  async addDish(dish: any): Promise<{ message: string; status: string }> {
    const response = await api.post('/admin/dish', dish);
    return response.data;
  },

  async addUserMeal(userMeal: any): Promise<{ message: string; status: string }> {
    const response = await api.post('/admin/user_meal', userMeal);
    return response.data;
  },

  async clearCache(dishName: string): Promise<{ message: string; status: string }> {
    const response = await api.post('/admin/cache/clear', null, {
      params: { dish_name: dishName }
    });
    return response.data;
  },

  // System methods
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await api.get('/health');
    return response.data;
  }
};

export default api;
```

---

## 🧩 Component Templates

### LoadingSkeleton Component

**src/components/LoadingSkeleton.tsx:**
```typescript
import React from 'react';

interface LoadingSkeletonProps {
  type: 'card' | 'chart' | 'text';
  count?: number;
}

const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({ type, count = 1 }) => {
  if (type === 'card') {
    return (
      <div className="bg-white rounded-lg shadow-sm border p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
        <div className="h-64 bg-gray-200 rounded mb-4"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2"></div>
      </div>
    );
  }

  if (type === 'chart') {
    return (
      <div className="bg-white rounded-lg shadow-sm border p-6 animate-pulse">
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  return (
    <div className="animate-pulse space-y-2">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="h-4 bg-gray-200 rounded w-full"></div>
      ))}
    </div>
  );
};

export default LoadingSkeleton;
```

### ImageWithFallback Component

**src/components/ImageWithFallback.tsx:**
```typescript
import React, { useState } from 'react';

interface ImageWithFallbackProps {
  src: string;
  alt: string;
  fallbackSrc?: string;
  className?: string;
}

const ImageWithFallback: React.FC<ImageWithFallbackProps> = ({
  src,
  alt,
  fallbackSrc = '/placeholder.png',
  className = ''
}) => {
  const [imgSrc, setImgSrc] = useState(src);
  const [isLoading, setIsLoading] = useState(true);

  const handleError = () => {
    setImgSrc(fallbackSrc);
    setIsLoading(false);
  };

  const handleLoad = () => {
    setIsLoading(false);
  };

  return (
    <div className="relative">
      {isLoading && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse rounded"></div>
      )}
      <img
        src={imgSrc}
        alt={alt}
        onError={handleError}
        onLoad={handleLoad}
        className={`${className} ${isLoading ? 'opacity-0' : 'opacity-100'} transition-opacity`}
      />
    </div>
  );
};

export default ImageWithFallback;
```

---

## 🎨 Main App Structure

**src/App.tsx:**
```typescript
import React, { useState } from 'react';
import TabNavigation from './components/TabNavigation';
import DailyPreview from './pages/DailyPreview';
import SwitchupDiff from './pages/SwitchupDiff';
import WeeklySnapshot from './pages/WeeklySnapshot';
import './App.css';

type TabType = 'preview' | 'compare' | 'weekly';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('preview');

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'preview':
        return <DailyPreview />;
      case 'compare':
        return <SwitchupDiff />;
      case 'weekly':
        return <WeeklySnapshot />;
      default:
        return <DailyPreview />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <span className="text-2xl">🍅</span>
              <h1 className="ml-2 text-xl font-bold text-gray-900">
                Tamatar-Bhai MVP
              </h1>
            </div>
            <div className="text-sm text-gray-500">
              AI-powered food insights
            </div>
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderActiveTab()}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-center text-sm text-gray-500">
            Generated by OpenAI & StabilityAI • Built with ❤️ for the Tamatar-Bhai community
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
```

---

## 🧪 Testing Your Setup

### 1. Test Backend Connection

```typescript
// Add this to your page component
useEffect(() => {
  apiService.healthCheck()
    .then(data => console.log('✅ Backend connected:', data))
    .catch(err => console.error('❌ Backend connection failed:', err));
}, []);
```

### 2. Test API Call

```bash
# In browser console
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log)
```

### 3. Run Development Server

```bash
cd frontend
npm run dev
# Open http://localhost:5173
```

---

## 📝 Development Workflow

1. **Start Backend** (in one terminal):
   ```bash
   cd backend
   uvicorn app:app --reload
   ```

2. **Start Frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Make Changes** → Save → Browser auto-refreshes

4. **Check Console** for API calls and errors

5. **Test Features** as you build them

---

## 🐛 Common Issues & Solutions

### CORS Errors
**Problem**: "Access to fetch blocked by CORS policy"
**Solution**: Backend already configured for http://localhost:3000 and http://localhost:5173

### API Not Found
**Problem**: 404 errors on API calls
**Solution**: Check `VITE_API_BASE_URL` in `.env` file

### Images Not Loading
**Problem**: Images return 404
**Solution**: Backend serves images at `/data/images/` - use full URL from API response

### TypeScript Errors
**Problem**: Type errors in components
**Solution**: Check `src/types/api.ts` matches backend response structure

---

## 🎯 Build Order (Recommended)

1. ✅ Set up project structure
2. ✅ Create API service layer
3. ✅ Build LoadingSkeleton component
4. ✅ Build TabNavigation component
5. ✅ Build DailyPreview page (test end-to-end)
6. ✅ Build SwitchupDiff page
7. ✅ Build WeeklySnapshot page
8. ✅ Add error handling
9. ✅ Polish styling
10. ✅ Create Dockerfile

---

## 📚 Helpful Resources

- **Backend API Docs**: http://localhost:8000/docs
- **Backend Health**: http://localhost:8000/health
- **Vite Docs**: https://vitejs.dev/
- **React Docs**: https://react.dev/
- **TailwindCSS Docs**: https://tailwindcss.com/docs
- **Lucide Icons**: https://lucide.dev/icons/

---

## 🚀 Next Steps

1. Follow the setup steps above
2. Test that backend is running
3. Build one page at a time
4. Test each feature before moving on
5. Refer to `tasks.md` for detailed implementation steps

**Good luck building! 🍅**
