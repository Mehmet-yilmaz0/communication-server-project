// API functions for message operations
import { getToken } from './authApi';

const API_URL = "http://localhost:5000/api";

/**
 * Fetch all messages from the server
 * @returns {Promise<Array>} Array of message objects
 */
export const getMessages = async () => {
  const token = getToken();
  if (!token) {
    throw new Error("Authentication required");
  }

  const response = await fetch(`${API_URL}/messages`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `HTTP error! status: ${response.status}`);
  }

  const messages = await response.json();
  // Transform backend format to frontend format
  return messages.map((msg) => ({
    id: msg.id,
    content: msg.encrypted_content,
    timestamp: msg.created_at,
    sender: `User${msg.sender_id}`,
    encrypted: true,
    encryptionMethod: msg.method,
  }));
};

/**
 * Send a new message to the server
 * @param {Object} messageData - The message data to send
 * @param {string} messageData.content - Message content (plain text)
 * @param {string} messageData.encryptionMethod - Encryption method ID (vigenere, caesar, etc.) - directly from backend
 * @param {number} messageData.receiver_id - Receiver user ID (required, must be provided)
 * @param {string} messageData.key - Encryption key (optional, only if algorithm requires it)
 * @returns {Promise<Object>} The created message object
 */
export const postMessage = async (messageData) => {
  const token = getToken();
  if (!token) {
    throw new Error("Authentication required");
  }

  // Validate required fields
  if (!messageData.content || !messageData.content.trim()) {
    throw new Error("Message content is required");
  }

  if (!messageData.encryptionMethod) {
    throw new Error("Encryption method is required");
  }

  if (!messageData.receiver_id) {
    throw new Error("Receiver is required. Please select a receiver.");
  }

  // Prepare request body
  const requestBody = {
    receiver_id: messageData.receiver_id, // Must be provided, no default
    text: messageData.content.trim(),
    method: messageData.encryptionMethod, // Direct algorithm ID, no mapping
  };

  // Only include key if provided (some algorithms don't require key)
  if (messageData.key !== undefined && messageData.key !== null && messageData.key !== '') {
    requestBody.key = messageData.key;
  }

  const response = await fetch(`${API_URL}/messages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `HTTP error! status: ${response.status}`);
  }

  const newMessage = await response.json();
  return newMessage;
};

/**
 * Delete a message by ID
 * @param {number|string} messageId - The ID of the message to delete
 * @returns {Promise<boolean>} Success status
 */
export const deleteMessage = async (messageId) => {
  const token = getToken();
  if (!token) {
    throw new Error("Authentication required");
  }

  const response = await fetch(`${API_URL}/messages/${messageId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `HTTP error! status: ${response.status}`);
  }

  return true;
};

/**
 * Decrypt an encrypted message
 * @param {number|string} messageId - The ID of the message to decrypt (not used in API, kept for compatibility)
 * @param {string} encryptionMethod - The encryption method ID (vigenere, caesar, etc.) - directly from backend
 * @param {string} password - The decryption key
 * @param {string} encryptedText - The encrypted text to decrypt
 * @returns {Promise<Object>} Decrypted message content
 */
export const decryptMessage = async (messageId, encryptionMethod, password, encryptedText) => {
  // Validate required fields
  if (!encryptionMethod || !encryptedText) {
    throw new Error("Encryption method and encrypted text are required");
  }

  // Prepare request body
  const requestBody = {
    text: encryptedText,
    method: encryptionMethod, // Direct algorithm ID, no mapping
  };

  // Only include key if provided (some algorithms don't require key)
  if (password !== undefined && password !== null && password !== '') {
    requestBody.key = password;
  }

  const response = await fetch(`${API_URL}/crypto/decrypt`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || "Failed to decrypt message. Invalid key.");
  }

  const decryptedData = await response.json();
  return {
    content: decryptedData.decrypted,
    decrypted: true,
  };
};