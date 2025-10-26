import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import PasswordStatus from './components/PasswordStatus';

function App() {
  // State for selected encryption method
  const [selectedEncryptionMethod, setSelectedEncryptionMethod] = useState('none');
  
  // State for triggering chat refresh
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // Handle encryption method selection
  const handleEncryptionMethodSelect = (method) => {
    setSelectedEncryptionMethod(method);
  };

  // Handle new message sent (trigger refresh)
  const handleMessageSent = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="h-screen w-screen bg-gray-900 flex overflow-hidden">
      {/* Sidebar */}
      <Sidebar 
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
          onMessageSent={handleMessageSent}
        />
      </div>
    </div>
  );
}

export default App;
