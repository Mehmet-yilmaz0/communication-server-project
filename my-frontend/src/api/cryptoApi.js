// API functions for crypto operations
const API_URL = "http://localhost:5000/api";

/**
 * Fetch all available encryption methods from the backend
 * @returns {Promise<Array>} Array of method objects with id, label, requires_key, hint
 */
export const getEncryptionMethods = async () => {
  try {
    const response = await fetch(`${API_URL}/crypto/methods`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.error || `HTTP error! status: ${response.status}`);
    }

    const methods = await response.json();
    return methods;
  } catch (error) {
    console.error("Error fetching encryption methods:", error);
    throw error;
  }
};

