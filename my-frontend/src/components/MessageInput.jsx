import React, { useState, useEffect } from 'react';
import { postMessage } from '../api/messagesApi';
import { getUsers } from '../api/usersApi';

/**
 * MessageInput Component
 * 
 * Handles message input with encryption method, key input, and receiver selection.
 * Key input is shown/hidden based on algorithm requirements.
 * Receiver selection is required before sending messages.
 */
const MessageInput = ({ 
  selectedEncryptionMethod, 
  selectedMethodInfo,
  currentKey,
  onKeyChange,
  onMessageSent 
}) => {
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [keyError, setKeyError] = useState('');
  const [users, setUsers] = useState([]);
  const [usersLoading, setUsersLoading] = useState(true);
  const [selectedReceiver, setSelectedReceiver] = useState(null);
  const [receiverError, setReceiverError] = useState('');

  // Load users list on mount
  useEffect(() => {
    const loadUsers = async () => {
      try {
        setUsersLoading(true);
        const usersList = await getUsers();
        setUsers(usersList);
      } catch (error) {
        console.error('Failed to load users:', error);
        setUsers([]);
      } finally {
        setUsersLoading(false);
      }
    };

    loadUsers();
  }, []);

  // Validate receiver before submission
  const validateReceiver = () => {
    if (!selectedReceiver) {
      setReceiverError('Please select a receiver');
      return false;
    }
    setReceiverError('');
    return true;
  };

  // Validate key before submission
  const validateKey = () => {
    if (!selectedMethodInfo) {
      return true; // No method selected, will be handled elsewhere
    }

    // If key is not required, validation passes
    if (!selectedMethodInfo.requires_key) {
      return true;
    }

    // If key is required, check if it's provided
    const key = currentKey || '';
    if (!key.trim()) {
      setKeyError('Key is required for this algorithm');
      return false;
    }

    setKeyError('');
    return true;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!message.trim() || sending) {
      return;
    }

    // Validate receiver before sending
    if (!validateReceiver()) {
      return;
    }

    // Validate key before sending
    if (!validateKey()) {
      return;
    }

    setSending(true);
    
    try {
      // Prepare message data
      const messageData = {
        content: message.trim(),
        encryptionMethod: selectedEncryptionMethod,
        receiver_id: selectedReceiver.id, // From dropdown selection
        key: selectedMethodInfo.requires_key ? (currentKey || '').trim() : undefined
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

  // Handle key input change
  const handleKeyInputChange = (e) => {
    const newKey = e.target.value;
    onKeyChange(newKey);
    // Clear error when user starts typing
    if (keyError) {
      setKeyError('');
    }
  };

  // Get encryption method display info
  const getEncryptionInfo = () => {
    if (!selectedMethodInfo) {
      return { name: 'No Method', icon: '🔓', color: 'text-gray-400' };
    }
    
    return {
      name: selectedMethodInfo.label,
      icon: selectedMethodInfo.requires_key ? '🔐' : '🔓',
      color: selectedMethodInfo.requires_key ? 'text-blue-400' : 'text-gray-400'
    };
  };

  const encryptionInfo = getEncryptionInfo();
  const requiresKey = selectedMethodInfo?.requires_key || false;

  return (
    <div className="bg-gray-800 border-t border-gray-700 p-4">
      <form onSubmit={handleSubmit} className="space-y-3">
        {/* Receiver Selection */}
        <div className="flex items-start space-x-2">
          <div className="flex-1">
            <label htmlFor="receiver-select" className="block text-xs font-medium text-gray-300 mb-1">
              Select Receiver <span className="text-red-400">*</span>
            </label>
            <select
              id="receiver-select"
              value={selectedReceiver?.id || ''}
              onChange={(e) => {
                const receiverId = parseInt(e.target.value);
                const receiver = users.find(u => u.id === receiverId);
                setSelectedReceiver(receiver || null);
                if (receiverError) {
                  setReceiverError('');
                }
              }}
              className={`w-full bg-gray-700 text-gray-200 rounded-lg px-3 py-2 text-sm border transition-all duration-200 ${
                receiverError 
                  ? 'border-red-500 focus:border-red-500 focus:ring-2 focus:ring-red-500 focus:ring-opacity-20' 
                  : 'border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:ring-opacity-20'
              }`}
              disabled={sending || usersLoading}
            >
              <option value="">-- Select a receiver --</option>
              {users.map((user) => (
                <option key={user.id} value={user.id}>
                  {user.username}
                </option>
              ))}
            </select>
            {receiverError && (
              <p className="mt-1 text-xs text-red-400">{receiverError}</p>
            )}
            {usersLoading && (
              <p className="mt-1 text-xs text-gray-500">Loading users...</p>
            )}
            {!usersLoading && users.length === 0 && (
              <p className="mt-1 text-xs text-gray-500">No other users available</p>
            )}
          </div>
        </div>

        {/* Key Input Section */}
        {requiresKey && (
          <div className="flex items-start space-x-2">
            <div className="flex-1">
              <label htmlFor="encryption-key" className="block text-xs font-medium text-gray-300 mb-1">
                Encryption Key {selectedMethodInfo?.hint && (
                  <span className="text-gray-500 font-normal">({selectedMethodInfo.hint})</span>
                )}
              </label>
              <input
                id="encryption-key"
                type="text"
                value={currentKey || ''}
                onChange={handleKeyInputChange}
                placeholder="Enter encryption key"
                className={`w-full bg-gray-700 text-gray-200 placeholder-gray-400 rounded-lg px-3 py-2 text-sm border transition-all duration-200 ${
                  keyError 
                    ? 'border-red-500 focus:border-red-500 focus:ring-2 focus:ring-red-500 focus:ring-opacity-20' 
                    : 'border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:ring-opacity-20'
                }`}
                disabled={sending}
              />
              {keyError && (
                <p className="mt-1 text-xs text-red-400">{keyError}</p>
              )}
            </div>
          </div>
        )}

        {/* Main Input Row */}
        <div className="flex items-end space-x-3">
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
            disabled={!message.trim() || sending || !selectedReceiver || (requiresKey && !currentKey?.trim())}
            className="flex-shrink-0 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-xl px-6 py-3 transition-all duration-200 shadow-md hover:shadow-lg disabled:shadow-none flex items-center space-x-2"
            title={!selectedReceiver ? 'Please select a receiver' : ''}
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
        </div>

        {/* Help Text */}
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Press Enter to send, Shift+Enter for new line</span>
          <span>
            {selectedEncryptionMethod && '🔒 Encrypted'}
          </span>
        </div>
      </form>
    </div>
  );
};

export default MessageInput;
