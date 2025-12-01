// API Type Definitions for Tamatar-Bhai MVP
// Based on backend API specification

// ============================================================================
// REQUEST TYPES
// ============================================================================

export interface PreviewRequest {
  dish: string;
  meal: 'breakfast' | 'lunch' | 'dinner' | 'snack';
}

export interface CompareRequest {
  dishA: string;
  dishB: string;
}

export interface WeeklyRequest {
  start: string; // YYYY-MM-DD format
  end: string;   // YYYY-MM-DD format
}

export interface DishModel {
  name: string;
  calories: number;
  meal_type?: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  description?: string;
}

export interface UserMealModel {
  dish_name: string;
  meal_type: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  calories?: number;
  consumed_at?: string; // ISO datetime string
}

export interface ClearCacheRequest {
  dish_name: string;
}

// ============================================================================
// RESPONSE TYPES
// ============================================================================

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
    matched_dish: string;
    confidence: number;
  };
}

export interface DishInfo {
  name: string;
  calories: number;
  matched_name: string;
  confidence: number;
  protein_g?: number;
  carbs_g?: number;
  fat_g?: number;
}

export interface CompareResponse {
  dishA: DishInfo;
  dishB: DishInfo;
  suggestion: string;
  meta: {
    model: string;
    generated_at: string;
    calorie_difference: number;
    lighter_dish: string;
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
    meal_count: number;
    unique_dishes: number;
    avg_calories_per_day: number;
    days_in_range: number;
    most_consumed_dish: string;
    most_consumed_count: number;
  };
}

export interface Dish {
  id: number;
  name: string;
  calories: number;
  meal_type: string;
  description?: string;
}

export interface UserMeal {
  id: number;
  dish_name: string;
  meal_type: string;
  calories: number;
  consumed_at: string;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  service: string;
}

export interface RootResponse {
  message: string;
  version: string;
  docs: string;
  health: string;
}

export interface AdminResponse {
  message: string;
  status: 'success' | 'error';
}

export interface ErrorResponse {
  error: boolean;
  message: string;
  error_code: string;
  timestamp: string;
  fallback_used?: boolean;
}

// ============================================================================
// API CLIENT TYPES
// ============================================================================

export type MealType = 'breakfast' | 'lunch' | 'dinner' | 'snack';

export interface ApiConfig {
  baseURL: string;
  timeout?: number;
}

export interface ApiError extends Error {
  response?: {
    data: ErrorResponse;
    status: number;
  };
}
