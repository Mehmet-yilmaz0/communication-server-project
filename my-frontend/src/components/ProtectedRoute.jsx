import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { getToken, validateToken } from '../api/authApi';

/**
 * ProtectedRoute Component
 * 
 * Protects routes that require authentication.
 * 
 * Behavior:
 * - If no token → redirect to /login
 * - If token exists → validate it
 * - If token is invalid/expired → clear token and redirect to /login
 * - If token is valid → render children
 * 
 * @param {React.ReactNode} children - Components to render if authenticated
 */
const ProtectedRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null); // null = checking, true = authenticated, false = not authenticated
  const [isValidating, setIsValidating] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const token = getToken();
      
      if (!token) {
        // No token, not authenticated
        setIsAuthenticated(false);
        setIsValidating(false);
        return;
      }

      // Token exists, validate it
      try {
        const isValid = await validateToken();
        setIsAuthenticated(isValid);
      } catch (error) {
        console.error('Token validation error:', error);
        setIsAuthenticated(false);
      } finally {
        setIsValidating(false);
      }
    };

    checkAuth();
  }, []);

  // Show loading state while validating
  if (isValidating) {
    return (
      <div className="h-screen w-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Verifying authentication...</p>
        </div>
      </div>
    );
  }

  // If not authenticated, redirect to login
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // If authenticated, render children
  return children;
};

export default ProtectedRoute;

