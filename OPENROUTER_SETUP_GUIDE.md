# OpenRouter API Key Setup Guide

This guide explains how to configure the OpenRouter API key for the AI chatbot functionality in both the backend and frontend of the EV User Intelligence Platform.

## Prerequisites

1. **OpenRouter Account**: Sign up at [https://openrouter.ai/](https://openrouter.ai/)
2. **API Key**: Generate an API key from your OpenRouter dashboard
3. **Credits**: Ensure you have sufficient credits for API calls

## Backend Configuration

### 1. Environment Variables

The backend uses environment variables to store sensitive configuration. You have several options:

#### Option A: Create a .env file (Recommended for development)
Create a `.env` file in the `backend/` directory:

```bash
# Navigate to backend directory
cd backend

# Create .env file
touch .env
```

Add the following content to your `.env` file:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key-here

# Other configurations...
DATABASE_URL=your_database_url_here
SNOWFLAKE_ACCOUNT=your_snowflake_account
# ... (other variables as needed)
```

#### Option B: Set environment variables directly
```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-or-v1-your-actual-api-key-here"

# Windows Command Prompt
set OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key-here

# Linux/Mac
export OPENROUTER_API_KEY="sk-or-v1-your-actual-api-key-here"
```

### 2. Configuration File

The backend configuration is centralized in `backend/core/config.py`. The OpenRouter API key is automatically loaded from environment variables.

### 3. Verification

Test your backend configuration:

```bash
# Navigate to backend directory
cd backend

# Start the backend server
python -m uvicorn app:app --reload

# Test the chatbot health endpoint
curl http://localhost:8000/api/chatbot/health
```

Expected response:
```json
{
  "status": "healthy",
  "openrouter_configured": true,
  "timestamp": "2024-01-01T12:00:00"
}
```

## Frontend Configuration

### 1. Environment Configuration

The frontend uses a configuration file `frontend/env.config.js` that can be customized for different environments.

#### For Development:
Update `frontend/env.config.js`:

```javascript
const envConfig = {
  // OpenRouter API Configuration
  OPENROUTER_API_KEY: 'sk-or-v1-your-actual-api-key-here',
  
  // Backend API Configuration
  BACKEND_API_URL: 'http://localhost:8000',
  
  // Other configuration variables
  APP_NAME: 'EV User Intelligence Platform',
  VERSION: '1.0.0'
};
```

#### For Production:
Set environment variables with the `REACT_APP_` prefix:

```bash
# Windows PowerShell
$env:REACT_APP_OPENROUTER_API_KEY="sk-or-v1-your-actual-api-key-here"

# Windows Command Prompt
set REACT_APP_OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key-here

# Linux/Mac
export REACT_APP_OPENROUTER_API_KEY="sk-or-v1-your-actual-api-key-here"
```

### 2. Fallback Mechanism

The frontend includes a fallback mechanism:
1. **Primary**: Uses the backend API endpoint (`/api/chatbot/chat`)
2. **Fallback**: If backend fails, makes direct calls to OpenRouter API
3. **Final Fallback**: Provides helpful static responses for common queries

### 3. Testing Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start the development server
npm start
```

Open your browser and test the chatbot widget to ensure it's working with the OpenRouter API.

## Security Considerations

### 1. API Key Protection
- **Never commit API keys to version control**
- **Use environment variables for production deployments**
- **Rotate API keys regularly**
- **Monitor API usage and costs**

### 2. Rate Limiting
- OpenRouter has rate limits based on your plan
- Implement client-side rate limiting if needed
- Monitor API response times and errors

### 3. CORS Configuration
- Ensure your backend allows requests from your frontend domain
- Configure proper CORS headers in production

## Troubleshooting

### Common Issues

#### 1. "AI service not configured" Error
- Check if `OPENROUTER_API_KEY` is set in environment variables
- Verify the API key format starts with `sk-or-v1-`
- Restart the backend server after setting environment variables

#### 2. "AI service authentication failed" Error
- Verify your API key is correct
- Check if your OpenRouter account has sufficient credits
- Ensure the API key hasn't expired

#### 3. Frontend Fallback Not Working
- Check browser console for CORS errors
- Verify the OpenRouter API key in `env.config.js`
- Ensure the frontend can reach the OpenRouter API endpoint

### Debug Endpoints

The backend provides debug endpoints to help troubleshoot:

```bash
# Check environment configuration
curl http://localhost:8000/api/chatbot/debug

# Check chatbot health
curl http://localhost:8000/api/chatbot/health
```

## Production Deployment

### 1. Environment Variables
Set environment variables in your production environment:

```bash
# Example for Docker
docker run -e OPENROUTER_API_KEY="sk-or-v1-your-key" your-app

# Example for systemd service
Environment="OPENROUTER_API_KEY=sk-or-v1-your-key"
```

### 2. Frontend Build
For production builds, ensure environment variables are properly set:

```bash
# Build with environment variables
REACT_APP_OPENROUTER_API_KEY="sk-or-v1-your-key" npm run build
```

### 3. Monitoring
- Monitor API usage and costs
- Set up alerts for API failures
- Log chatbot interactions for debugging

## Support

If you encounter issues:
1. Check the debug endpoints
2. Review the logs for error messages
3. Verify your OpenRouter account status
4. Test with a simple API call to OpenRouter directly

For OpenRouter-specific issues, visit their [documentation](https://openrouter.ai/docs) or [support](https://openrouter.ai/support).
