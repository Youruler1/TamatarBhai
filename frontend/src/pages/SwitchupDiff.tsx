// SwitchupDiff Page
// Compare two dishes and get bhai-style recommendation

import { useState } from 'react';
import { CompareResponse } from '../types/api';
import { compareDishes, formatErrorMessage } from '../services/api';
import LoadingSkeleton from '../components/LoadingSkeleton';

const SwitchupDiff = () => {
  const [dishA, setDishA] = useState('');
  const [dishB, setDishB] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<CompareResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!dishA.trim() || !dishB.trim()) {
      setError('Please enter both dish names');
      return;
    }

    if (dishA.trim().toLowerCase() === dishB.trim().toLowerCase()) {
      setError('Please enter two different dishes to compare');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await compareDishes(dishA.trim(), dishB.trim());
      setResult(response);
    } catch (err) {
      setError(formatErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  };

  const handleSwap = () => {
    const temp = dishA;
    setDishA(dishB);
    setDishB(temp);
  };

  const handleReset = () => {
    setDishA('');
    setDishB('');
    setResult(null);
    setError(null);
  };

  const getLighterDish = () => {
    if (!result) return null;
    return result.dishA.calories < result.dishB.calories ? 'A' : 'B';
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Switch-up Diff</h1>
        <p className="mt-2 text-gray-600">
          Compare two dishes and get a bhai-style recommendation
        </p>
      </div>

      {/* Form */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Dish A */}
            <div>
              <label htmlFor="dishA" className="block text-sm font-medium text-gray-700 mb-2">
                First Dish
              </label>
              <input
                type="text"
                id="dishA"
                value={dishA}
                onChange={(e) => setDishA(e.target.value)}
                placeholder="e.g., rajma"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                disabled={isLoading}
              />
            </div>

            {/* Dish B */}
            <div>
              <label htmlFor="dishB" className="block text-sm font-medium text-gray-700 mb-2">
                Second Dish
              </label>
              <input
                type="text"
                id="dishB"
                value={dishB}
                onChange={(e) => setDishB(e.target.value)}
                placeholder="e.g., dal tadka"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                disabled={isLoading}
              />
            </div>
          </div>

          <div className="flex flex-wrap gap-4">
            <button
              type="submit"
              disabled={isLoading || !dishA.trim() || !dishB.trim()}
              className="flex-1 min-w-[200px] px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {isLoading ? 'Comparing...' : 'Compare Dishes'}
            </button>
            
            <button
              type="button"
              onClick={handleSwap}
              disabled={isLoading}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
              title="Swap dishes"
            >
              ⇄ Swap
            </button>

            {result && (
              <button
                type="button"
                onClick={handleReset}
                className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
              >
                Reset
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="space-y-6">
          <LoadingSkeleton type="card" count={2} />
        </div>
      )}

      {/* Error State */}
      {error && !isLoading && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex items-start">
            <svg
              className="w-6 h-6 text-red-600 mt-0.5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <div className="ml-3 flex-1">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <p className="mt-1 text-sm text-red-700">{error}</p>
              <button
                onClick={handleSubmit}
                className="mt-3 text-sm font-medium text-red-600 hover:text-red-500"
              >
                Try Again →
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {result && !isLoading && (
        <div className="space-y-6">
          {/* Comparison Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Dish A Card */}
            <div
              className={`bg-white rounded-lg shadow-md p-6 border-2 ${
                getLighterDish() === 'A' ? 'border-green-500' : 'border-gray-200'
              }`}
            >
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">{result.dishA.name}</h3>
                {getLighterDish() === 'A' && (
                  <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded">
                    Lighter
                  </span>
                )}
              </div>
              
              <div className="mb-4">
                <span className="text-4xl font-bold text-red-600">{result.dishA.calories}</span>
                <span className="text-lg text-gray-600 ml-2">cal</span>
              </div>

              {result.dishA.matched_name !== result.dishA.name && (
                <p className="text-sm text-gray-500 mb-3">
                  Matched to: {result.dishA.matched_name} ({result.dishA.confidence}%)
                </p>
              )}

              {(result.dishA.protein_g || result.dishA.carbs_g || result.dishA.fat_g) && (
                <div className="space-y-2 text-sm">
                  {result.dishA.protein_g && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Protein:</span>
                      <span className="font-medium">{result.dishA.protein_g}g</span>
                    </div>
                  )}
                  {result.dishA.carbs_g && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Carbs:</span>
                      <span className="font-medium">{result.dishA.carbs_g}g</span>
                    </div>
                  )}
                  {result.dishA.fat_g && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Fat:</span>
                      <span className="font-medium">{result.dishA.fat_g}g</span>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Dish B Card */}
            <div
              className={`bg-white rounded-lg shadow-md p-6 border-2 ${
                getLighterDish() === 'B' ? 'border-green-500' : 'border-gray-200'
              }`}
            >
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">{result.dishB.name}</h3>
                {getLighterDish() === 'B' && (
                  <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded">
                    Lighter
                  </span>
                )}
              </div>
              
              <div className="mb-4">
                <span className="text-4xl font-bold text-red-600">{result.dishB.calories}</span>
                <span className="text-lg text-gray-600 ml-2">cal</span>
              </div>

              {result.dishB.matched_name !== result.dishB.name && (
                <p className="text-sm text-gray-500 mb-3">
                  Matched to: {result.dishB.matched_name} ({result.dishB.confidence}%)
                </p>
              )}

              {(result.dishB.protein_g || result.dishB.carbs_g || result.dishB.fat_g) && (
                <div className="space-y-2 text-sm">
                  {result.dishB.protein_g && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Protein:</span>
                      <span className="font-medium">{result.dishB.protein_g}g</span>
                    </div>
                  )}
                  {result.dishB.carbs_g && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Carbs:</span>
                      <span className="font-medium">{result.dishB.carbs_g}g</span>
                    </div>
                  )}
                  {result.dishB.fat_g && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Fat:</span>
                      <span className="font-medium">{result.dishB.fat_g}g</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Calorie Difference */}
          <div className="bg-gray-50 rounded-lg p-4 text-center">
            <p className="text-sm text-gray-600">
              Calorie Difference:{' '}
              <span className="font-bold text-gray-900">
                {Math.abs(result.meta.calorie_difference)} calories
              </span>
            </p>
          </div>

          {/* Bhai Recommendation */}
          <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-lg shadow-md p-6 border-l-4 border-red-500">
            <div className="flex items-start">
              <span className="text-3xl mr-4">💡</span>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Bhai's Recommendation</h3>
                <p className="text-gray-800 text-lg italic">{result.suggestion}</p>
              </div>
            </div>
          </div>

          {/* Attribution Footer */}
          <div className="text-center text-sm text-gray-500">
            <p>Generated by OpenAI</p>
            <p className="text-xs mt-1">
              {new Date(result.meta.generated_at).toLocaleString()}
            </p>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!result && !isLoading && !error && (
        <div className="bg-gray-50 rounded-lg p-12 text-center">
          <span className="text-6xl mb-4 block">⚖️</span>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Ready to compare dishes?
          </h3>
          <p className="text-gray-600 max-w-md mx-auto">
            Enter two dish names above to compare their nutritional values and get a bhai-style
            recommendation on which one to choose.
          </p>
          <div className="mt-6 text-sm text-gray-500">
            <p className="font-medium mb-2">Try these comparisons:</p>
            <div className="flex flex-wrap justify-center gap-2">
              {[
                { a: 'Rajma', b: 'Dal Tadka' },
                { a: 'Butter Chicken', b: 'Tandoori Chicken' },
                { a: 'Aloo Paratha', b: 'Roti' },
              ].map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setDishA(example.a);
                    setDishB(example.b);
                  }}
                  className="px-3 py-1 bg-white border border-gray-300 rounded-full hover:border-red-500 hover:text-red-600 transition-colors"
                >
                  {example.a} vs {example.b}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SwitchupDiff;
