# 🚗 EV User Intelligence & Recommendation Platform

A comprehensive electric vehicle charging platform with real-time station data, ML-powered recommendations, and advanced analytics.

## ✨ Features

- **Real-time Data**: Live charging station data from Open Charge Map API
- **Enterprise Storage**: Scalable data warehouse with Snowflake
- **ML Recommendations**: Collaborative filtering and user clustering
- **Interactive Maps**: Real-time station location and availability
- **Analytics Dashboard**: Energy consumption and usage insights
- **Admin Panel**: Station and user management
- **Forecasting**: Energy demand prediction and station usage analytics
- **AI Chatbot**: Intelligent EV assistant powered by OpenRouter API

## 🚀 Quick Start

### Prerequisites

1. **OpenRouter API Key** (for AI Chatbot): Get from [OpenRouter](https://openrouter.ai/)
2. **Open Charge Map API Key**: Get from [Open Charge Map](https://openchargemap.io/site/develop/api)
3. **Snowflake Account**: For data warehouse storage

### Option 1: Automated Setup (Recommended)

```bash
# Run the automated setup script
python setup_snowflake_integration.py
```

This will guide you through:
- Snowflake configuration
- Open Charge Map API setup
- Database table creation
- Initial data ingestion

### Option 2: Manual Setup

1. **Configure Environment**
   ```bash
   # Copy environment template
   cp env_template.txt backend/.env
   
   # Edit backend/.env with your credentials
   # - Snowflake credentials
   # - Open Charge Map API key
   # - OpenRouter API key (for AI chatbot)
   ```

2. **Set up OpenRouter API (AI Chatbot)**
   ```bash
   # Set environment variable
   export OPENROUTER_API_KEY="sk-or-v1-your-api-key-here"
   
   # Test configuration
   cd backend
   python ../test_openrouter_config.py
   ```

### Option 2: Manual Setup

1. **Configure Environment**
   ```bash
   # Copy environment template
   cp env_template.txt backend/.env
   
   # Edit backend/.env with your credentials
   # - Snowflake credentials
   # - Open Charge Map API key
   ```

2. **Set up Snowflake**
   ```bash
   # Run the enhanced schema
   # Copy contents of db/create_tables.sql to Snowflake web interface
   ```

3. **Install Dependencies**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   npm install
   ```

4. **Start the Application**
   ```bash
   # Backend (Terminal 1)
   cd backend
   python -m uvicorn app:app --reload
   
   # Frontend (Terminal 2)
   cd frontend
   npm start
   ```

5. **Access the Platform**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📊 Data Sources

### Open Charge Map API
- **Free API Key**: Get from [Open Charge Map](https://openchargemap.io/site/develop/api)
- **Coverage**: 8+ countries (US, CA, GB, DE, FR, NL, AU, JP)
- **Data Types**: Station locations, energy types, availability
- **Update Frequency**: Real-time via API

### Snowflake Data Warehouse
- **Storage**: Enterprise-grade cloud data warehouse
- **Tables**: Stations, users, sessions, analytics, ML features
- **Performance**: Optimized indexes and query patterns
- **Scalability**: Handles millions of records

## 🏗️ Architecture

```
UV-Cursor/
├── backend/                 # FastAPI Backend
│   ├── app.py              # Main application
│   ├── api/                # REST API endpoints
│   │   ├── stations.py     # Station management (Snowflake + OCM)
│   │   ├── users.py        # User authentication
│   │   ├── recommendations.py # ML recommendations
│   │   ├── sessions.py     # Charging sessions
│   │   ├── admin.py        # Admin panel
│   │   ├── chatbot.py      # AI chatbot with OpenRouter integration
│   │   └── forecast.py     # Energy demand prediction
│   ├── core/               # Core utilities
│   │   ├── config.py       # Configuration management
│   │   └── security.py     # Authentication
│   └── models/             # Pydantic schemas
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── App.js          # Main app component
│   │   ├── components/     # React components
│   │   │   ├── MapView.js  # Interactive map (Leaflet)
│   │   │   ├── Dashboard.js # Analytics dashboard
│   │   │   ├── Login.js    # User authentication
│   │   │   └── AdminPanel.js # Admin interface
│   │   └── index.js        # React entry point
├── db/                     # Database Layer
│   ├── snowflake_connector.py # Enhanced Snowflake manager
│   ├── fetch_and_store_ocm.py # Open Charge Map integration
│   └── create_tables.sql   # Enhanced database schema
├── models/                 # ML Models
│   ├── recommendation.py   # Collaborative filtering
│   ├── clustering.py       # User pattern clustering
│   └── train_lightfm.py   # Model training
├── deploy/                 # Deployment
│   ├── Dockerfile          # Docker configuration
│   └── ec2_setup.sh       # AWS deployment
└── docs/                   # Documentation
    ├── SNOWFLAKE_INTEGRATION.md # Complete integration guide
    └── PROJECT_SUMMARY.md  # Project overview
```

## 🔌 API Endpoints

### Stations
- `GET /stations/` - Get all stations (Snowflake + fallback)
- `GET /stations/nearby` - Get nearby stations with distance calculation
- `GET /stations/count` - Get station count and data source
- `GET /stations/statistics` - Get comprehensive statistics

### Users & Authentication
- `POST /login` - User authentication
- `GET /admin/users` - Get all users (admin)

### ML & Analytics
- `POST /recommendations` - Get personalized station recommendations
- `GET /forecast/energy-demand` - Energy demand forecasting
- `GET /forecast/station-usage/{station_id}` - Station usage prediction

### Sessions
- `POST /sessions` - Log charging session
- `GET /sessions/{user_id}` - Get user session history

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Snowflake** - Enterprise data warehouse
- **Pydantic** - Data validation and serialization
- **scikit-learn** - Machine learning algorithms
- **NumPy/Pandas** - Data processing

### Frontend
- **React** - User interface framework
- **Leaflet** - Interactive maps
- **Plotly** - Data visualization
- **Axios** - HTTP client

### ML/AI
- **Collaborative Filtering** - Station recommendations
- **K-Means Clustering** - User pattern classification
- **Time Series Forecasting** - Energy demand prediction

### Data Sources
- **Open Charge Map API** - Real charging station data
- **Snowflake** - Scalable data warehouse
- **Mock Data** - Development and testing

## 📈 Data Analytics

### Station Analytics
- Total stations by country and energy type
- Availability percentages
- Usage patterns and peak hours
- Revenue metrics

### User Analytics
- Eco-scores and sustainability tracking
- Charging behavior patterns
- Energy consumption trends
- Cost analysis

### ML Features
- User clustering for personalized recommendations
- Station popularity scoring
- Demand forecasting models
- Anomaly detection

## 🔧 Configuration

### Environment Variables
```env
# Snowflake Configuration
SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema

# Open Charge Map API
OCM_API_KEY=your_openchargemap_api_key

# ML Model Path
RECOMMENDATION_MODEL_PATH=models/recommendation_model.pkl
```

### Database Schema
The enhanced schema includes:
- **Stations**: Comprehensive station data with OCM integration
- **Users**: User profiles with analytics and preferences
- **Sessions**: Detailed charging session tracking
- **Station Usage**: Analytics and forecasting data
- **User Preferences**: ML features and personalization
- **Recommendations**: ML recommendation storage
- **Forecasts**: Energy demand predictions
- **Audit Log**: System monitoring and debugging

## 🧪 Testing

### Integration Testing
```bash
# Test complete Snowflake integration
python test_snowflake_integration.py
```

### API Testing
```bash
# Test API endpoints
curl http://localhost:8000/stations/
curl http://localhost:8000/stations/count
```

## 📚 Documentation

- **[Snowflake Integration Guide](SNOWFLAKE_INTEGRATION.md)** - Complete setup and usage
- **[Project Summary](PROJECT_SUMMARY.md)** - Detailed project overview
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker
docker build -t ev-platform -f deploy/Dockerfile .
docker run -p 8000:8000 ev-platform
```

### AWS EC2 Deployment
```bash
# Deploy to AWS EC2
chmod +x deploy/ec2_setup.sh
./deploy/ec2_setup.sh
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the [Snowflake Integration Guide](SNOWFLAKE_INTEGRATION.md)
2. Review the [Project Summary](PROJECT_SUMMARY.md)
3. Test your setup with `python test_snowflake_integration.py`
4. Check the API documentation at http://localhost:8000/docs

## 🎉 Success!

Once configured, your EV User Intelligence will have:
- ✅ Real charging station data from 8+ countries
- ✅ Enterprise-grade data storage with Snowflake
- ✅ Advanced analytics and ML capabilities
- ✅ Scalable architecture for growth
- ✅ Comprehensive monitoring and maintenance tools

Your platform is now ready for production use! 🚗⚡

