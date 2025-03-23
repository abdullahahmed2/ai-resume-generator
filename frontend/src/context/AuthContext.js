import React, { createContext, useState, useEffect, useContext } from 'react';
import { authAPI } from '../services/api';

// Create the auth context
const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if user is logged in on initial load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetchUserProfile();
    } else {
      setLoading(false);
    }
  }, []);

  // Fetch the user's profile from the API
  const fetchUserProfile = async () => {
    try {
      setLoading(true);
      const response = await authAPI.getUser();
      setCurrentUser(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching user profile:', err);
      setError('Failed to fetch user profile');
      // If the token is invalid, clear it
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        logout();
      }
    } finally {
      setLoading(false);
    }
  };

  // Register a new user
  const register = async (email, password) => {
    try {
      setLoading(true);
      const response = await authAPI.register({ email, password });
      return response.data;
    } catch (err) {
      console.error('Registration error:', err);
      const errorMessage = err.response?.data?.detail || 'Registration failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Log in a user
  const login = async (email, password) => {
    try {
      setLoading(true);
      const response = await authAPI.login({
        username: email, // FastAPI OAuth2 expects 'username' field
        password: password,
      });
      
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      
      // Fetch the user profile after successful login
      await fetchUserProfile();
      return true;
    } catch (err) {
      console.error('Login error:', err);
      const errorMessage = err.response?.data?.detail || 'Login failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Log out a user
  const logout = () => {
    localStorage.removeItem('token');
    setCurrentUser(null);
    setError(null);
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