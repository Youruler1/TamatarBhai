// DailyPreview Page
// Main feature: Generate AI-powered dish preview with image, calories, and captions

import { useState } from 'react';
import { PreviewResponse, MealType } from '../types/api';
import { generatePreview, getImageUrl, formatErrorMessage } from '../services/api';
import LoadingSkeleton from '../components/LoadingSkeleton';
import ImageWithFallback from '../components/ImageWithFallback';

const DailyPreview = () => {
  const [dish, setDish] = useState('');
  const [meal, setMeal] = useState<MealType>('lunch');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PreviewResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!dish.trim()) {
      setError('Please enter a dish name');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await generatePreview(dish.trim(), meal);
      setResult(response);
    } catch (err) {
      setError(formatErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setDish('');
    setMeal('lunch');
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Daily Preview</h1>
        <p className="mt-2 text-gray-600">
          Get AI-generated insights about your dish with image, calories, and captions
        </p>
      </div>

      {/* Form */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="dish" className="block text-sm font-medium text-gray-700 mb-2">
              Dish Name
            </label>
            <input
              type="text"
              id="dish"
              value={dish}
              onChange={(e) => setDish(e.target.value)}
              placeholder="e.g., aloo paratha, butter chicken, rajma"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              disabled={isLoading}
            />
          </div>

          <div>
            <label htmlFor="meal" className="block text-sm font-medium text-gray-700 mb-2">
              Meal Type
            </label>
            <select
              id="meal"
              value={meal}
              onChange={(e) => setMeal(e.target.value as MealType)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              disabled={isLoading}
            >
              <option value="breakfast">Breakfast</option>
              <option value="lunch">Lunch</option>
              <option value="dinner">Dinner</option>
              <option value="snack">Snack</option>
            </select>
          </div>

          <div className="flex space-x-4">
            <button
              type="submit"
              disabled={isLoading || !dish.trim()}
              className="flex-1 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {isLoading ? 'Generating...' : 'Generate Preview'}
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
          <LoadingSkeleton type="image" />
          <LoadingSkeleton type="card" />
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
          {/* Dish Image */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <ImageWithFallback
              src={getImageUrl(result.image_url)}
              alt={result.dish}
              className="w-full h-64 object-cover"
            />
          </div>

          {/* Calories */}
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <h2 className="text-2xl font-bold text-gray-900">{result.dish}</h2>
            <div className="mt-4">
              <span className="text-5xl font-bold text-red-600">{result.calories}</span>
              <span className="text-xl text-gray-600 ml-2">calories</span>
            </div>
            {result.meta.matched_dish !== result.dish && (
              <p className="mt-2 text-sm text-gray-500">
                Matched to: {result.meta.matched_dish} ({result.meta.confidence}% confidence)
              </p>
            )}
          </div>

          {/* Bhai Style Caption */}
          <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-lg shadow-md p-6 border-l-4 border-red-500">
            <div className="flex items-start">
              <span className="text-2xl mr-3">💬</span>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Bhai Style</h3>
                <p className="text-gray-800 italic">{result.captions.bhai}</p>
              </div>
            </div>
          </div>

          {/* Formal Caption */}
          <div className="bg-blue-50 rounded-lg shadow-md p-6 border-l-4 border-blue-500">
            <div className="flex items-start">
              <span className="text-2xl mr-3">📝</span>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Formal Description</h3>
                <p className="text-gray-800">{result.captions.formal}</p>
              </div>
            </div>
          </div>

          {/* Attribution Footer */}
          <div className="text-center text-sm text-gray-500">
            <p>Generated by OpenAI & StabilityAI</p>
            <p className="text-xs mt-1">
              {new Date(result.meta.generated_at).toLocaleString()}
            </p>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!result && !isLoading && !error && (
        <div className="bg-gray-50 rounded-lg p-12 text-center">
          <span className="text-6xl mb-4 block">🍽️</span>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Ready to explore your dish?
          </h3>
          <p className="text-gray-600 max-w-md mx-auto">
            Enter a dish name and meal type above to get AI-generated insights including an image,
            calorie count, and both casual and formal descriptions.
          </p>
          <div className="mt-6 text-sm text-gray-500">
            <p className="font-medium mb-2">Try these examples:</p>
            <div className="flex flex-wrap justify-center gap-2">
              {['Aloo Paratha', 'Butter Chicken', 'Rajma', 'Dal Tadka'].map((example) => (
                <button
                  key={example}
                  onClick={() => setDish(example)}
                  className="px-3 py-1 bg-white border border-gray-300 rounded-full hover:border-red-500 hover:text-red-600 transition-colors"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DailyPreview;
