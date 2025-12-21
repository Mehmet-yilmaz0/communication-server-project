import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { UserProvider } from './contexts/UserContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Chat from './pages/Chat';
import ProtectedRoute from './components/ProtectedRoute';

/**
 * Main App Component with Routing
 * 
 * Routes:
 * - /login - Login page (public)
 * - /register - Register page (public)
 * - /chat - Chat page (protected, requires authentication)
 * - / - Redirects to /chat if authenticated, /login otherwise
 */
function App() {
  return (
    <UserProvider>
      <Router>
        <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes */}
        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          }
        />

        {/* Default Route - Redirect based on auth status */}
        <Route path="/" element={<Navigate to="/chat" replace />} />

        {/* Catch all - redirect to chat */}
        <Route path="*" element={<Navigate to="/chat" replace />} />
        </Routes>
      </Router>
    </UserProvider>
  );
}

export default App;
