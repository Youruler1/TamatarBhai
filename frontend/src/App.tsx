// Main App Component
// Tamatar-Bhai MVP - AI-powered food insights with bhai style personality

import { useState } from 'react';
import { TabType } from './types/components';
import ErrorBoundary from './components/ErrorBoundary';
import TabNavigation from './components/TabNavigation';
import { DailyPreview, SwitchupDiff, WeeklySnapshot } from './pages';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('preview');

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'preview':
        return <DailyPreview />;
      case 'compare':
        return <SwitchupDiff />;
      case 'weekly':
        return <WeeklySnapshot />;
      default:
        return <DailyPreview />;
    }
  };

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        {/* Header */}
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-4xl">🍅</span>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">Tamatar-Bhai</h1>
                  <p className="text-sm text-gray-600">AI-powered food insights</p>
                </div>
              </div>
              <div className="hidden sm:block text-right">
                <p className="text-sm text-gray-600">Bhai, khana khao aur mast raho!</p>
              </div>
            </div>
          </div>
        </header>

        {/* Tab Navigation */}
        <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />

        {/* Main Content */}
        <main className="flex-1">
          {renderActiveTab()}
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="text-center">
              <p className="text-sm text-gray-600">
                Built with ❤️ for the Tamatar-Bhai community
              </p>
              <p className="text-xs text-gray-500 mt-2">
                Powered by OpenAI & StabilityAI • 1-day MVP
              </p>
            </div>
          </div>
        </footer>
      </div>
    </ErrorBoundary>
  );
}

export default App;
