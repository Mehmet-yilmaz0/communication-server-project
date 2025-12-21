import React, { createContext, useContext, useState, useEffect } from 'react';
import { getToken } from '../api/authApi';

/**
 * UserContext
 * 
 * Provides global access to the current logged-in user information.
 * User info is extracted from JWT token.
 */
const UserContext = createContext(null);

/**
 * UserProvider Component
 * 
 * Wraps the app and provides user context to all children.
 */
export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = () => {
      try {
        const token = getToken();
        
        if (!token) {
          setUser(null);
          setLoading(false);
          return;
        }

        // Decode JWT token to get user info
        // JWT format: header.payload.signature
        // We only need payload (base64 encoded)
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          
          // Extract user info from token payload
          setUser({
            id: payload.user_id,
            username: payload.username
          });
        } catch (error) {
          console.error('Failed to decode token:', error);
          setUser(null);
        }
      } catch (error) {
        console.error('Error loading user:', error);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    loadUser();

    // Listen for storage changes (e.g., logout)
    const handleStorageChange = () => {
      loadUser();
    };

    window.addEventListener('storage', handleStorageChange);
    
    // Also check periodically (in case token is removed in same tab)
    const interval = setInterval(() => {
      const token = getToken();
      if (!token && user) {
        setUser(null);
      }
    }, 1000);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      clearInterval(interval);
    };
  }, [user]);

  return (
    <UserContext.Provider value={{ user, loading }}>
      {children}
    </UserContext.Provider>
  );
};

/**
 * useUser Hook
 * 
 * Custom hook to access user context.
 * 
 * @returns {Object} { user: { id, username } | null, loading: boolean }
 */
export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within UserProvider');
  }
  return context;
};

