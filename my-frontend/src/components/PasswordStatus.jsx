import React, { useState, useEffect } from 'react';

const PasswordStatus = () => {
  const [isLocked, setIsLocked] = useState(true);
  const [showDetails, setShowDetails] = useState(false);

  // Simulate password status changes (placeholder logic)
  useEffect(() => {
    // This is just for demo purposes - in real app, this would come from auth context
    const interval = setInterval(() => {
      // Randomly toggle status for demo
      if (Math.random() > 0.8) {
        setIsLocked(prev => !prev);
      }
    }, 10000); // Change every 10 seconds

    return () => clearInterval(interval);
  }, []);

  const statusConfig = {
    locked: {
      icon: '🔒',
      text: 'Locked',
      bgColor: 'bg-red-600',
      hoverBgColor: 'hover:bg-red-700',
      textColor: 'text-red-100',
      borderColor: 'border-red-500',
      statusColor: 'bg-red-400'
    },
    unlocked: {
      icon: '🔓',
      text: 'Unlocked',
      bgColor: 'bg-green-600',
      hoverBgColor: 'hover:bg-green-700',
      textColor: 'text-green-100',
      borderColor: 'border-green-500',
      statusColor: 'bg-green-400'
    }
  };

  const config = isLocked ? statusConfig.locked : statusConfig.unlocked;

  return (
    <div className="absolute top-4 right-4 z-10">
      {/* Main Status Button */}
      <button
        onClick={() => setShowDetails(!showDetails)}
        className={`${config.bgColor} ${config.hoverBgColor} ${config.borderColor} ${config.textColor} px-4 py-2 rounded-xl shadow-lg border transition-all duration-200 flex items-center space-x-2 backdrop-blur-sm`}
      >
        <span className="text-lg">{config.icon}</span>
        <span className="font-medium text-sm">{config.text}</span>
        <div className={`w-2 h-2 ${config.statusColor} rounded-full animate-pulse`}></div>
      </button>

      {/* Details Panel */}
      {showDetails && (
        <div className="absolute top-12 right-0 bg-gray-800 border border-gray-600 rounded-xl shadow-xl p-4 min-w-64 backdrop-blur-sm">
          <div className="space-y-3">
            {/* Header */}
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-gray-200 text-sm">
                Password Status
              </h3>
              <button
                onClick={() => setShowDetails(false)}
                className="text-gray-400 hover:text-gray-200 transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Status Details */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-gray-400 text-sm">Status:</span>
                <span className={`text-sm font-medium ${config.textColor}`}>
                  {isLocked ? 'Locked' : 'Unlocked'}
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-gray-400 text-sm">Last Change:</span>
                <span className="text-gray-300 text-sm">
                  {new Date().toLocaleTimeString()}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-gray-400 text-sm">Security:</span>
                <span className="text-gray-300 text-sm">
                  {isLocked ? 'High' : 'Medium'}
                </span>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="pt-2 border-t border-gray-600">
              <div className="flex space-x-2">
                <button
                  onClick={() => setIsLocked(!isLocked)}
                  className={`flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isLocked 
                      ? 'bg-green-600 hover:bg-green-700 text-green-100'
                      : 'bg-red-600 hover:bg-red-700 text-red-100'
                  }`}
                >
                  {isLocked ? 'Unlock' : 'Lock'}
                </button>
                <button className="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-gray-300 rounded-lg text-sm font-medium transition-colors">
                  Settings
                </button>
              </div>
            </div>

            {/* Help Text */}
            <div className="pt-2 border-t border-gray-600">
              <p className="text-xs text-gray-500">
                {isLocked 
                  ? 'Password protection is active. Messages are encrypted.'
                  : 'Password protection is disabled. Messages are not encrypted.'
                }
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Click outside to close */}
      {showDetails && (
        <div 
          className="fixed inset-0 z-[-1]" 
          onClick={() => setShowDetails(false)}
        />
      )}
    </div>
  );
};

export default PasswordStatus;
