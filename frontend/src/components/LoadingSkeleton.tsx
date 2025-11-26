import React from 'react'
import { clsx } from 'clsx'

interface LoadingSkeletonProps {
  type: 'card' | 'chart' | 'text' | 'image'
  count?: number
  className?: string
}

const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({ 
  type, 
  count = 1, 
  className 
}) => {
  const renderSkeleton = () => {
    switch (type) {
      case 'card':
        return (
          <div className={clsx('bg-white rounded-lg shadow-sm border p-6', className)}>
            <div className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-2/3 mb-4"></div>
              <div className="h-32 bg-gray-200 rounded mb-4"></div>
              <div className="h-3 bg-gray-200 rounded w-full mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-4/5"></div>
            </div>
          </div>
        )
      
      case 'chart':
        return (
          <div className={clsx('bg-white rounded-lg shadow-sm border p-6', className)}>
            <div className="animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-1/2 mb-6"></div>
              <div className="h-64 bg-gray-200 rounded mb-4"></div>
              <div className="flex justify-center space-x-4">
                <div className="h-3 bg-gray-200 rounded w-16"></div>
                <div className="h-3 bg-gray-200 rounded w-16"></div>
                <div className="h-3 bg-gray-200 rounded w-16"></div>
              </div>
            </div>
          </div>
        )
      
      case 'image':
        return (
          <div className={clsx('bg-gray-200 rounded-lg animate-pulse', className)}>
            <div className="h-64 w-full bg-gray-200 rounded-lg flex items-center justify-center">
              <span className="text-gray-400 text-4xl">🖼️</span>
            </div>
          </div>
        )
      
      case 'text':
        return (
          <div className={clsx('animate-pulse', className)}>
            <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-4/6"></div>
          </div>
        )
      
      default:
        return (
          <div className={clsx('h-4 bg-gray-200 rounded animate-pulse', className)}></div>
        )
    }
  }

  return (
    <>
      {Array.from({ length: count }, (_, index) => (
        <div key={index} className="mb-4 last:mb-0">
          {renderSkeleton()}
        </div>
      ))}
    </>
  )
}

export default LoadingSkeleton