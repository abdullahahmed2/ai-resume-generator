import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import './styles/App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <Navbar />
          <main className="main-content">
            <Routes>
              {/* Public routes - kept for appearances but will auto-redirect to dashboard */}
              <Route path="/login" element={<Navigate to="/dashboard" />} />
              <Route path="/register" element={<Navigate to="/dashboard" />} />
              
              {/* All routes now act as if they're protected */}
              <Route path="/dashboard" element={<Dashboard />} />
              {/* Add these routes as we develop the components */}
              {/* <Route path="/resume/new" element={<CreateResume />} /> */}
              {/* <Route path="/resume/edit/:id" element={<EditResume />} /> */}
              {/* <Route path="/resume/share/:id" element={<ShareResume />} /> */}
              {/* <Route path="/templates" element={<Templates />} /> */}
              
              {/* Default route */}
              <Route path="*" element={<Navigate to="/dashboard" />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App; 