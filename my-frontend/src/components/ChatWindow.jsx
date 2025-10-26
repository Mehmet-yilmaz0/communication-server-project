import React, { useState, useEffect, useRef } from 'react';
import { getMessages } from '../api/messagesApi';
import DecryptPanel from './DecryptPanel';

const ChatWindow = ({ refreshTrigger }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [decryptedMessages, setDecryptedMessages] = useState({}); // Track decrypted content per message
  const [hoveredMessage, setHoveredMessage] = useState(null); // Track which message is hovered
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Fetch messages from API
  const fetchMessages = async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedMessages = await getMessages();
      setMessages(fetchedMessages);
    } catch (err) {
      setError('Failed to load messages');
      console.error('Error fetching messages:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch messages on component mount and when refreshTrigger changes
  useEffect(() => {
    fetchMessages();
  }, [refreshTrigger]);

  // Auto-scroll when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle message decryption callback
  const handleDecrypted = (messageId, decryptedData) => {
    setDecryptedMessages((prev) => ({
      ...prev,
      [messageId]: decryptedData.content || decryptedData.text || 'Decrypted successfully',
    }));
    // Hide the panel after successful decryption
    setHoveredMessage(null);
  };

  // Get display content for a message (encrypted or decrypted)
  const getMessageContent = (message) => {
    if (message.encrypted && decryptedMessages[message.id]) {
      return decryptedMessages[message.id];
    }
    return message.content;
  };

  // Format timestamp for display
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Get message bubble styling based on sender and encryption
  const getMessageStyle = (message) => {
    const isSystem = message.sender === 'System';
    const isCurrentUser = message.sender === 'Current User';
    
    if (isSystem) {
      return 'bg-gray-700 text-gray-300 border border-gray-600';
    }
    
    if (isCurrentUser) {
      return 'bg-blue-600 text-white ml-auto';
    }
    
    return 'bg-gray-800 text-gray-200 border border-gray-600';
  };

  if (loading) {
    return (
      <div className="flex-1 bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading messages...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-400 text-4xl mb-4">⚠️</div>
          <p className="text-red-400 mb-2">{error}</p>
          <button
            onClick={fetchMessages}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 bg-gray-900 flex flex-col">
      {/* Chat Header */}
      <div className="bg-gray-800 border-b border-gray-700 p-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-gray-200">
              💬 Secure Chat
            </h1>
            <p className="text-sm text-gray-400">
              {messages.length} message{messages.length !== 1 ? 's' : ''}
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-400">Online</span>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="text-6xl mb-4">💬</div>
              <p className="text-gray-400 text-lg mb-2">No messages yet</p>
              <p className="text-gray-500 text-sm">
                Start the conversation by sending a message below
              </p>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message-enter flex ${message.sender === 'Current User' ? 'justify-end' : 'justify-start'}`}
              onMouseEnter={() => {
                // Only show decrypt panel if message is encrypted and not already decrypted
                if (message.encrypted && !decryptedMessages[message.id]) {
                  setHoveredMessage(message.id);
                }
              }}
              onMouseLeave={() => {
                setHoveredMessage(null);
              }}
            >
              {/* Message Container with Hover Effect */}
              <div className={`relative max-w-xs lg:max-w-md group ${message.sender === 'Current User' ? 'ml-auto' : ''}`}>
                <div className={`px-4 py-3 rounded-2xl shadow-md transition-all duration-200 ${getMessageStyle(message)} ${hoveredMessage === message.id ? 'opacity-70' : ''}`}>
                  {/* Message Header */}
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-medium opacity-75">
                      {message.sender}
                    </span>
                    {message.encrypted && !decryptedMessages[message.id] && (
                      <span className="text-xs opacity-75">🔒</span>
                    )}
                    {decryptedMessages[message.id] && (
                      <span className="text-xs opacity-75">🔓</span>
                    )}
                  </div>

                  {/* Message Content */}
                  <p className="text-sm leading-relaxed break-words">
                    {getMessageContent(message)}
                  </p>

                  {/* Message Footer */}
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-xs opacity-60">
                      {formatTime(message.timestamp)}
                    </span>
                    {message.encryptionMethod && message.encryptionMethod !== 'none' && (
                      <span className="text-xs opacity-60 bg-gray-600 px-2 py-1 rounded">
                        {message.encryptionMethod.toUpperCase()}
                      </span>
                    )}
                  </div>
                </div>

                {/* Decrypt Panel - Shows on hover for encrypted messages */}
                {hoveredMessage === message.id && message.encrypted && !decryptedMessages[message.id] && (
                  <DecryptPanel
                    messageId={message.id}
                    encryptionMethod={message.encryptionMethod || 'aes'}
                    onDecrypted={(decryptedData) => handleDecrypted(message.id, decryptedData)}
                    onError={(errorMessage) => console.error('Decryption error:', errorMessage)}
                  />
                )}
              </div>
            </div>
          ))
        )}
        
        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatWindow;
