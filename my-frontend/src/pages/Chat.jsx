import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';
import MessageInput from '../components/MessageInput';
import PasswordStatus from '../components/PasswordStatus';
import { getEncryptionMethods } from '../api/cryptoApi';

/**
 * Chat Page Component
 * 
 * Main chat interface with encryption methods sidebar,
 * message window, and input field.
 */
const Chat = () => {
  // State for encryption methods (loaded from backend)
  const [encryptionMethods, setEncryptionMethods] = useState([]);
  const [methodsLoading, setMethodsLoading] = useState(true);
  
  // State for selected encryption method (algorithm ID)
  const [selectedEncryptionMethod, setSelectedEncryptionMethod] = useState(null);
  
  // State for keys per algorithm (algorithm ID -> key mapping)
  const [algorithmKeys, setAlgorithmKeys] = useState({});
  
  // State for triggering chat refresh
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // Load encryption methods from backend on mount
  useEffect(() => {
    const loadMethods = async () => {
      try {
        setMethodsLoading(true);
        const methods = await getEncryptionMethods();
        setEncryptionMethods(methods);
        
        // Set first method as default if none selected
        if (methods.length > 0 && !selectedEncryptionMethod) {
          setSelectedEncryptionMethod(methods[0].id);
        }
      } catch (error) {
        console.error('Failed to load encryption methods:', error);
        // Fallback: empty array, will show error state
        setEncryptionMethods([]);
      } finally {
        setMethodsLoading(false);
      }
    };

    loadMethods();
  }, []);

  // Handle encryption method selection
  const handleEncryptionMethodSelect = (methodId) => {
    setSelectedEncryptionMethod(methodId);
  };

  // Handle key change for a specific algorithm
  const handleKeyChange = (algorithmId, key) => {
    setAlgorithmKeys(prev => ({
      ...prev,
      [algorithmId]: key
    }));
  };

  // Get current key for selected algorithm
  const getCurrentKey = () => {
    return algorithmKeys[selectedEncryptionMethod] || '';
  };

  // Handle new message sent (trigger refresh)
  const handleMessageSent = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  // Show loading state while methods are loading
  if (methodsLoading) {
    return (
      <div className="h-screen w-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading encryption methods...</p>
        </div>
      </div>
    );
  }

  // Show error state if no methods loaded
  if (encryptionMethods.length === 0) {
    return (
      <div className="h-screen w-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-400 text-4xl mb-4">⚠️</div>
          <p className="text-red-400 mb-2">Failed to load encryption methods</p>
          <p className="text-gray-500 text-sm">Please check your connection and try again</p>
        </div>
      </div>
    );
  }

  // Get selected method info
  const selectedMethodInfo = encryptionMethods.find(m => m.id === selectedEncryptionMethod) || encryptionMethods[0];

  return (
    <div className="h-screen w-screen bg-gray-900 flex overflow-hidden">
      {/* Sidebar */}
      <Sidebar 
        methods={encryptionMethods}
        selectedMethod={selectedEncryptionMethod}
        onMethodSelect={handleEncryptionMethodSelect}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative">
        {/* Password Status (floating) */}
        <PasswordStatus />

        {/* Chat Window */}
        <ChatWindow refreshTrigger={refreshTrigger} />

        {/* Message Input */}
        <MessageInput 
          selectedEncryptionMethod={selectedEncryptionMethod}
          selectedMethodInfo={selectedMethodInfo}
          currentKey={getCurrentKey()}
          onKeyChange={(key) => handleKeyChange(selectedEncryptionMethod, key)}
          onMessageSent={handleMessageSent}
        />
      </div>
    </div>
  );
};

export default Chat;

