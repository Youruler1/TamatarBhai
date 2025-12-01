// API Service Layer for Tamatar-Bhai MVP
// Handles all communication with the backend API

import axios, { AxiosInstance, AxiosError } from 'axios';
import {
  PreviewRequest,
  PreviewResponse,
  CompareRequest,
  CompareResponse,
  WeeklyResponse,
  Dish,
  UserMeal,
  DishModel,
  UserMealModel,
  AdminResponse,
  HealthResponse,
  RootResponse,
  ErrorResponse,
  ApiError,
} from '../types/api';

// ============================================================================
// API CONFIGURATION
// ============================================================================

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_TIMEOUT = 30000; // 30 seconds

// ============================================================================
// AXIOS INSTANCE
// ============================================================================

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================================================
// REQUEST INTERCEPTOR
// ============================================================================

apiClient.interceptors.request.use(
  (config) => {
    // Log outgoing requests in development
    if (import.meta.env.DEV) {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, config.data);
    }
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// ============================================================================
// RESPONSE INTERCEPTOR
// ============================================================================

apiClient.interceptors.response.use(
  (response) => {
    // Log successful responses in development
    if (import.meta.env.DEV) {
      console.log(`[API Response] ${response.config.url}`, response.data);
    }
    return response;
  },
  (error: AxiosError<ErrorResponse>) => {
    // Log errors
    console.error('[API Response Error]', {
      url: error.config?.url,
      status: error.response?.status,
      message: error.response?.data?.message || error.message,
    });

    // Transform error for better handling
    const apiError: ApiError = new Error(
      error.response?.data?.message || error.message || 'An unexpected error occurred'
    ) as ApiError;
    
    apiError.response = error.response;
    
    return Promise.reject(apiError);
  }
);

// ============================================================================
// API METHODS
// ============================================================================

/**
 * System Endpoints
 */

export const healthCheck = async (): Promise<HealthResponse> => {
  const response = await apiClient.get<HealthResponse>('/health');
  return response.data;
};

export const getRootInfo = async (): Promise<RootResponse> => {
  const response = await apiClient.get<RootResponse>('/');
  return response.data;
};

/**
 * Core API Endpoints
 */

export const generatePreview = async (
  dish: string,
  meal: PreviewRequest['meal']
): Promise<PreviewResponse> => {
  const response = await apiClient.post<PreviewResponse>('/api/preview', {
    dish,
    meal,
  });
  return response.data;
};

export const getDishes = async (): Promise<Dish[]> => {
  const response = await apiClient.get<Dish[]>('/api/dishes');
  return response.data;
};

export const getUserMeals = async (): Promise<UserMeal[]> => {
  const response = await apiClient.get<UserMeal[]>('/api/user_meals');
  return response.data;
};

export const compareDishes = async (
  dishA: string,
  dishB: string
): Promise<CompareResponse> => {
  const response = await apiClient.post<CompareResponse>('/api/compare', {
    dishA,
    dishB,
  });
  return response.data;
};

export const getWeeklySnapshot = async (
  startDate: string,
  endDate: string
): Promise<WeeklyResponse> => {
  const response = await apiClient.get<WeeklyResponse>('/api/weekly', {
    params: {
      start: startDate,
      end: endDate,
    },
  });
  return response.data;
};

/**
 * Admin Endpoints
 */

export const addDish = async (dish: DishModel): Promise<AdminResponse> => {
  const response = await apiClient.post<AdminResponse>('/admin/dish', dish);
  return response.data;
};

export const addUserMeal = async (meal: UserMealModel): Promise<AdminResponse> => {
  const response = await apiClient.post<AdminResponse>('/admin/user_meal', meal);
  return response.data;
};

export const clearCache = async (dishName: string): Promise<AdminResponse> => {
  const response = await apiClient.post<AdminResponse>('/admin/cache/clear', null, {
    params: {
      dish_name: dishName,
    },
  });
  return response.data;
};

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Check if the API is reachable
 */
export const checkApiConnection = async (): Promise<boolean> => {
  try {
    await healthCheck();
    return true;
  } catch (error) {
    console.error('API connection check failed:', error);
    return false;
  }
};

/**
 * Get the full URL for an image or chart
 */
export const getImageUrl = (path: string): string => {
  if (path.startsWith('http')) {
    return path;
  }
  return `${API_BASE_URL}${path}`;
};

/**
 * Format error message for display
 */
export const formatErrorMessage = (error: unknown): string => {
  if (error instanceof Error) {
    const apiError = error as ApiError;
    if (apiError.response?.data?.message) {
      return apiError.response.data.message;
    }
    return error.message;
  }
  return 'An unexpected error occurred';
};

// ============================================================================
// EXPORT DEFAULT API CLIENT
// ============================================================================

export default {
  // System
  healthCheck,
  getRootInfo,
  
  // Core API
  generatePreview,
  getDishes,
  getUserMeals,
  compareDishes,
  getWeeklySnapshot,
  
  // Admin
  addDish,
  addUserMeal,
  clearCache,
  
  // Utilities
  checkApiConnection,
  getImageUrl,
  formatErrorMessage,
};
