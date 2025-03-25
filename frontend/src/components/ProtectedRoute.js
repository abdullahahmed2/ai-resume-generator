import React from 'react';
import { Outlet } from 'react-router-dom';

function ProtectedRoute() {
  // In demo mode, we always allow access to protected routes
  return <Outlet />;
}

export default ProtectedRoute; 