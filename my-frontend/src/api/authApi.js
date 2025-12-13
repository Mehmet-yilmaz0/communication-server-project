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

