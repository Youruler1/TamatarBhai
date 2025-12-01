// Component Props Type Definitions for Tamatar-Bhai MVP

import { ReactNode } from 'react';
import {
  PreviewResponse,
  CompareResponse,
  WeeklyResponse,
  MealType,
} from './api';

// ============================================================================
// MAIN APP COMPONENTS
// ============================================================================

export interface AppProps {
  theme?: 'light' | 'dark';
}

export type TabType = 'preview' | 'compare' | 'weekly';

export interface TabNavigationProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

// ============================================================================
// PAGE COMPONENTS
// ============================================================================

export interface DailyPreviewProps {
  // Optional props for testing or custom behavior
  onPreviewGenerate?: (dish: string, meal: MealType) => Promise<PreviewResponse>;
}

export interface SwitchupDiffProps {
  // Optional props for testing or custom behavior
  onCompare?: (dishA: string, dishB: string) => Promise<CompareResponse>;
}

export interface WeeklySnapshotProps {
  // Optional props for testing or custom behavior
  onWeeklyGenerate?: (startDate: string, endDate: string) => Promise<WeeklyResponse>;
}

// ============================================================================
// SHARED COMPONENTS
// ============================================================================

export type LoadingSkeletonType = 'card' | 'chart' | 'text' | 'image';

export interface LoadingSkeletonProps {
  type: LoadingSkeletonType;
  count?: number;
  className?: string;
}

export interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error) => ReactNode);
}

export interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export interface ImageWithFallbackProps {
  src: string;
  alt: string;
  fallbackSrc?: string;
  className?: string;
  onLoad?: () => void;
  onError?: () => void;
}

// ============================================================================
// FORM COMPONENTS
// ============================================================================

export interface DishInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
}

export interface MealSelectorProps {
  value: MealType;
  onChange: (meal: MealType) => void;
  disabled?: boolean;
}

export interface DatePickerProps {
  value: string;
  onChange: (date: string) => void;
  min?: string;
  max?: string;
  disabled?: boolean;
  label?: string;
}

// ============================================================================
// RESULT DISPLAY COMPONENTS
// ============================================================================

export interface PreviewResultProps {
  data: PreviewResponse;
  onReset?: () => void;
}

export interface CompareResultProps {
  data: CompareResponse;
  onReset?: () => void;
  onSwap?: () => void;
}

export interface WeeklyResultProps {
  data: WeeklyResponse;
  onReset?: () => void;
}

// ============================================================================
// UI COMPONENTS
// ============================================================================

export interface ButtonProps {
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;
  variant?: 'primary' | 'secondary' | 'danger';
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}

export interface CardProps {
  children: ReactNode;
  title?: string;
  className?: string;
  variant?: 'default' | 'bhai' | 'formal';
}

export interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
}

export interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
  className?: string;
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export interface LoadingState {
  isLoading: boolean;
  error: string | null;
}

export interface FormState<T> {
  values: T;
  errors: Partial<Record<keyof T, string>>;
  isSubmitting: boolean;
}
