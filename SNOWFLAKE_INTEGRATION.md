# 🚗 EV Platform - Snowflake Integration Guide

This guide explains how to connect your EV User Intelligence & Recommendation Platform to Snowflake and fetch real charging station data from the Open Charge Map API.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Setup](#quick-setup)
4. [Manual Configuration](#manual-configuration)
5. [Data Ingestion](#data-ingestion)
6. [API Usage](#api-usage)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Features](#advanced-features)

## 🎯 Overview

The enhanced Snowflake integration provides:

- **Real-time Data**: Live charging station data from Open Charge Map API
- **Scalable Storage**: Enterprise-grade data warehouse with Snowflake
- **Advanced Analytics**: Built-in views and queries for insights
- **ML Integration**: Support for recommendation systems and forecasting
- **High Performance**: Optimized indexes and query patterns

## ✅ Prerequisites

### 1. Snowflake Account
- Active Snowflake account with admin privileges
- Warehouse, database, and schema created
- User with appropriate permissions

### 2. Open Charge Map API Key
- Free API key from [Open Charge Map](https://openchargemap.io/site/develop/api)
- No credit card required

### 3. Python Environment
- Python 3.8+ with required packages
- All dependencies installed (see `backend/requirements.txt`)

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
python setup_snowflake_integration.py
```

This script will:
- Guide you through configuration
- Test connections
- Create database tables
- Optionally fetch initial data

### Option 2: Manual Setup

Follow the manual configuration steps below.

## ⚙️ Manual Configuration

### 1. Create Environment File

Create `backend/.env` with your credentials:

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

### 2. Create Database Tables

Run the enhanced schema:

```bash
# Option 1: Using Snowflake web interface
# Copy and paste the contents of db/create_tables.sql

# Option 2: Using Python
python -c "
from db.snowflake_connector import SnowflakeManager
manager = SnowflakeManager()
manager.create_tables()
print('Tables created successfully!')
"
```

### 3. Test Connection

```python
from db.snowflake_connector import SnowflakeManager

# Test connection
manager = SnowflakeManager()
result = manager.execute_query("SELECT CURRENT_VERSION() as version")
print(f"Snowflake version: {result[0]['version']}")
```

## 📊 Data Ingestion

### Fetch Open Charge Map Data

```python
from db.fetch_and_store_ocm import OpenChargeMapFetcher

# Initialize fetcher
fetcher = OpenChargeMapFetcher()

# Fetch data for specific countries
countries = ["US", "CA", "GB"]
results = fetcher.run_full_ingestion(countries, max_stations_per_country=500)

print(f"Fetched: {results['summary']['total_fetched']} stations")
print(f"Stored: {results['summary']['total_stored']} stations")
```

### Available Countries

- **US**: United States
- **CA**: Canada
- **GB**: United Kingdom
- **DE**: Germany
- **FR**: France
- **NL**: Netherlands
- **AU**: Australia
- **JP**: Japan

### Data Quality

The ingestion process includes:
- **Data Validation**: Coordinates, required fields
- **Deduplication**: Prevents duplicate stations
- **Error Handling**: Graceful failure recovery
- **Rate Limiting**: Respects API limits

## 🔌 API Usage

### Enhanced Endpoints

#### Get All Stations
```bash
GET /stations/
```
Returns stations from Snowflake (with mock fallback)

#### Get Nearby Stations
```bash
GET /stations/nearby?lat=37.7749&lon=-122.4194&radius=10&use_snowflake=true&use_ocm=true
```
Parameters:
- `lat`, `lon`: User location
- `radius`: Search radius in km
- `use_snowflake`: Use Snowflake database
- `use_ocm`: Include Open Charge Map data

#### Get Station Count
```bash
GET /stations/count
```
Returns total station count and data source

#### Get Statistics
```bash
GET /stations/statistics
```
Returns comprehensive station statistics

### Response Examples

#### Station Data
```json
{
  "id": 1,
  "name": "Downtown Charging Station",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "energy_type": "Level 2",
  "available": true,
  "address_line1": "123 Main St",
  "town": "San Francisco",
  "state": "California",
  "country": "United States"
}
```

#### Nearby Station
```json
{
  "id": "1",
  "name": "Downtown Charging Station",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "energy_type": "Level 2",
  "available": true,
  "distance_km": 2.5,
  "travel_time_minutes": 5,
  "source": "snowflake"
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Snowflake Connection Failed
```
Error: Missing Snowflake configuration
```
**Solution**: Check your `.env` file and ensure all Snowflake credentials are set.

#### 2. OCM API Errors
```
Error: OCM_API_KEY not found
```
**Solution**: Get a free API key from [Open Charge Map](https://openchargemap.io/site/develop/api).

#### 3. Table Creation Failed
```
Error: Insufficient privileges
```
**Solution**: Ensure your Snowflake user has CREATE TABLE permissions.

#### 4. Data Ingestion Timeout
```
Error: Request timeout
```
**Solution**: Reduce `max_stations_per_country` or add delays between requests.

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Test specific components
from db.snowflake_connector import SnowflakeManager
manager = SnowflakeManager()
manager.execute_query("SELECT 1 as test")
```

### Performance Optimization

#### 1. Warehouse Sizing
```sql
-- Use appropriate warehouse size for your workload
ALTER WAREHOUSE your_warehouse SET WAREHOUSE_SIZE = 'MEDIUM';
```

#### 2. Query Optimization
```sql
-- Use the provided indexes
SELECT * FROM stations 
WHERE latitude BETWEEN 37.7 AND 37.8 
  AND longitude BETWEEN -122.5 AND -122.4;
```

#### 3. Batch Operations
```python
# Use batch inserts for large datasets
manager.insert_stations_batch(stations_list)
```

## 🚀 Advanced Features

### 1. Custom Queries

```python
# Execute custom SQL
query = """
SELECT 
    country,
    COUNT(*) as station_count,
    AVG(CASE WHEN available THEN 1 ELSE 0 END) * 100 as availability
FROM stations 
GROUP BY country 
ORDER BY station_count DESC
"""

results = manager.execute_query(query)
```

### 2. Real-time Updates

```python
# Update station availability
def update_station_availability(station_id: int, available: bool):
    query = "UPDATE stations SET available = %s WHERE id = %s"
    manager.execute_query(query, (available, station_id))
```

### 3. Analytics Views

The schema includes pre-built views:

```sql
-- Station usage summary
SELECT * FROM station_usage_summary;

-- User activity summary  
SELECT * FROM user_activity_summary;
```

### 4. ML Integration

```python
# Get user preferences for ML models
query = """
SELECT user_id, preferred_energy_type, max_travel_distance_km
FROM user_preferences
WHERE user_cluster = %s
"""

user_features = manager.execute_query(query, (cluster_id,))
```

## 📈 Monitoring

### 1. Data Quality Metrics

```python
# Check data completeness
query = """
SELECT 
    COUNT(*) as total_stations,
    COUNT(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 END) as with_coordinates,
    COUNT(CASE WHEN energy_type IS NOT NULL THEN 1 END) as with_energy_type
FROM stations
"""

quality_metrics = manager.execute_query(query)
```

### 2. Performance Monitoring

```python
# Monitor query performance
import time

start_time = time.time()
results = manager.get_stations_by_location(37.7749, -122.4194, 10)
query_time = time.time() - start_time

print(f"Query executed in {query_time:.2f} seconds")
```

## 🔄 Maintenance

### 1. Regular Data Updates

```python
# Schedule regular OCM data updates
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', hour=2)  # Daily at 2 AM
def update_station_data():
    fetcher = OpenChargeMapFetcher()
    fetcher.run_full_ingestion(["US"], max_stations_per_country=100)

scheduler.start()
```

### 2. Database Maintenance

```sql
-- Clean up old audit logs
DELETE FROM audit_log 
WHERE created_at < DATEADD(month, -6, CURRENT_TIMESTAMP());

-- Update statistics
ANALYZE TABLE stations;
```

## 📞 Support

For issues and questions:

1. **Check the logs**: Look for detailed error messages
2. **Verify credentials**: Ensure all environment variables are set
3. **Test connections**: Use the setup script to verify configuration
4. **Review documentation**: Check this guide and `PROJECT_SUMMARY.md`

## 🎉 Success!

Once configured, your EV platform will have:

- ✅ Real charging station data from 8+ countries
- ✅ Enterprise-grade data storage with Snowflake
- ✅ Advanced analytics and ML capabilities
- ✅ Scalable architecture for growth
- ✅ Comprehensive monitoring and maintenance tools

Your platform is now ready for production use! 🚗⚡ 