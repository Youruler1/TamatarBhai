// TabNavigation Component
// Top-level navigation for the three main features

import { TabNavigationProps, TabType } from '../types/components';

const TabNavigation = ({ activeTab, onTabChange }: TabNavigationProps) => {
  const tabs: { id: TabType; label: string; icon: string }[] = [
    { id: 'preview', label: 'Daily Preview', icon: '🍽️' },
    { id: 'compare', label: 'Switch-up Diff', icon: '⚖️' },
    { id: 'weekly', label: 'Weekly Snapshot', icon: '📊' },
  ];

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex space-x-8">
          {tabs.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`
                  flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors
                  ${
                    isActive
                      ? 'border-red-500 text-red-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
                aria-current={isActive ? 'page' : undefined}
              >
                <span className="text-xl">{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

export default TabNavigation;
