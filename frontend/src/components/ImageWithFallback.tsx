import React, { useState, useEffect } from 'react'
import { clsx } from 'clsx'

interface ImageWithFallbackProps {
  src: string
  alt: string
  fallbackSrc?: string
  className?: string
  onLoad?: () => void
  onError?: () => void
}

const ImageWithFallback: React.FC<ImageWithFallbackProps> = ({
  src,
  alt,
  fallbackSrc = '/data/images/default_placeholder.png',
  className,
  onLoad,
  onError
}) => {
  const [currentSrc, setCurrentSrc] = useState(src)
  const [isLoading, setIsLoading] = useState(true)
  const [hasError, setHasError] = useState(false)

  useEffect(() => {
    setCurrentSrc(src)
    setIsLoading(true)
    setHasError(false)
  }, [src])

  const handleLoad = () => {
    setIsLoading(false)
    onLoad?.()
  }

  const handleError = () => {
    setIsLoading(false)
    setHasError(true)
    
    if (currentSrc !== fallbackSrc) {
      setCurrentSrc(fallbackSrc)
    }
    
    onError?.()
  }

  return (
    <div className={clsx('relative overflow-hidden', className)}>
      {isLoading && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse flex items-center justify-center">
          <span className="text-gray-400 text-2xl">🖼️</span>
        </div>
      )}
      
      <img
        src={currentSrc}
        alt={alt}
        onLoad={handleLoad}
        onError={handleError}
        className={clsx(
          'w-full h-full object-cover transition-opacity duration-300',
          isLoading ? 'opacity-0' : 'opacity-100'
        )}
      />
      
      {hasError && currentSrc === fallbackSrc && (
        <div className="absolute inset-0 bg-gray-100 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <span className="text-3xl mb-2 block">🍽️</span>
            <p className="text-sm">Image not available</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default ImageWithFallback