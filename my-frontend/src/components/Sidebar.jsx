import React, { useState } from 'react';

const Sidebar = ({ selectedMethod, onMethodSelect }) => {
  // List of available encryption methods
  const encryptionMethods = [
    { id: 'none', name: 'No Encryption', icon: '🔓', description: 'Send messages without encryption' },
    { id: 'aes', name: 'AES-256', icon: '🔐', description: 'Advanced Encryption Standard' },
    { id: 'rsa', name: 'RSA-2048', icon: '🔑', description: 'Rivest-Shamir-Adleman' },
    { id: 'sha256', name: 'SHA-256', icon: '🛡️', description: 'Secure Hash Algorithm' },
    { id: 'base64', name: 'Base64', icon: '📝', description: 'Base64 encoding' },
  ];

  return (
    <div className="w-64 bg-gray-900 border-r border-gray-700 h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-xl font-semibold text-gray-200 mb-2">
          🔒 Encryption Methods
        </h2>
        <p className="text-sm text-gray-400">
          Choose your preferred encryption method
        </p>
      </div>

      {/* Encryption Methods List */}
      <div className="flex-1 overflow-y-auto p-2">
        <div className="space-y-1">
          {encryptionMethods.map((method) => (
            <button
              key={method.id}
              onClick={() => onMethodSelect(method.id)}
              className={`w-full text-left p-3 rounded-lg transition-all duration-200 group ${
                selectedMethod === method.id
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-gray-200'
              }`}
            >
              <div className="flex items-center space-x-3">
                <span className="text-lg">{method.icon}</span>
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-sm truncate">
                    {method.name}
                  </div>
                  <div className={`text-xs truncate ${
                    selectedMethod === method.id 
                      ? 'text-blue-100' 
                      : 'text-gray-400 group-hover:text-gray-300'
                  }`}>
                    {method.description}
                  </div>
                </div>
                {selectedMethod === method.id && (
                  <div className="w-2 h-2 bg-blue-200 rounded-full"></div>
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
