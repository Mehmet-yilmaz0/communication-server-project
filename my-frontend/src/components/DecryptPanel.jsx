import React, { useState } from 'react';
import { decryptMessage } from '../api/messagesApi';

/**
 * DecryptPanel Component
 * Appears on hover over encrypted messages to allow password entry and decryption
 */
const DecryptPanel = ({ messageId, encryptionMethod, encryptedText, onDecrypted, onError }) => {
  const [password, setPassword] = useState('');
  const [isDecrypting, setIsDecrypting] = useState(false);
  const [error, setError] = useState(null);

  // Handle decryption
  const handleDecrypt = async () => {
    if (!password.trim()) {
      setError('Please enter a password');
      return;
    }

    setIsDecrypting(true);
    setError(null);

    try {
      // Call the API to decrypt the message
      const decryptedData = await decryptMessage(messageId, encryptionMethod, password, encryptedText);
      
      // Call the callback with the decrypted content
      if (onDecrypted) {
        onDecrypted(decryptedData);
      }

      // Clear password for security
      setPassword('');
    } catch (err) {
      // Show error message
      const errorMessage = err.message || 'Invalid password. Please try again.';
      setError(errorMessage);
      
      // Call error callback if provided
      if (onError) {
        onError(errorMessage);
      }
      
      // Clear password on error for retry
      setPassword('');
    } finally {
      setIsDecrypting(false);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isDecrypting) {
      handleDecrypt();
    }
  };

  return (
    <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm rounded-2xl group-hover:opacity-100 transition-all duration-200">
      <div className="bg-gray-800 border border-gray-600 rounded-xl p-3 shadow-xl max-w-xs w-full transform transition-all duration-200 hover:scale-105">
        {/* Error Message */}
        {error && (
          <div className="mb-2 px-2 py-1 bg-red-600 bg-opacity-20 border border-red-500 rounded text-xs text-red-300">
            {error}
          </div>
        )}

        <div className="flex items-center space-x-2">
          {/* Password Input */}
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter password"
            className="flex-1 bg-gray-700 text-gray-200 placeholder-gray-400 rounded-lg px-3 py-2 text-sm border border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:ring-opacity-20 transition-all duration-200"
            disabled={isDecrypting}
            autoFocus
          />

          {/* Unlock Button */}
          <button
            onClick={handleDecrypt}
            disabled={isDecrypting || !password.trim()}
            className="flex-shrink-0 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg px-3 py-2 transition-all duration-200 shadow-md hover:shadow-lg disabled:shadow-none flex items-center space-x-1"
          >
            {isDecrypting ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span className="text-xs">Decrypting...</span>
              </>
            ) : (
              <>
                <span>🔓</span>
                <span className="text-xs">Unlock</span>
              </>
            )}
          </button>
        </div>

        {/* Help Text */}
        <p className="text-xs text-gray-400 mt-2 text-center">
          {encryptionMethod.toUpperCase()} Encrypted
        </p>
      </div>
    </div>
  );
};

export default DecryptPanel;

