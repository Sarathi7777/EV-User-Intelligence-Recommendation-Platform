import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import Plot from 'react-plotly.js';

const HomePage = ({ user }) => {
  const [energyData, setEnergyData] = useState({
    dates: ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
    consumption: [25, 30, 22, 35, 28],
    cost: [5.25, 6.30, 4.62, 7.35, 5.88]
  });
  const [recentSessions, setRecentSessions] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [stats, setStats] = useState({
    totalSessions: 45,
    totalEnergy: 1250,
    averageSession: 28,
    ecoScore: 85
  });

  const wsRef = useRef(null);

  const fetchRecentSessions = async () => {
    try {
      const response = await fetch('http://localhost:8000/sessions');
      if (response.ok) {
        const data = await response.json();
        setRecentSessions(data.slice(0, 5)); // Last 5 sessions
      }
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const fetchRecommendations = async () => {
    try {
      const response = await fetch(`http://localhost:8000/recommendations?user_id=${user.id}`);
      if (response.ok) {
        const data = await response.json();
        setRecommendations(data.recommended_station_ids);
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  
  // Call both fetch functions when component mounts
  useEffect(() => {
    // Fetch user data
    fetchRecentSessions();
    fetchRecommendations();
    // Open realtime websocket for home feed
    try {
      const ws = new WebSocket('ws://localhost:8000/realtime/home');
      wsRef.current = ws;
      ws.onmessage = (evt) => {
        try {
          const payload = JSON.parse(evt.data);
          if (payload.type === 'session_created' && payload.session) {
            setRecentSessions(prev => [payload.session, ...prev].slice(0, 10));
          }
        } catch (e) {
          // ignore malformed
        }
      };
      ws.onopen = () => {
        // optional ping
      };
      ws.onerror = () => {};
    } catch (e) {
      console.error('WS init failed', e);
    }
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return (
    <div style={{ padding: '2rem', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      {/* Welcome Header */}
      <div style={{ 
        backgroundColor: 'white', 
        padding: '2rem', 
        borderRadius: '8px', 
        marginBottom: '2rem',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h1 style={{ color: '#28a745', marginBottom: '0.5rem' }}>
          Welcome back, {user.email}!
        </h1>
        <p style={{ color: '#6c757d', margin: 0 }}>
          Here's your EV charging overview for today
        </p>
      </div>

      {/* Stats Cards */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
        gap: '1.5rem',
        marginBottom: '2rem'
      }}>
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1.5rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', color: '#28a745', marginBottom: '0.5rem' }}>⚡</div>
          <h3 style={{ margin: '0 0 0.5rem 0' }}>{stats.totalSessions}</h3>
          <p style={{ color: '#6c757d', margin: 0 }}>Total Sessions</p>
        </div>
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1.5rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', color: '#007bff', marginBottom: '0.5rem' }}>🔋</div>
          <h3 style={{ margin: '0 0 0.5rem 0' }}>{stats.totalEnergy} kWh</h3>
          <p style={{ color: '#6c757d', margin: 0 }}>Total Energy</p>
        </div>
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1.5rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', color: '#ffc107', marginBottom: '0.5rem' }}>💰</div>
          <h3 style={{ margin: '0 0 0.5rem 0' }}>${(stats.totalEnergy * 0.21).toFixed(2)}</h3>
          <p style={{ color: '#6c757d', margin: 0 }}>Total Spent</p>
        </div>
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1.5rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', color: '#28a745', marginBottom: '0.5rem' }}>🌱</div>
          <h3 style={{ margin: '0 0 0.5rem 0' }}>{stats.ecoScore}%</h3>
          <p style={{ color: '#6c757d', margin: 0 }}>Eco Score</p>
        </div>
      </div>

      {/* Charts Section */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
        gap: '2rem',
        marginBottom: '2rem'
      }}>
        {/* Energy Consumption Chart */}
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1.5rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ marginBottom: '1rem' }}>Energy Consumption</h3>
          <Plot
            data={[
              {
                x: energyData.dates,
                y: energyData.consumption,
                type: 'bar',
                marker: { color: '#28a745' }
              }
            ]}
            layout={{
              title: 'Daily Energy Consumption (kWh)',
              height: 300,
              margin: { t: 40, b: 40, l: 40, r: 40 }
            }}
            config={{ displayModeBar: false }}
          />
        </div>

        {/* Cost Analysis Chart */}
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1.5rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ marginBottom: '1rem' }}>Charging Costs</h3>
          <Plot
            data={[
              {
                x: energyData.dates,
                y: energyData.cost,
                type: 'scatter',
                mode: 'lines+markers',
                marker: { color: '#007bff' }
              }
            ]}
            layout={{
              title: 'Daily Charging Costs ($)',
              height: 300,
              margin: { t: 40, b: 40, l: 40, r: 40 }
            }}
            config={{ displayModeBar: false }}
          />
        </div>
      </div>

      {/* Recent Activity & Recommendations */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
        gap: '2rem'
      }}>
        {/* Recent Sessions */}
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1.5rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ marginBottom: '1rem' }}>Recent Charging Sessions</h3>
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            {recentSessions.map((session, index) => (
              <div key={index} style={{ 
                padding: '1rem', 
                border: '1px solid #e9ecef', 
                borderRadius: '4px', 
                marginBottom: '0.5rem',
                backgroundColor: '#f8f9fa'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <strong>Station {session.station_id}</strong>
                    <div style={{ fontSize: '0.9rem', color: '#6c757d' }}>
                      {new Date(session.timestamp).toLocaleDateString()}
                    </div>
                  </div>
                  <div style={{ color: '#28a745', fontWeight: 'bold' }}>
                    +25 kWh
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Recommendations */}
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1.5rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ marginBottom: '1rem' }}>AI Recommendations</h3>
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            {recommendations.map((stationId, index) => (
              <div key={index} style={{ 
                padding: '1rem', 
                border: '1px solid #e9ecef', 
                borderRadius: '4px', 
                marginBottom: '0.5rem',
                backgroundColor: '#f8f9fa'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <strong>Station {stationId}</strong>
                    <div style={{ fontSize: '0.9rem', color: '#6c757d' }}>
                      Based on your preferences
                    </div>
                  </div>
                  <div style={{ 
                    padding: '0.25rem 0.5rem', 
                    backgroundColor: '#28a745', 
                    color: 'white', 
                    borderRadius: '4px',
                    fontSize: '0.8rem'
                  }}>
                    Recommended
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div style={{ 
        backgroundColor: 'white', 
        padding: '2rem', 
        borderRadius: '8px',
        marginTop: '2rem',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h3 style={{ marginBottom: '1rem' }}>Quick Actions</h3>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '1rem'
        }}>
          <button style={{ 
            padding: '1rem', 
            backgroundColor: '#28a745', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            <Link to="/find-stations" style={{ textDecoration: 'none', color: 'white' }}>
              🗺️ Find Nearby Stations
            </Link>
          </button>
          <button style={{ 
            padding: '1rem', 
            backgroundColor: '#007bff', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            <Link to="/analytics" style={{ textDecoration: 'none', color: 'white' }}>
              📊 View Analytics
            </Link>
          </button>
          <button style={{ 
            padding: '1rem', 
            backgroundColor: '#ffc107', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            <Link to="/start-charging" style={{ textDecoration: 'none', color: 'white' }}>
              ⚡ Start Charging
            </Link>
          </button>
          <button style={{ 
            padding: '1rem', 
            backgroundColor: '#6c757d', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            <Link to="/settings" style={{ textDecoration: 'none', color: 'white' }}>
            ⚙️ Settings
            </Link>
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 