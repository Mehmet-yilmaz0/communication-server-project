// API functions for message operations
// TODO: Replace with actual backend endpoints when available

const BASE_URL = 'http://localhost:3001'; // Replace with your actual backend URL

/**
 * Fetch all messages from the server
 * @returns {Promise<Array>} Array of message objects
 */
export const getMessages = async () => {
  try {
    // TODO: Replace with actual GET endpoint
    const response = await fetch(`${BASE_URL}/api/messages`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Add authentication headers if needed
        // 'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const messages = await response.json();
    return messages;
  } catch (error) {
    console.error('Error fetching messages:', error);
    // Return dummy data for development
    return [
      {
        id: 1,
        content: "Welcome to the secure chat! 🔒",
        timestamp: new Date().toISOString(),
        sender: "System",
        encrypted: false
      },
      {
        id: 2,
        content: "This is a sample message to demonstrate the UI",
        timestamp: new Date(Date.now() - 60000).toISOString(),
        sender: "User1",
        encrypted: true
      },
      {
        id: 3,
        content: "Encryption methods are available in the sidebar",
        timestamp: new Date(Date.now() - 120000).toISOString(),
        sender: "User2",
        encrypted: false
      }
    ];
  }
};

/**
 * Send a new message to the server
 * @param {Object} messageData - The message data to send
 * @param {string} messageData.content - Message content
 * @param {string} messageData.encryptionMethod - Encryption method used
 * @param {boolean} messageData.encrypted - Whether message is encrypted
 * @returns {Promise<Object>} The created message object
 */
export const postMessage = async (messageData) => {
  try {
    // TODO: Replace with actual POST endpoint
    const response = await fetch(`${BASE_URL}/api/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add authentication headers if needed
        // 'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        content: messageData.content,
        encryptionMethod: messageData.encryptionMethod || 'none',
        encrypted: messageData.encrypted || false,
        timestamp: new Date().toISOString(),
        sender: 'Current User', // TODO: Get from auth context
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const newMessage = await response.json();
    return newMessage;
  } catch (error) {
    console.error('Error posting message:', error);
    // Return dummy data for development
    return {
      id: Date.now(),
      content: messageData.content,
      timestamp: new Date().toISOString(),
      sender: 'Current User',
      encrypted: messageData.encrypted || false,
      encryptionMethod: messageData.encryptionMethod || 'none'
    };
  }
};

/**
 * Delete a message by ID
 * @param {number|string} messageId - The ID of the message to delete
 * @returns {Promise<boolean>} Success status
 */
export const deleteMessage = async (messageId) => {
  try {
    // TODO: Replace with actual DELETE endpoint
    const response = await fetch(`${BASE_URL}/api/messages/${messageId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        // Add authentication headers if needed
        // 'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return true;
  } catch (error) {
    console.error('Error deleting message:', error);
    return false;
  }
};
