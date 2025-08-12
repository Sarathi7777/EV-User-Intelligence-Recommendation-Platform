// Environment Configuration for Frontend
// This file contains environment variables that can be used in the React application
// For production, these should be set as actual environment variables

const envConfig = {
  // OpenRouter API Configuration (do NOT hardcode secrets here)
  OPENROUTER_API_KEY: process.env.REACT_APP_OPENROUTER_API_KEY || '',
  
  // Backend API Configuration
  BACKEND_API_URL: process.env.REACT_APP_BACKEND_API_URL || 'http://localhost:8000',
  
  // Other configuration variables
  APP_NAME: 'EV User Intelligence Platform',
  VERSION: '1.0.0'
};

export default envConfig;
