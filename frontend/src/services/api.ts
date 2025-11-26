import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.status, error.message)
    return Promise.reject(error)
  }
)

// Types
export interface PreviewRequest {
  dish: string
  meal: string
}

export interface PreviewResponse {
  dish: string
  calories: number
  image_url: string
  captions: {
    bhai: string
    formal: string
  }
  meta: {
    model: string
    generated_at: string
    matched_dish?: string
    confidence?: number
  }
}

export interface CompareRequest {
  dishA: string
  dishB: string
}

export interface CompareResponse {
  dishA: {
    name: string
    calories: number
    matched_name?: string
    confidence?: number
  }
  dishB: {
    name: string
    calories: number
    matched_name?: string
    confidence?: number
  }
  suggestion: string
  meta: {
    model: string
    generated_at: string
    calorie_difference?: number
    lighter_dish?: string
  }
}

export interface WeeklyResponse {
  total_calories: number
  chart_url: string
  summary: string
  date_range: {
    start: string
    end: string
  }
  meta: {
    model: string
    generated_at: string
    meal_count?: number
    unique_dishes?: number
    avg_calories_per_day?: number
  }
}

export interface Dish {
  id: number
  name: string
  calories: number
  meal_type: string
  description?: string
}

// API functions
export const apiService = {
  // Generate daily preview
  async generatePreview(request: PreviewRequest): Promise<PreviewResponse> {
    const response = await api.post<PreviewResponse>('/api/preview', request)
    return response.data
  },

  // Get all dishes
  async getDishes(): Promise<Dish[]> {
    const response = await api.get<Dish[]>('/api/dishes')
    return response.data
  },

  // Compare dishes
  async compareDishes(request: CompareRequest): Promise<CompareResponse> {
    const response = await api.post<CompareResponse>('/api/compare', request)
    return response.data
  },

  // Get weekly snapshot
  async getWeeklySnapshot(startDate: string, endDate: string): Promise<WeeklyResponse> {
    const response = await api.get<WeeklyResponse>('/api/weekly', {
      params: { start: startDate, end: endDate }
    })
    return response.data
  },

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await api.get('/health')
    return response.data
  },

  // Admin functions
  async addDish(dish: Omit<Dish, 'id'>): Promise<{ message: string; status: string }> {
    const response = await api.post('/admin/dish', dish)
    return response.data
  },

  async clearCache(dishName: string): Promise<{ message: string; status: string }> {
    const response = await api.post('/admin/cache/clear', null, {
      params: { dish_name: dishName }
    })
    return response.data
  }
}

export default api