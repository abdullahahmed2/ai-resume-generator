import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Navbar.css';

function Navbar() {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          AI Resume Generator
        </Link>

        <div className="navbar-menu">
          {currentUser ? (
            <>
              <Link to="/dashboard" className="navbar-item">
                Dashboard
              </Link>
              <Link to="/templates" className="navbar-item">
                Templates
              </Link>
              <div className="navbar-user">
                <span className="navbar-email">{currentUser.email}</span>
                <button onClick={handleLogout} className="navbar-logout">
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-item">
                Log In
              </Link>
              <Link to="/register" className="navbar-item navbar-btn">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar; 