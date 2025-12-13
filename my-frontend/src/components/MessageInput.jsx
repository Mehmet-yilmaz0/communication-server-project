import React, { useState } from 'react';
import { postMessage } from '../api/messagesApi';

const MessageInput = ({ selectedEncryptionMethod, onMessageSent }) => {
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!message.trim() || sending) {
      return;
    }

    setSending(true);
    
    try {
      // Prepare message data
      // Note: receiver_id and key should ideally come from user input or context
      // For now, using defaults - you may want to add UI for these
      const messageData = {
        content: message.trim(),
        encryptionMethod: selectedEncryptionMethod,
        encrypted: selectedEncryptionMethod !== 'none',
        receiver_id: 1, // TODO: Get from user selection or context
        key: 'KEY' // TODO: Get from user input or context
      };

      // Send message to API
      await postMessage(messageData);
      
      // Clear input and trigger refresh
      setMessage('');
      onMessageSent(); // This will trigger a refresh in the parent component
      
    } catch (error) {
      console.error('Error sending message:', error);
      // You could add a toast notification here
    } finally {
      setSending(false);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Get encryption method display info
  const getEncryptionInfo = () => {
    const methods = {
      'none': { name: 'No Encryption', icon: '🔓', color: 'text-gray-400' },
      'aes': { name: 'AES-256', icon: '🔐', color: 'text-blue-400' },
      'rsa': { name: 'RSA-2048', icon: '🔑', color: 'text-green-400' },
      'sha256': { name: 'SHA-256', icon: '🛡️', color: 'text-yellow-400' },
      'base64': { name: 'Base64', icon: '📝', color: 'text-purple-400' }
    };
    
    return methods[selectedEncryptionMethod] || methods['none'];
  };

  const encryptionInfo = getEncryptionInfo();

  return (
    <div className="bg-gray-800 border-t border-gray-700 p-4">
      <form onSubmit={handleSubmit} className="flex items-end space-x-3">
        {/* Encryption Method Indicator */}
        <div className="flex-shrink-0">
          <div className={`flex items-center space-x-2 px-3 py-2 rounded-lg bg-gray-700 ${encryptionInfo.color}`}>
            <span className="text-sm">{encryptionInfo.icon}</span>
            <span className="text-xs font-medium">
              {encryptionInfo.name}
            </span>
          </div>
        </div>

        {/* Message Input */}
        <div className="flex-1 relative">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={`Type your message... (${encryptionInfo.name})`}
            className="w-full bg-gray-700 text-gray-200 placeholder-gray-400 rounded-xl px-4 py-3 pr-12 resize-none border border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:ring-opacity-20 transition-all duration-200"
            rows="1"
            style={{
              minHeight: '48px',
              maxHeight: '120px'
            }}
            disabled={sending}
          />
          
          {/* Character count (optional) */}
          {message.length > 100 && (
            <div className="absolute bottom-1 right-12 text-xs text-gray-400">
              {message.length}
            </div>
          )}
        </div>

        {/* Send Button */}
        <button
          type="submit"
          disabled={!message.trim() || sending}
          className="flex-shrink-0 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-xl px-6 py-3 transition-all duration-200 shadow-md hover:shadow-lg disabled:shadow-none flex items-center space-x-2"
        >
          {sending ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Sending...</span>
            </>
          ) : (
            <>
              <span>Send</span>
              <svg 
                className="w-4 h-4" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" 
                />
              </svg>
            </>
          )}
        </button>
      </form>

      {/* Help Text */}
      <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
        <span>Press Enter to send, Shift+Enter for new line</span>
        <span>
          {selectedEncryptionMethod !== 'none' && '🔒 Encrypted'}
        </span>
      </div>
    </div>
  );
};

export default MessageInput;
