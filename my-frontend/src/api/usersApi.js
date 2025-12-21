// API functions for user operations
import { getToken } from './authApi';

const API_URL = "http://localhost:5000/api";

/**
 * Fetch all users except the currently logged-in user
 * @returns {Promise<Array>} Array of user objects with id and username
 */
export const getUsers = async () => {
  const token = getToken();
  if (!token) {
    throw new Error("Authentication required");
  }

  const response = await fetch(`${API_URL}/users`, {
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

  const users = await response.json();
  return users;
};

