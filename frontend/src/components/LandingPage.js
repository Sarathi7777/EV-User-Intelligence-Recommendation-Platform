import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      {/* Navigation */}
      <nav style={{ 
        backgroundColor: '#fff', 
        padding: '1rem 2rem', 
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#28a745' }}>
          ⚡ EV Platform
        </div>
        <div>
          <Link to="/login" style={{ 
            marginRight: '1rem', 
            padding: '0.5rem 1rem', 
            textDecoration: 'none', 
            color: '#007bff' 
          }}>
            Login
          </Link>
          <Link to="/register" style={{ 
            padding: '0.5rem 1rem', 
            backgroundColor: '#28a745', 
            color: 'white', 
            textDecoration: 'none', 
            borderRadius: '4px' 
          }}>
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <div style={{ 
        textAlign: 'center', 
        padding: '4rem 2rem', 
        backgroundColor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        background: 'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
        color: 'white'
      }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>
          Smart EV Charging Intelligence
        </h1>
        <p style={{ fontSize: '1.2rem', marginBottom: '2rem', opacity: 0.9 }}>
          Find, charge, and optimize your electric vehicle experience with AI-powered recommendations
        </p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}>
          <Link to="/register" style={{ 
            padding: '1rem 2rem', 
            backgroundColor: 'white', 
            color: '#28a745', 
            textDecoration: 'none', 
            borderRadius: '8px',
            fontWeight: 'bold'
          }}>
            Start Free Trial
          </Link>
          <Link to="/demo" style={{ 
            padding: '1rem 2rem', 
            border: '2px solid white', 
            color: 'white', 
            textDecoration: 'none', 
            borderRadius: '8px'
          }}>
            Watch Demo
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div style={{ padding: '4rem 2rem', backgroundColor: 'white' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '3rem', fontSize: '2.5rem' }}>
          Why Choose EV Platform?
        </h2>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: '2rem',
          maxWidth: '1200px',
          margin: '0 auto'
        }}>
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🗺️</div>
            <h3>Smart Station Finder</h3>
            <p>Real-time map with all charging stations, availability status, and route optimization</p>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🤖</div>
            <h3>AI Recommendations</h3>
            <p>Personalized station suggestions based on your driving patterns and preferences</p>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📊</div>
            <h3>Energy Analytics</h3>
            <p>Track your consumption, eco-score, and get insights to optimize your charging</p>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚡</div>
            <h3>Fast Charging</h3>
            <p>Find DC fast chargers and plan your trips with charging stops optimized</p>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🌱</div>
            <h3>Eco-Friendly</h3>
            <p>Reduce your carbon footprint with smart charging and green energy options</p>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📱</div>
            <h3>Mobile First</h3>
            <p>Access your charging data anywhere with our responsive mobile app</p>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div style={{ 
        padding: '4rem 2rem', 
        backgroundColor: '#f8f9fa',
        textAlign: 'center'
      }}>
        <h2 style={{ marginBottom: '3rem', fontSize: '2.5rem' }}>
          Platform Statistics
        </h2>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '2rem',
          maxWidth: '800px',
          margin: '0 auto'
        }}>
          <div>
            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#28a745' }}>500+</div>
            <div>Charging Stations</div>
          </div>
          <div>
            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#28a745' }}>10K+</div>
            <div>Active Users</div>
          </div>
          <div>
            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#28a745' }}>50K+</div>
            <div>Charging Sessions</div>
          </div>
          <div>
            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#28a745' }}>95%</div>
            <div>User Satisfaction</div>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div style={{ padding: '4rem 2rem', backgroundColor: 'white' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '3rem', fontSize: '2.5rem' }}>
          How It Works
        </h2>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '2rem',
          maxWidth: '1000px',
          margin: '0 auto'
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              width: '60px', 
              height: '60px', 
              backgroundColor: '#28a745', 
              borderRadius: '50%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              color: 'white',
              fontSize: '1.5rem',
              margin: '0 auto 1rem'
            }}>
              1
            </div>
            <h3>Sign Up</h3>
            <p>Create your account and add your vehicle details</p>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              width: '60px', 
              height: '60px', 
              backgroundColor: '#28a745', 
              borderRadius: '50%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              color: 'white',
              fontSize: '1.5rem',
              margin: '0 auto 1rem'
            }}>
              2
            </div>
            <h3>Find Stations</h3>
            <p>Browse the interactive map to find nearby charging stations</p>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              width: '60px', 
              height: '60px', 
              backgroundColor: '#28a745', 
              borderRadius: '50%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              color: 'white',
              fontSize: '1.5rem',
              margin: '0 auto 1rem'
            }}>
              3
            </div>
            <h3>Charge & Track</h3>
            <p>Start charging and track your session in real-time</p>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              width: '60px', 
              height: '60px', 
              backgroundColor: '#28a745', 
              borderRadius: '50%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              color: 'white',
              fontSize: '1.5rem',
              margin: '0 auto 1rem'
            }}>
              4
            </div>
            <h3>Get Insights</h3>
            <p>View analytics and get personalized recommendations</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer style={{ 
        backgroundColor: '#343a40', 
        color: 'white', 
        padding: '3rem 2rem',
        textAlign: 'center'
      }}>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '2rem',
          maxWidth: '1200px',
          margin: '0 auto'
        }}>
          <div>
            <h3>EV Platform</h3>
            <p>Smart charging solutions for electric vehicle owners</p>
          </div>
          <div>
            <h4>Features</h4>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li>Station Finder</li>
              <li>AI Recommendations</li>
              <li>Energy Analytics</li>
              <li>Route Planning</li>
            </ul>
          </div>
          <div>
            <h4>Support</h4>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li>Help Center</li>
              <li>Contact Us</li>
              <li>FAQ</li>
              <li>Community</li>
            </ul>
          </div>
          <div>
            <h4>Legal</h4>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li>Privacy Policy</li>
              <li>Terms of Service</li>
              <li>Cookie Policy</li>
              <li>Data Protection</li>
            </ul>
          </div>
        </div>
        <div style={{ marginTop: '2rem', paddingTop: '2rem', borderTop: '1px solid #6c757d' }}>
          <p>&copy; 2024 EV Platform. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage; 