import React, { useState } from "react";
import { apiService, PreviewResponse } from "../services/api";
import LoadingSkeleton from "../components/LoadingSkeleton";
import ImageWithFallback from "../components/ImageWithFallback";
import { ChefHat, Clock, Utensils, Sparkles } from "lucide-react";

const DailyPreview: React.FC = () => {
  const [dish, setDish] = useState("");
  const [meal, setMeal] = useState("lunch");
  const [isLoading, setIsLoading] = useState(false);
  const [preview, setPreview] = useState<PreviewResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mealOptions = [
    { value: "breakfast", label: "🌅 Breakfast", icon: "☕" },
    { value: "lunch", label: "☀️ Lunch", icon: "🍽️" },
    { value: "dinner", label: "🌙 Dinner", icon: "🍴" },
    { value: "snack", label: "🍪 Snack", icon: "🥨" },
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!dish.trim()) {
      setError("Please enter a dish name");
      return;
    }

    setIsLoading(true);
    setError(null);
    setPreview(null);

    try {
      const result = await apiService.generatePreview({
        dish: dish.trim(),
        meal,
      });
      setPreview(result);
    } catch (err: any) {
      console.error("Preview generation failed:", err);
      setError(
        err.response?.data?.message ||
          "Failed to generate preview. Please try again."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setDish("");
    setMeal("lunch");
    setPreview(null);
    setError(null);
  };

  return (
    <div className="fade-in space-y-6">
      {/* Input Form */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center mb-6">
          <ChefHat className="w-6 h-6 text-red-500 mr-2" />
          <h2 className="text-xl font-semibold text-gray-900">Daily Preview</h2>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Dish Input */}
            <div>
              <label
                htmlFor="dish"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                <Utensils className="w-4 h-4 inline mr-1" />
                Dish Name
              </label>
              <input
                type="text"
                id="dish"
                value={dish}
                onChange={(e) => setDish(e.target.value)}
                placeholder="e.g., Butter Chicken, Dal Tadka, Biryani"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors"
                disabled={isLoading}
              />
            </div>

            {/* Meal Type */}
            <div>
              <label
                htmlFor="meal"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                <Clock className="w-4 h-4 inline mr-1" />
                Meal Type
              </label>
              <select
                id="meal"
                value={meal}
                onChange={(e) => setMeal(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors"
                disabled={isLoading}
              >
                {mealOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button
              type="submit"
              disabled={isLoading || !dish.trim()}
              className={`flex-1 flex items-center justify-center px-4 py-2 rounded-md font-medium transition-colors ${
                isLoading || !dish.trim()
                  ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                  : "bg-red-600 text-white hover:bg-red-700"
              } ${isLoading ? "btn-loading" : ""}`}
            >
              {!isLoading && <Sparkles className="w-4 h-4 mr-2" />}
              {isLoading ? "Generating..." : "Generate Preview"}
            </button>

            {(preview || error) && (
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

      {/* Preview Results */}
      {preview && !isLoading && (
        <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900">
                {preview.dish}
              </h3>
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <span className="flex items-center">
                  <Clock className="w-4 h-4 mr-1" />
                  {meal.charAt(0).toUpperCase() + meal.slice(1)}
                </span>
                <span className="font-semibold text-red-600">
                  {preview.calories} cal
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Image Section */}
              <div className="space-y-4">
                <div className="aspect-square rounded-lg overflow-hidden bg-gray-100">
                  <ImageWithFallback
                    src={preview.image_url}
                    alt={preview.dish}
                    className="w-full h-full image-hover"
                  />
                </div>

                {preview.meta.matched_dish &&
                  preview.meta.matched_dish !== preview.dish && (
                    <div className="text-xs text-gray-500 bg-gray-50 p-2 rounded">
                      <span className="font-medium">Matched:</span>{" "}
                      {preview.meta.matched_dish}
                      {preview.meta.confidence && (
                        <span className="ml-2">
                          ({Math.round(preview.meta.confidence * 100)}%
                          confidence)
                        </span>
                      )}
                    </div>
                  )}
              </div>

              {/* Captions Section */}
              <div className="space-y-4">
                {/* Bhai Style Caption */}
                <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <span className="text-orange-600 font-medium text-sm">
                      🤙 Bhai Style
                    </span>
                  </div>
                  <p className="text-gray-800 leading-relaxed">
                    {preview.captions.bhai}
                  </p>
                </div>

                {/* Formal Caption */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <span className="text-blue-600 font-medium text-sm">
                      📋 Formal
                    </span>
                  </div>
                  <p className="text-gray-800 leading-relaxed">
                    {preview.captions.formal}
                  </p>
                </div>

                {/* Nutrition Info */}
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <span className="text-green-600 font-medium text-sm">
                      🥗 Nutrition
                    </span>
                  </div>
                  <div className="text-2xl font-bold text-green-700">
                    {preview.calories} calories
                  </div>
                  <p className="text-green-600 text-sm mt-1">
                    Perfect for your {meal}!
                  </p>
                </div>
              </div>
            </div>

            {/* API Attribution */}
            <div className="mt-6 pt-4 border-t border-gray-200">
              <div className="flex flex-col space-y-2">
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>Generated by {preview.meta.model}</span>
                  <span>
                    {new Date(preview.meta.generated_at).toLocaleString()}
                  </span>
                </div>
                <div className="text-xs text-gray-400 text-center">
                  🤖 AI-powered content by OpenAI • 🎨 Images by StabilityAI
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Help Text */}
      {!preview && !isLoading && !error && (
        <div className="text-center py-8">
          <span className="text-4xl mb-4 block">🍽️</span>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Ready to explore your dish?
          </h3>
          <p className="text-gray-600 max-w-md mx-auto">
            Enter any Indian dish name and get AI-generated images, calorie
            information, and both bhai-style and formal descriptions.
          </p>
        </div>
      )}
    </div>
  );
};

export default DailyPreview;
