import React, { useState } from 'react'
import { apiService, CompareResponse } from '../services/api'
import LoadingSkeleton from '../components/LoadingSkeleton'
import { Scale, Utensils, Zap, ArrowRight, TrendingDown, TrendingUp } from 'lucide-react'

const SwitchupDiff: React.FC = () => {
  const [dishA, setDishA] = useState('')
  const [dishB, setDishB] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [comparison, setComparison] = useState<CompareResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!dishA.trim() || !dishB.trim()) {
      setError('Please enter both dish names')
      return
    }

    if (dishA.trim().toLowerCase() === dishB.trim().toLowerCase()) {
      setError('Please enter two different dishes to compare')
      return
    }

    setIsLoading(true)
    setError(null)
    setComparison(null)

    try {
      const result = await apiService.compareDishes({ 
        dishA: dishA.trim(), 
        dishB: dishB.trim() 
      })
      setComparison(result)
    } catch (err: any) {
      console.error('Comparison failed:', err)
      setError(
        err.response?.data?.message || 
        'Failed to compare dishes. Please try again.'
      )
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setDishA('')
    setDishB('')
    setComparison(null)
    setError(null)
  }

  const handleSwap = () => {
    const temp = dishA
    setDishA(dishB)
    setDishB(temp)
  }

  const getCalorieDifference = () => {
    if (!comparison) return null
    return comparison.dishA.calories - comparison.dishB.calories
  }

  const getLighterDish = () => {
    if (!comparison) return null
    return comparison.dishA.calories < comparison.dishB.calories ? 'A' : 'B'
  }

  return (
    <div className="fade-in space-y-6">
      {/* Input Form */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center mb-6">
          <Scale className="w-6 h-6 text-blue-500 mr-2" />
          <h2 className="text-xl font-semibold text-gray-900">Switch-up Diff</h2>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-end">
            {/* Dish A Input */}
            <div>
              <label htmlFor="dishA" className="block text-sm font-medium text-gray-700 mb-2">
                <Utensils className="w-4 h-4 inline mr-1" />
                First Dish
              </label>
              <input
                type="text"
                id="dishA"
                value={dishA}
                onChange={(e) => setDishA(e.target.value)}
                placeholder="e.g., Butter Chicken"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                disabled={isLoading}
              />
            </div>

            {/* Swap Button */}
            <div className="flex justify-center md:justify-start">
              <button
                type="button"
                onClick={handleSwap}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                disabled={isLoading}
                title="Swap dishes"
              >
                <ArrowRight className="w-5 h-5 transform rotate-90 md:rotate-0" />
              </button>
            </div>

            {/* Dish B Input */}
            <div className="md:col-start-2">
              <label htmlFor="dishB" className="block text-sm font-medium text-gray-700 mb-2">
                <Utensils className="w-4 h-4 inline mr-1" />
                Second Dish
              </label>
              <input
                type="text"
                id="dishB"
                value={dishB}
                onChange={(e) => setDishB(e.target.value)}
                placeholder="e.g., Dal Tadka"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                disabled={isLoading}
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button
              type="submit"
              disabled={isLoading || !dishA.trim() || !dishB.trim()}
              className={`flex-1 flex items-center justify-center px-4 py-2 rounded-md font-medium transition-colors ${
                isLoading || !dishA.trim() || !dishB.trim()
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              } ${isLoading ? 'btn-loading' : ''}`}
            >
              {!isLoading && <Zap className="w-4 h-4 mr-2" />}
              {isLoading ? 'Comparing...' : 'Compare Dishes'}
            </button>
            
            {(comparison || error) && (
              <button
                type="button"
                onClick={handleReset}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
                disabled={isLoading}
              >
                Reset
              </button>
            )}
          </div>
        </form>

        {/* Error Display */}
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <span className="text-red-500 mr-2">⚠️</span>
                <p className="text-red-700 text-sm">{error}</p>
              </div>
              <button
                onClick={handleSubmit}
                className="text-red-600 hover:text-red-800 text-sm font-medium underline"
                disabled={isLoading}
              >
                Retry
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="space-y-4">
          <LoadingSkeleton type="card" />
        </div>
      )}

      {/* Comparison Results */}
      {comparison && !isLoading && (
        <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
          <div className="p-6">
            <div className="flex items-center mb-6">
              <Scale className="w-5 h-5 text-blue-500 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">
                Comparison Results
              </h3>
            </div>

            {/* Dishes Comparison */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              {/* Dish A */}
              <div className="bg-gradient-to-br from-orange-50 to-red-50 border border-orange-200 rounded-lg p-4">
                <div className="text-center">
                  <h4 className="font-semibold text-gray-900 mb-2">
                    {comparison.dishA.name}
                  </h4>
                  <div className="text-3xl font-bold text-orange-600 mb-1">
                    {comparison.dishA.calories}
                  </div>
                  <div className="text-sm text-orange-700">calories</div>
                  
                  {comparison.dishA.matched_name && comparison.dishA.matched_name !== comparison.dishA.name && (
                    <div className="mt-2 text-xs text-gray-500">
                      Matched: {comparison.dishA.matched_name}
                      {comparison.dishA.confidence && (
                        <span className="block">({Math.round(comparison.dishA.confidence * 100)}% confidence)</span>
                      )}
                    </div>
                  )}
                </div>
              </div>

              {/* VS Indicator */}
              <div className="flex items-center justify-center">
                <div className="bg-gray-100 rounded-full p-3">
                  <span className="text-2xl font-bold text-gray-600">VS</span>
                </div>
              </div>

              {/* Dish B */}
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4">
                <div className="text-center">
                  <h4 className="font-semibold text-gray-900 mb-2">
                    {comparison.dishB.name}
                  </h4>
                  <div className="text-3xl font-bold text-blue-600 mb-1">
                    {comparison.dishB.calories}
                  </div>
                  <div className="text-sm text-blue-700">calories</div>
                  
                  {comparison.dishB.matched_name && comparison.dishB.matched_name !== comparison.dishB.name && (
                    <div className="mt-2 text-xs text-gray-500">
                      Matched: {comparison.dishB.matched_name}
                      {comparison.dishB.confidence && (
                        <span className="block">({Math.round(comparison.dishB.confidence * 100)}% confidence)</span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Calorie Difference */}
            {getCalorieDifference() !== null && (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-6">
                <div className="flex items-center justify-center space-x-2">
                  {getCalorieDifference()! > 0 ? (
                    <TrendingUp className="w-5 h-5 text-red-500" />
                  ) : (
                    <TrendingDown className="w-5 h-5 text-green-500" />
                  )}
                  <span className="text-sm font-medium text-gray-700">
                    Calorie Difference: 
                  </span>
                  <span className={`font-bold ${getCalorieDifference()! > 0 ? 'text-red-600' : 'text-green-600'}`}>
                    {Math.abs(getCalorieDifference()!)} cal
                  </span>
                  {getLighterDish() && (
                    <span className="text-sm text-gray-600">
                      ({getLighterDish() === 'A' ? comparison.dishA.name : comparison.dishB.name} is lighter)
                    </span>
                  )}
                </div>
              </div>
            )}

            {/* Bhai Style Suggestion */}
            <div className="bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200 rounded-lg p-6">
              <div className="flex items-center mb-3">
                <span className="text-2xl mr-2">🤙</span>
                <h4 className="font-semibold text-gray-900">Bhai's Recommendation</h4>
              </div>
              <p className="text-gray-800 text-lg leading-relaxed font-medium">
                {comparison.suggestion}
              </p>
            </div>

            {/* API Attribution */}
            <div className="mt-6 pt-4 border-t border-gray-200">
              <div className="flex flex-col space-y-2">
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>Generated by {comparison.meta.model}</span>
                  <span>{new Date(comparison.meta.generated_at).toLocaleString()}</span>
                </div>
                <div className="text-xs text-gray-400 text-center">
                  🤖 AI-powered recommendations by OpenAI
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Help Text */}
      {!comparison && !isLoading && !error && (
        <div className="text-center py-8">
          <span className="text-4xl mb-4 block">⚖️</span>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Ready to compare dishes?
          </h3>
          <p className="text-gray-600 max-w-md mx-auto">
            Enter two Indian dish names and get calorie comparisons with 
            bhai-style recommendations to help you make better food choices.
          </p>
        </div>
      )}
    </div>
  )
}

export default SwitchupDiff