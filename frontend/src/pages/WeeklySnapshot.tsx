import React, { useState } from "react";
import { apiService, WeeklyResponse } from "../services/api";
import LoadingSkeleton from "../components/LoadingSkeleton";
import ImageWithFallback from "../components/ImageWithFallback";
import { BarChart3, Calendar, TrendingUp, FileText, Clock } from "lucide-react";
import { format, subDays, startOfWeek, endOfWeek } from "date-fns";

const WeeklySnapshot: React.FC = () => {
  const [startDate, setStartDate] = useState(() => {
    const today = new Date();
    const weekStart = startOfWeek(today, { weekStartsOn: 1 }); // Monday
    return format(weekStart, "yyyy-MM-dd");
  });

  const [endDate, setEndDate] = useState(() => {
    const today = new Date();
    const weekEnd = endOfWeek(today, { weekStartsOn: 1 }); // Sunday
    return format(weekEnd, "yyyy-MM-dd");
  });

  const [isLoading, setIsLoading] = useState(false);
  const [weeklyData, setWeeklyData] = useState<WeeklyResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!startDate || !endDate) {
      setError("Please select both start and end dates");
      return;
    }

    if (new Date(startDate) > new Date(endDate)) {
      setError("Start date must be before end date");
      return;
    }

    setIsLoading(true);
    setError(null);
    setWeeklyData(null);

    try {
      const result = await apiService.getWeeklySnapshot(startDate, endDate);
      setWeeklyData(result);
    } catch (err: any) {
      console.error("Weekly snapshot failed:", err);
      setError(
        err.response?.data?.message ||
          "Failed to generate weekly snapshot. Please try again."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    const today = new Date();
    const weekStart = startOfWeek(today, { weekStartsOn: 1 });
    const weekEnd = endOfWeek(today, { weekStartsOn: 1 });

    setStartDate(format(weekStart, "yyyy-MM-dd"));
    setEndDate(format(weekEnd, "yyyy-MM-dd"));
    setWeeklyData(null);
    setError(null);
  };

  const handleQuickSelect = (days: number) => {
    const today = new Date();
    const start = subDays(today, days - 1);

    setStartDate(format(start, "yyyy-MM-dd"));
    setEndDate(format(today, "yyyy-MM-dd"));
  };

  const getDateRangeText = () => {
    if (!weeklyData) return "";

    const start = new Date(weeklyData.date_range.start);
    const end = new Date(weeklyData.date_range.end);

    return `${format(start, "MMM dd")} - ${format(end, "MMM dd, yyyy")}`;
  };

  const getAverageCaloriesPerDay = () => {
    if (!weeklyData?.meta?.avg_calories_per_day) return null;
    return Math.round(weeklyData.meta.avg_calories_per_day);
  };

  return (
    <div className="fade-in space-y-6">
      {/* Input Form */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center mb-6">
          <BarChart3 className="w-6 h-6 text-purple-500 mr-2" />
          <h2 className="text-xl font-semibold text-gray-900">
            Weekly Snapshot
          </h2>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Start Date */}
            <div>
              <label
                htmlFor="startDate"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                <Calendar className="w-4 h-4 inline mr-1" />
                Start Date
              </label>
              <input
                type="date"
                id="startDate"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors"
                disabled={isLoading}
              />
            </div>

            {/* End Date */}
            <div>
              <label
                htmlFor="endDate"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                <Calendar className="w-4 h-4 inline mr-1" />
                End Date
              </label>
              <input
                type="date"
                id="endDate"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors"
                disabled={isLoading}
              />
            </div>
          </div>

          {/* Quick Select Buttons */}
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-gray-600 mr-2">Quick select:</span>
            <button
              type="button"
              onClick={() => handleQuickSelect(7)}
              className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
              disabled={isLoading}
            >
              Last 7 days
            </button>
            <button
              type="button"
              onClick={() => handleQuickSelect(14)}
              className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
              disabled={isLoading}
            >
              Last 14 days
            </button>
            <button
              type="button"
              onClick={() => handleQuickSelect(30)}
              className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
              disabled={isLoading}
            >
              Last 30 days
            </button>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button
              type="submit"
              disabled={isLoading || !startDate || !endDate}
              className={`flex-1 flex items-center justify-center px-4 py-2 rounded-md font-medium transition-colors ${
                isLoading || !startDate || !endDate
                  ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                  : "bg-purple-600 text-white hover:bg-purple-700"
              } ${isLoading ? "btn-loading" : ""}`}
            >
              {!isLoading && <TrendingUp className="w-4 h-4 mr-2" />}
              {isLoading ? "Generating..." : "Generate Snapshot"}
            </button>

            {(weeklyData || error) && (
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
          <LoadingSkeleton type="chart" />
        </div>
      )}

      {/* Weekly Results */}
      {weeklyData && !isLoading && (
        <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900">
                Weekly Analysis
              </h3>
              <div className="text-sm text-gray-500">{getDateRangeText()}</div>
            </div>

            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              {/* Total Calories */}
              <div className="bg-gradient-to-br from-purple-50 to-indigo-50 border border-purple-200 rounded-lg p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600 mb-1">
                    {weeklyData.total_calories.toLocaleString()}
                  </div>
                  <div className="text-sm text-purple-700">Total Calories</div>
                </div>
              </div>

              {/* Average Per Day */}
              {getAverageCaloriesPerDay() && (
                <div className="bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-lg p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600 mb-1">
                      {getAverageCaloriesPerDay()}
                    </div>
                    <div className="text-sm text-green-700">Avg per Day</div>
                  </div>
                </div>
              )}

              {/* Meal Count */}
              {weeklyData.meta?.meal_count && (
                <div className="bg-gradient-to-br from-orange-50 to-red-50 border border-orange-200 rounded-lg p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600 mb-1">
                      {weeklyData.meta.meal_count}
                    </div>
                    <div className="text-sm text-orange-700">Total Meals</div>
                  </div>
                </div>
              )}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Chart Section */}
              <div className="space-y-4">
                <div className="flex items-center">
                  <BarChart3 className="w-5 h-5 text-purple-500 mr-2" />
                  <h4 className="font-semibold text-gray-900">Calorie Chart</h4>
                </div>

                <div className="aspect-video rounded-lg overflow-hidden bg-gray-50 border">
                  <ImageWithFallback
                    src={weeklyData.chart_url}
                    alt="Weekly calorie chart"
                    className="w-full h-full"
                    fallbackSrc="/data/images/chart_placeholder.png"
                  />
                </div>

                {weeklyData.meta?.unique_dishes && (
                  <div className="text-xs text-gray-500 bg-gray-50 p-2 rounded">
                    <span className="font-medium">Unique dishes:</span>{" "}
                    {weeklyData.meta.unique_dishes}
                  </div>
                )}
              </div>

              {/* Summary Section */}
              <div className="space-y-4">
                <div className="flex items-center">
                  <FileText className="w-5 h-5 text-blue-500 mr-2" />
                  <h4 className="font-semibold text-gray-900">AI Summary</h4>
                </div>

                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
                  <p className="text-gray-800 leading-relaxed">
                    {weeklyData.summary}
                  </p>
                </div>

                {/* Additional Insights */}
                <div className="space-y-2">
                  <h5 className="font-medium text-gray-900 text-sm">
                    Quick Insights
                  </h5>
                  <div className="space-y-1 text-sm text-gray-600">
                    <div className="flex items-center">
                      <Clock className="w-3 h-3 mr-2" />
                      Period:{" "}
                      {Math.ceil(
                        (new Date(weeklyData.date_range.end).getTime() -
                          new Date(weeklyData.date_range.start).getTime()) /
                          (1000 * 60 * 60 * 24) +
                          1
                      )}{" "}
                      days
                    </div>
                    {getAverageCaloriesPerDay() && (
                      <div className="flex items-center">
                        <TrendingUp className="w-3 h-3 mr-2" />
                        Daily average: {getAverageCaloriesPerDay()} calories
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* API Attribution */}
            <div className="mt-6 pt-4 border-t border-gray-200">
              <div className="flex flex-col space-y-2">
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>Generated by {weeklyData.meta.model}</span>
                  <span>
                    {new Date(weeklyData.meta.generated_at).toLocaleString()}
                  </span>
                </div>
                <div className="text-xs text-gray-400 text-center">
                  📊 Charts generated with matplotlib • 🤖 AI summaries by
                  OpenAI
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Help Text */}
      {!weeklyData && !isLoading && !error && (
        <div className="text-center py-8">
          <span className="text-4xl mb-4 block">📊</span>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Ready to analyze your eating patterns?
          </h3>
          <p className="text-gray-600 max-w-md mx-auto">
            Select a date range to generate visual charts and AI-powered
            summaries of your calorie consumption patterns.
          </p>
        </div>
      )}
    </div>
  );
};

export default WeeklySnapshot;
