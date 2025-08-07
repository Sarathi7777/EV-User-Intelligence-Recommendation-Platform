import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import HomePage from './components/HomePage';
import ProfilePage from './components/ProfilePage';
import MapPage from './components/MapPage';
import SettingsPage from './components/SettingsPage';
import Login from './components/Login';
import Register from './components/Register';
import AdminPanel from './components/AdminPanel';

const Navigation = ({ user, onLogout }) => {
  const navigate = useNavigate();
  
  const handleLogout = () => {
    onLogout();
    navigate('/');
  };

  return (
    <nav style={{ 
      backgroundColor: 'white', 
      padding: '1rem 2rem', 
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#28a745' }}>
          <Link to="/home" style={{ textDecoration: 'none', color: '#28a745' }}>
            ⚡ EV User Intelligence
          </Link>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <Link to="/home" style={{ 
            padding: '0.5rem 1rem', 
            textDecoration: 'none', 
            color: '#007bff',
            borderRadius: '4px',
            transition: 'background-color 0.2s'
          }}>
            🏠 Home
          </Link>
          <Link to="/map" style={{ 
            padding: '0.5rem 1rem', 
            textDecoration: 'none', 
            color: '#007bff',
            borderRadius: '4px',
            transition: 'background-color 0.2s'
          }}>
            🗺️ Map
          </Link>
          <Link to="/profile" style={{ 
            padding: '0.5rem 1rem', 
            textDecoration: 'none', 
            color: '#007bff',
            borderRadius: '4px',
            transition: 'background-color 0.2s'
          }}>
            👤 Profile
          </Link>
          <Link to="/settings" style={{ 
            padding: '0.5rem 1rem', 
            textDecoration: 'none', 
            color: '#007bff',
            borderRadius: '4px',
            transition: 'background-color 0.2s'
          }}>
            ⚙️ Settings
          </Link>
          {user.email === 'admin@example.com' && (
            <Link to="/admin" style={{ 
              padding: '0.5rem 1rem', 
              textDecoration: 'none', 
              color: '#dc3545',
              borderRadius: '4px',
              transition: 'background-color 0.2s'
            }}>
              👨‍💼 Admin
            </Link>
          )}
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <span style={{ color: '#6c757d' }}>
          Welcome, {user.email}
        </span>
        <button 
          onClick={handleLogout}
          style={{ 
            padding: '0.5rem 1rem', 
            backgroundColor: '#dc3545', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Logout
        </button>
      </div>
    </nav>
  );
};

const App = () => {
  const [user, setUser] = useState(null);

  // Restore user from localStorage on mount
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  if (!user) {
    return (
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/register" element={<Register onLogin={handleLogin} />} />
          <Route path="*" element={<LandingPage />} />
        </Routes>
      </Router>
    );
  }

  return (
    <Router>
      <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
        <Navigation user={user} onLogout={handleLogout} />
        <Routes>
          <Route path="/" element={<HomePage user={user} />} />
          <Route path="/home" element={<HomePage user={user} />} />
          <Route path="/profile" element={<ProfilePage user={user} />} />
          <Route path="/map" element={<MapPage user={user} />} />
          <Route path="/settings" element={<SettingsPage user={user} />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="*" element={<HomePage user={user} />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;