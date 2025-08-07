-- Enhanced Database Schema for EV User Intelligence & Recommendation Platform
-- This schema supports comprehensive station data, user analytics, and ML features

-- =====================================================
-- STATIONS TABLE - Enhanced with OCM data
-- =====================================================
CREATE TABLE IF NOT EXISTS stations (
    id INTEGER PRIMARY KEY,
    ocm_id INTEGER,  -- Open Charge Map ID for reference
    name STRING NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    energy_type STRING,
    available BOOLEAN DEFAULT TRUE,
    
    -- Address information
    address_line1 STRING,
    address_line2 STRING,
    town STRING,
    state STRING,
    country STRING,
    postcode STRING,
    access_comments STRING,
    
    -- Additional OCM data
    operator_info STRING,
    usage_type STRING,
    status_type STRING,
    
    -- Timestamps
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_stations_location ON stations(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_stations_country ON stations(country);
CREATE INDEX IF NOT EXISTS idx_stations_energy_type ON stations(energy_type);
CREATE INDEX IF NOT EXISTS idx_stations_ocm_id ON stations(ocm_id);

-- =====================================================
-- USERS TABLE - Enhanced user management
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    email STRING UNIQUE NOT NULL,
    password_hash STRING NOT NULL,
    
    -- User profile
    first_name STRING,
    last_name STRING,
    phone STRING,
    
    -- Analytics
    eco_score FLOAT DEFAULT 0.0,
    total_charging_sessions INTEGER DEFAULT 0,
    total_energy_consumed_kwh FLOAT DEFAULT 0.0,
    total_cost FLOAT DEFAULT 0.0,
    
    -- Preferences
    preferred_energy_type STRING,
    max_travel_distance_km FLOAT DEFAULT 10.0,
    
    -- Timestamps
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    last_login_at TIMESTAMP_NTZ
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_eco_score ON users(eco_score);

-- =====================================================
-- SESSIONS TABLE - Enhanced charging sessions
-- =====================================================
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    station_id INTEGER NOT NULL,
    
    -- Session details
    start_time TIMESTAMP_NTZ NOT NULL,
    end_time TIMESTAMP_NTZ,
    duration_minutes INTEGER,
    energy_consumed_kwh FLOAT,
    cost FLOAT,
    
    -- Session status
    status STRING DEFAULT 'active', -- active, completed, cancelled, failed
    
    -- Additional data
    initial_battery_percentage FLOAT,
    final_battery_percentage FLOAT,
    charging_rate_kw FLOAT,
    
    -- Timestamps
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    
    -- Foreign keys
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (station_id) REFERENCES stations(id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_station_id ON sessions(station_id);
CREATE INDEX IF NOT EXISTS idx_sessions_start_time ON sessions(start_time);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);

-- =====================================================
-- STATION_USAGE TABLE - Analytics and forecasting
-- =====================================================
CREATE TABLE IF NOT EXISTS station_usage (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    station_id INTEGER NOT NULL,
    usage_date DATE NOT NULL,
    hour_of_day INTEGER, -- 0-23
    
    -- Usage metrics
    total_sessions INTEGER DEFAULT 0,
    total_energy_kwh FLOAT DEFAULT 0.0,
    avg_session_duration_minutes FLOAT DEFAULT 0.0,
    peak_usage_minutes INTEGER DEFAULT 0,
    
    -- Revenue metrics
    total_revenue FLOAT DEFAULT 0.0,
    avg_session_cost FLOAT DEFAULT 0.0,
    
    -- Availability metrics
    total_downtime_minutes INTEGER DEFAULT 0,
    availability_percentage FLOAT DEFAULT 100.0,
    
    -- Timestamps
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    
    -- Foreign key
    FOREIGN KEY (station_id) REFERENCES stations(id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_station_usage_station_date ON station_usage(station_id, usage_date);
CREATE INDEX IF NOT EXISTS idx_station_usage_hour ON station_usage(hour_of_day);

-- =====================================================
-- USER_PREFERENCES TABLE - ML and personalization
-- =====================================================
CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    
    -- Charging preferences
    preferred_charging_time_start INTEGER, -- Hour of day (0-23)
    preferred_charging_time_end INTEGER,   -- Hour of day (0-23)
    preferred_weekdays STRING, -- Comma-separated days (1-7)
    
    -- Location preferences
    home_latitude FLOAT,
    home_longitude FLOAT,
    work_latitude FLOAT,
    work_longitude FLOAT,
    
    -- Vehicle preferences
    vehicle_model STRING,
    battery_capacity_kwh FLOAT,
    max_charging_rate_kw FLOAT,
    
    -- ML features
    user_cluster INTEGER, -- K-means cluster assignment
    recommendation_score FLOAT DEFAULT 0.0,
    
    -- Timestamps
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    
    -- Foreign key
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_user_preferences_cluster ON user_preferences(user_cluster);

-- =====================================================
-- RECOMMENDATIONS TABLE - ML recommendations
-- =====================================================
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    station_id INTEGER NOT NULL,
    
    -- Recommendation details
    recommendation_score FLOAT NOT NULL,
    recommendation_type STRING, -- 'collaborative', 'content_based', 'hybrid'
    reason STRING, -- Why this station was recommended
    
    -- Usage tracking
    is_clicked BOOLEAN DEFAULT FALSE,
    is_used BOOLEAN DEFAULT FALSE,
    clicked_at TIMESTAMP_NTZ,
    used_at TIMESTAMP_NTZ,
    
    -- Timestamps
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    expires_at TIMESTAMP_NTZ, -- When recommendation expires
    
    -- Foreign keys
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (station_id) REFERENCES stations(id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_recommendations_user_id ON recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_score ON recommendations(recommendation_score);
CREATE INDEX IF NOT EXISTS idx_recommendations_expires ON recommendations(expires_at);

-- =====================================================
-- FORECASTS TABLE - Energy demand predictions
-- =====================================================
CREATE TABLE IF NOT EXISTS forecasts (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    station_id INTEGER,
    forecast_date DATE NOT NULL,
    hour_of_day INTEGER, -- 0-23
    
    -- Forecast metrics
    predicted_demand_kwh FLOAT,
    predicted_sessions INTEGER,
    confidence_interval_lower FLOAT,
    confidence_interval_upper FLOAT,
    
    -- Model information
    model_type STRING, -- 'time_series', 'ml', 'ensemble'
    model_version STRING,
    
    -- Timestamps
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    forecast_generated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    
    -- Foreign key
    FOREIGN KEY (station_id) REFERENCES stations(id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_forecasts_station_date ON forecasts(station_id, forecast_date);
CREATE INDEX IF NOT EXISTS idx_forecasts_model_type ON forecasts(model_type);

-- =====================================================
-- AUDIT_LOG TABLE - System monitoring
-- =====================================================
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    
    -- Event details
    event_type STRING NOT NULL, -- 'user_login', 'session_start', 'recommendation_generated', etc.
    user_id INTEGER,
    station_id INTEGER,
    
    -- Event data
    event_data STRING, -- JSON string with additional event details
    ip_address STRING,
    user_agent STRING,
    
    -- Timestamps
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_audit_log_event_type ON audit_log(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_log(created_at);

-- =====================================================
-- VIEWS FOR ANALYTICS
-- =====================================================

-- Station usage summary view
CREATE OR REPLACE VIEW station_usage_summary AS
SELECT 
    s.id,
    s.name,
    s.latitude,
    s.longitude,
    s.energy_type,
    s.country,
    s.state,
    COUNT(su.id) as total_usage_records,
    SUM(su.total_sessions) as total_sessions,
    SUM(su.total_energy_kwh) as total_energy_kwh,
    AVG(su.avg_session_duration_minutes) as avg_session_duration,
    SUM(su.total_revenue) as total_revenue
FROM stations s
LEFT JOIN station_usage su ON s.id = su.station_id
GROUP BY s.id, s.name, s.latitude, s.longitude, s.energy_type, s.country, s.state;

-- User activity summary view
CREATE OR REPLACE VIEW user_activity_summary AS
SELECT 
    u.id,
    u.email,
    u.eco_score,
    COUNT(s.id) as total_sessions,
    SUM(s.energy_consumed_kwh) as total_energy_consumed,
    SUM(s.cost) as total_cost,
    AVG(s.duration_minutes) as avg_session_duration,
    MAX(s.start_time) as last_session_date
FROM users u
LEFT JOIN sessions s ON u.id = s.user_id
GROUP BY u.id, u.email, u.eco_score;

-- =====================================================
-- USER LOCATIONS TABLE - For real-time user sharing
-- =====================================================
CREATE TABLE IF NOT EXISTS user_locations (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    last_updated TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    status STRING DEFAULT 'active', -- active, hidden, offline
    message STRING, -- Optional help/status message
    contact_method STRING, -- phone/email/in-app
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_user_locations_user_id ON user_locations(user_id);
CREATE INDEX IF NOT EXISTS idx_user_locations_location ON user_locations(latitude, longitude);

-- =====================================================
-- EV STORES TABLE - For nearby EV stores
-- =====================================================
CREATE TABLE IF NOT EXISTS ev_stores (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    name STRING NOT NULL,
    store_type STRING, -- dealership, service, parts, etc.
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    address STRING,
    contact STRING,
    hours STRING,
    services STRING, -- comma-separated list
    website STRING,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
CREATE INDEX IF NOT EXISTS idx_ev_stores_location ON ev_stores(latitude, longitude);

-- =====================================================
-- FLOATING SERVICES TABLE - For mobile/roadside help
-- =====================================================
CREATE TABLE IF NOT EXISTS floating_services (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    name STRING NOT NULL,
    service_type STRING, -- roadside, mobile charging, towing, etc.
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    contact STRING,
    hours STRING,
    description STRING,
    website STRING,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
CREATE INDEX IF NOT EXISTS idx_floating_services_location ON floating_services(latitude, longitude);

-- =====================================================
-- SAMPLE DATA INSERTS (for testing)
-- =====================================================

-- Insert sample stations
INSERT INTO stations (id, name, latitude, longitude, energy_type, country, state, town) VALUES
(1, 'Downtown Charging Station', 10.877185, 77.005055, 'Level 2', 'India', 'Coimbatore', 'Othakalmandapam'),
(2, 'Mall Parking Garage', 10.902898, 76.998908, 'DC Fast', 'India', 'Coimbatore', 'malumichampatti'),
(3, 'Hindustan', 10.893707, 76.995006, 'Level 2', 'India', 'Coimbatore', 'Coimbatore International Airport'),
(4, 'Shopping Center', 10.877185, 77.005055, 'Level 1', 'India', 'Coimbatore', 'Othakalmandapam'),
(5, 'Office Building', 10.877185, 77.005055, 'DC Fast', 'India', 'Coimbatore', 'Othakalmandapam');

-- Insert sample users
INSERT INTO users (id, email, password_hash, eco_score, first_name, last_name) VALUES
(1, 'user1@example.com', 'hashed_password_1', 85.5, 'John', 'Doe'),
(2, 'user2@example.com', 'hashed_password_2', 72.3, 'Jane', 'Smith'),
(3, 'admin@example.com', 'hashed_password_3', 90.0, 'Admin', 'User');

-- Insert sample sessions
INSERT INTO sessions (user_id, station_id, start_time, end_time, duration_minutes, energy_consumed_kwh, cost, status) VALUES
(1, 1, '2024-01-15 10:00:00', '2024-01-15 11:30:00', 90, 25.5, 12.75, 'completed'),
(2, 2, '2024-01-15 14:00:00', '2024-01-15 14:45:00', 45, 35.0, 17.50, 'completed'),
(1, 3, '2024-01-16 09:00:00', '2024-01-16 10:15:00', 75, 20.0, 10.00, 'completed');

-- =====================================================
-- COMMENTS
-- =====================================================
/*
This enhanced schema provides:

1. **Comprehensive Station Data**: Full OCM integration with address details
2. **User Analytics**: Track eco-scores, preferences, and behavior patterns
3. **Session Management**: Detailed charging session tracking
4. **Usage Analytics**: Station performance and demand forecasting
5. **ML Features**: User clustering and recommendation storage
6. **Audit Trail**: System monitoring and debugging
7. **Performance**: Optimized indexes for fast queries
8. **Scalability**: Designed for large-scale EV User Intelligence

To use this schema:
1. Run this SQL in your Snowflake instance
2. Update your .env file with Snowflake credentials
3. Run the OCM data ingestion script
4. The platform will automatically use this enhanced data structure
*/

-- =====================================================
-- SAMPLE DATA FOR DEVELOPMENT (COIMBATORE REGION)
-- =====================================================
-- Sample user locations (Coimbatore)
INSERT INTO user_locations (user_id, latitude, longitude, status, message, contact_method) VALUES
(1, 10.877185, 77.005055, 'active', 'Need help, battery low near Gandhipuram!', 'email:user1@example.com'),
(2, 10.902898, 76.998908, 'active', NULL, 'phone:+919876543210'),
(3, 10.877185, 77.005055, 'active', 'Can assist near RS Puram!', 'in-app');

-- Sample EV stores (Coimbatore)
INSERT INTO ev_stores (name, store_type, latitude, longitude, address, contact, hours, services, website) VALUES
('Ampere EV Showroom', 'dealership', 11.0186, 76.9725, '100, Avinashi Road, Peelamedu, Coimbatore', '+91-422-1234567', '9am-7pm', 'sales,service,parts', 'https://amperevehicles.com'),
('Ather Space Coimbatore', 'dealership', 11.0168, 76.9552, '50, DB Road, RS Puram, Coimbatore', '+91-422-7654321', '10am-8pm', 'sales,service', 'https://atherenergy.com'),
('EV Service Hub', 'service', 11.0250, 76.9500, '200, Trichy Road, Singanallur, Coimbatore', '+91-422-2468101', '8am-6pm', 'service,charging', NULL);

-- Sample floating services (Coimbatore)
INSERT INTO floating_services (name, service_type, latitude, longitude, contact, hours, description, website) VALUES
('Coimbatore EV Rescue', 'mobile charging', 11.0120, 76.9800, '+91-9000000001', '24/7', 'On-demand mobile charging for stranded EVs in Coimbatore', NULL),
('Green Roadside Assist', 'roadside', 11.0300, 76.9500, '+91-9000000002', '24/7', 'Roadside help for flat tires, towing, and more', NULL);