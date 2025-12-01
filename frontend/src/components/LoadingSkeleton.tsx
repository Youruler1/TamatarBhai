// LoadingSkeleton Component
// Displays animated loading placeholders for different content types

import { LoadingSkeletonProps } from '../types/components';

const LoadingSkeleton = ({ type, count = 1, className = '' }: LoadingSkeletonProps) => {
  const skeletons = Array.from({ length: count }, (_, i) => i);

  const baseClasses = 'animate-pulse bg-gray-200 rounded';

  const getSkeletonByType = () => {
    switch (type) {
      case 'card':
        return (
          <div className={`${baseClasses} p-6 space-y-4 ${className}`}>
            <div className="h-4 bg-gray-300 rounded w-3/4"></div>
            <div className="h-4 bg-gray-300 rounded w-1/2"></div>
            <div className="h-32 bg-gray-300 rounded"></div>
            <div className="h-4 bg-gray-300 rounded w-5/6"></div>
          </div>
        );

      case 'chart':
        return (
          <div className={`${baseClasses} ${className}`}>
            <div className="h-64 bg-gray-300 rounded"></div>
            <div className="mt-4 space-y-2">
              <div className="h-4 bg-gray-300 rounded w-3/4"></div>
              <div className="h-4 bg-gray-300 rounded w-1/2"></div>
            </div>
          </div>
        );

      case 'text':
        return (
          <div className={`space-y-2 ${className}`}>
            <div className={`${baseClasses} h-4 w-full`}></div>
            <div className={`${baseClasses} h-4 w-5/6`}></div>
            <div className={`${baseClasses} h-4 w-4/6`}></div>
          </div>
        );

      case 'image':
        return (
          <div className={`${baseClasses} ${className}`}>
            <div className="aspect-video bg-gray-300 rounded"></div>
          </div>
        );

      default:
        return (
          <div className={`${baseClasses} h-20 ${className}`}></div>
        );
    }
  };

  return (
    <div className="space-y-4">
      {skeletons.map((index) => (
        <div key={index}>{getSkeletonByType()}</div>
      ))}
    </div>
  );
};

export default LoadingSkeleton;
