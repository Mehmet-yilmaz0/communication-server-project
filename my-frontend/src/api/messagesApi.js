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
 * @param {string} messageData.encryptionMethod - Encryption method used (vigenere, caesar, etc.)
 * @param {number} messageData.receiver_id - Receiver user ID
 * @param {string} messageData.key - Encryption key
 * @returns {Promise<Object>} The created message object
 */
export const postMessage = async (messageData) => {
  const token = getToken();
  if (!token) {
    throw new Error("Authentication required");
  }

  // Map frontend encryption method names to backend method names
  const methodMap = {
    'none': 'vigenere', // Default to vigenere if none
    'aes': 'vigenere',
    'rsa': 'caesar',
    'sha256': 'shift',
    'base64': 'vigenere',
    'vigenere': 'vigenere',
    'caesar': 'caesar',
    'shift': 'shift',
  };

  const method = methodMap[messageData.encryptionMethod] || 'vigenere';
  const key = messageData.key || 'KEY'; // Default key if not provided

  // If no receiver_id provided, default to 1 (or handle differently)
  const receiver_id = messageData.receiver_id || 1;

  const response = await fetch(`${API_URL}/messages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      receiver_id: receiver_id,
      text: messageData.content,
      method: method,
      key: key,
    }),
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
 * @param {string} encryptionMethod - The encryption method used (vigenere, caesar, shift)
 * @param {string} password - The decryption key
 * @param {string} encryptedText - The encrypted text to decrypt
 * @returns {Promise<Object>} Decrypted message content
 */
export const decryptMessage = async (messageId, encryptionMethod, password, encryptedText) => {
  // Map frontend encryption method names to backend method names
  const methodMap = {
    'none': 'vigenere',
    'aes': 'vigenere',
    'rsa': 'caesar',
    'sha256': 'shift',
    'base64': 'vigenere',
    'vigenere': 'vigenere',
    'caesar': 'caesar',
    'shift': 'shift',
  };

  const method = methodMap[encryptionMethod] || 'vigenere';

  const response = await fetch(`${API_URL}/crypto/decrypt`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: encryptedText,
      method: method,
      key: password,
    }),
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