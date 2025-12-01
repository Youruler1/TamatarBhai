// WeeklySnapshot Page
// View weekly calorie consumption with chart and summary

import { useState } from 'react';
import { format, subDays } from 'date-fns';
import { WeeklyResponse } from '../types/api';
import { getWeeklySnapshot, getImageUrl, formatErrorMessage } from '../services/api';
import LoadingSkeleton from '../components/LoadingSkeleton';
import ImageWithFallback from '../components/ImageWithFallback';

const WeeklySnapshot = () => {
  // Default to last 7 days
  const today = new Date();
  const weekAgo = subDays(today, 6);
  
  const [startDate, setStartDate] = useState(format(weekAgo, 'yyyy-MM-dd'));
  const [endDate, setEndDate] = useState(format(today, 'yyyy-MM-dd'));
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<WeeklyResponse | null>(null);

  const validateDates = (): string | null => {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const now = new Date();

    if (start > end) {
      return 'Start date must be before or equal to end date';
    }

    if (end > now) {
      return 'End date cannot be in the future';
    }

    if (start > now) {
      return 'Start date cannot be in the future';
    }

    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const validationError = validateDates();
    if (validationError) {
      setError(validationError);
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await getWeeklySnapshot(startDate, endDate);
      setResult(response);
    } catch (err) {
      setError(formatErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    const today = new Date();
    const weekAgo = subDays(today, 6);
    setStartDate(format(weekAgo, 'yyyy-MM-dd'));
    setEndDate(format(today, 'yyyy-MM-dd'));
    setResult(null);
    setError(null);
  };

  const handleQuickSelect = (days: number) => {
    const end = new Date();
    const start = subDays(end, days - 1);
    setStartDate(format(start, 'yyyy-MM-dd'));
    setEndDate(format(end, 'yyyy-MM-dd'));
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Weekly Snapshot</h1>
        <p className="mt-2 text-gray-600">
          View your calorie consumption with visual charts and AI-generated summary
        </p>
      </div>

      {/* Form */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Start Date */}
            <div>
              <label htmlFor="startDate" className="block text-sm font-medium text-gray-700 mb-2">
                Start Date
              </label>
              <input
                type="date"
                id="startDate"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                max={format(new Date(), 'yyyy-MM-dd')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                disabled={isLoading}
              />
            </div>

            {/* End Date */}
            <div>
              <label htmlFor="endDate" className="block text-sm font-medium text-gray-700 mb-2">
                End Date
              </label>
              <input
                type="date"
                id="endDate"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                max={format(new Date(), 'yyyy-MM-dd')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                disabled={isLoading}
              />
            </div>
          </div>

          {/* Quick Select Buttons */}
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-gray-600 self-center mr-2">Quick select:</span>
            {[7, 14, 30].map((days) => (
              <button
                key={days}
                type="button"
                onClick={() => handleQuickSelect(days)}
                disabled={isLoading}
                className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:bg-gray-50 disabled:cursor-not-allowed transition-colors"
              >
                Last {days} days
              </button>
            ))}
          </div>

          <div className="flex space-x-4">
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {isLoading ? 'Generating...' : 'Generate Snapshot'}
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
          <LoadingSkeleton type="chart" />
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
          {/* Statistics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Total Calories */}
            <div className="bg-white rounded-lg shadow-md p-6 text-center">
              <p className="text-sm text-gray-600 mb-2">Total Calories</p>
              <p className="text-3xl font-bold text-red-600">
                {result.total_calories.toLocaleString()}
              </p>
            </div>

            {/* Average Per Day */}
            <div className="bg-white rounded-lg shadow-md p-6 text-center">
              <p className="text-sm text-gray-600 mb-2">Average Per Day</p>
              <p className="text-3xl font-bold text-blue-600">
                {result.meta.avg_calories_per_day.toLocaleString()}
              </p>
            </div>

            {/* Total Meals */}
            <div className="bg-white rounded-lg shadow-md p-6 text-center">
              <p className="text-sm text-gray-600 mb-2">Total Meals</p>
              <p className="text-3xl font-bold text-green-600">{result.meta.meal_count}</p>
            </div>
          </div>

          {/* Chart */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="p-4 bg-gray-50 border-b">
              <h3 className="text-lg font-semibold text-gray-900">
                Calorie Chart ({result.date_range.start} to {result.date_range.end})
              </h3>
            </div>
            <div className="p-4">
              <ImageWithFallback
                src={getImageUrl(result.chart_url)}
                alt="Weekly calorie chart"
                className="w-full h-auto"
              />
            </div>
          </div>

          {/* Additional Stats */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Additional Statistics</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex justify-between items-center py-2 border-b">
                <span className="text-gray-600">Days in Range:</span>
                <span className="font-semibold text-gray-900">{result.meta.days_in_range}</span>
              </div>
              <div className="flex justify-between items-center py-2 border-b">
                <span className="text-gray-600">Unique Dishes:</span>
                <span className="font-semibold text-gray-900">{result.meta.unique_dishes}</span>
              </div>
              <div className="flex justify-between items-center py-2 border-b md:col-span-2">
                <span className="text-gray-600">Most Consumed:</span>
                <span className="font-semibold text-gray-900">
                  {result.meta.most_consumed_dish} ({result.meta.most_consumed_count}x)
                </span>
              </div>
            </div>
          </div>

          {/* Summary */}
          <div className="bg-blue-50 rounded-lg shadow-md p-6 border-l-4 border-blue-500">
            <div className="flex items-start">
              <span className="text-2xl mr-3">📊</span>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Weekly Summary</h3>
                <p className="text-gray-800 leading-relaxed">{result.summary}</p>
              </div>
            </div>
          </div>

          {/* Attribution Footer */}
          <div className="text-center text-sm text-gray-500">
            <p>Chart generated by Matplotlib • Summary by OpenAI</p>
            <p className="text-xs mt-1">
              {new Date(result.meta.generated_at).toLocaleString()}
            </p>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!result && !isLoading && !error && (
        <div className="bg-gray-50 rounded-lg p-12 text-center">
          <span className="text-6xl mb-4 block">📊</span>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Ready to view your weekly snapshot?
          </h3>
          <p className="text-gray-600 max-w-md mx-auto">
            Select a date range above to see your calorie consumption visualized with charts and
            get an AI-generated summary of your eating patterns.
          </p>
          <div className="mt-6 text-sm text-gray-500">
            <p className="font-medium mb-2">Quick tips:</p>
            <ul className="text-left max-w-sm mx-auto space-y-1">
              <li>• Use the quick select buttons for common date ranges</li>
              <li>• End date cannot be in the future</li>
              <li>• Start date must be before or equal to end date</li>
              <li>• Data is based on your meal tracking history</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default WeeklySnapshot;
