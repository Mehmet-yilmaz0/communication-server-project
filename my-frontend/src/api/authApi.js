// API functions for authentication
const API_URL = "http://localhost:5000/api";

/**
 * Register a new user
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise<Object>} Response with access_token and user
 */
export async function register(username, password) {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.error || "Registration failed");
  }

  return res.json();
}

/**
 * Login user
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise<Object>} Response with access_token and user
 */
export async function login(username, password) {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.error || "Login failed");
  }

  return res.json();
}

/**
 * Get token from localStorage
 * @returns {string|null} Token or null
 */
export function getToken() {
  return localStorage.getItem("access_token");
}

/**
 * Save token to localStorage
 * @param {string} token - JWT token
 */
export function saveToken(token) {
  localStorage.setItem("access_token", token);
}

/**
 * Remove token from localStorage
 */
export function removeToken() {
  localStorage.removeItem("access_token");
}

/**
 * Check if token exists and is valid
 * @returns {Promise<boolean>} True if token is valid, false otherwise
 */
export async function validateToken() {
  const token = getToken();
  if (!token) {
    return false;
  }

  try {
    // Try to verify token by making a request to a protected endpoint
    const res = await fetch(`${API_URL}/messages`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    // If we get 401, token is invalid/expired
    if (res.status === 401) {
      removeToken();
      return false;
    }

    // If we get 200 or other success status, token is valid
    return res.ok;
  } catch (error) {
    // Network error or other issues - assume token is invalid
    console.error("Token validation error:", error);
    removeToken();
    return false;
  }
}

/**
 * Logout user - clears token and redirects to login
 */
export function logout() {
  removeToken();
  // Note: Navigation will be handled by the component using this function
}

