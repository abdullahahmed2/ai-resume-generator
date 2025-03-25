import React, { createContext, useState, useEffect, useContext } from 'react';
// Import still needed for type definition but we won't use it for API calls
import { authAPI } from '../services/api';

// Create the auth context
const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

// Demo user for bypassing auth
const DEMO_USER = {
  id: 1,
  email: "demo@example.com",
  is_active: true,
  is_admin: true
};

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(DEMO_USER);
  const [loading, setLoading] = useState(false);  // Start with false as we don't need to load
  const [error, setError] = useState(null);

  // Auto-login with demo user
  useEffect(() => {
    // Store a fake token to maintain the appearance of being logged in
    localStorage.setItem('token', 'demo_token');
    // Demo user is already set in state
  }, []);

  // Fetch the user's profile from the API - not used in demo mode
  const fetchUserProfile = async () => {
    // In demo mode, simply return the demo user
    return DEMO_USER;
  };

  // Register a new user - simplified in demo mode
  const register = async (email, password) => {
    // Simulate successful registration
    setCurrentUser(DEMO_USER);
    localStorage.setItem('token', 'demo_token');
    return DEMO_USER;
  };

  // Log in a user - simplified in demo mode
  const login = async (email, password) => {
    // Simulate successful login
    setCurrentUser(DEMO_USER);
    localStorage.setItem('token', 'demo_token');
    return true;
  };

  // Log out a user - simplified in demo mode
  const logout = () => {
    // In demo mode, we don't actually log out
    // Just redirect to login page which will auto-login again
  };

  // Clear any auth errors
  const clearError = () => setError(null);

  // The value object that will be provided to consumers of this context
  const value = {
    currentUser,
    loading,
    error,
    register,
    login,
    logout,
    clearError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
} 