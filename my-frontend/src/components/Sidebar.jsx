import React from 'react';

/**
 * Sidebar Component
 * 
 * Displays list of encryption methods from backend.
 * Minimal UI - just algorithm names, no tooltips/details.
 */
const Sidebar = ({ methods, selectedMethod, onMethodSelect }) => {
  if (!methods || methods.length === 0) {
    return (
      <div className="w-64 bg-gray-900 border-r border-gray-700 h-full flex flex-col">
        <div className="p-4">
          <p className="text-gray-400 text-sm">No encryption methods available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-64 bg-gray-900 border-r border-gray-700 h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-xl font-semibold text-gray-200 mb-2">
          🔒 Encryption Methods
        </h2>
        <p className="text-sm text-gray-400">
          {methods.length} method{methods.length !== 1 ? 's' : ''} available
        </p>
      </div>

      {/* Encryption Methods List */}
      <div className="flex-1 overflow-y-auto p-2">
        <div className="space-y-1">
          {methods.map((method) => (
            <button
              key={method.id}
              onClick={() => onMethodSelect(method.id)}
              className={`w-full text-left p-3 rounded-lg transition-all duration-200 ${
                selectedMethod === method.id
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-gray-200'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-medium text-sm truncate">
                  {method.label}
                </span>
                {selectedMethod === method.id && (
                  <div className="w-2 h-2 bg-blue-200 rounded-full flex-shrink-0 ml-2"></div>
                )}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-700">
        <div className="bg-gray-800 rounded-lg p-3">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-300">Secure Connection</span>
          </div>
          <p className="text-xs text-gray-400 mt-1">
            All communications are encrypted
          </p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
