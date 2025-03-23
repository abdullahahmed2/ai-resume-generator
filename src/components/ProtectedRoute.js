import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function ProtectedRoute() {
  const { currentUser, loading } = useAuth();

  if (loading) {
    // You could render a loading spinner here
    return <div className="loading">Loading...</div>;
  }

  // If the user is not authenticated, redirect to login
  if (!currentUser) {
    return <Navigate to="/login" />;
  }

  // If the user is authenticated, render the child routes
  return <Outlet />;
}

export default ProtectedRoute; 