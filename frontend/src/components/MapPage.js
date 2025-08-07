import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const MapPage = ({ user }) => {
  const [stations, setStations] = useState([]);
  const [nearbyStations, setNearbyStations] = useState([]);
  const [users, setUsers] = useState([]);
  const [filters, setFilters] = useState({
    energyType: 'all',
    availability: 'all',
    distance: 10,
    showUsers: true,
    showNearby: true
  });
  const [selectedStation, setSelectedStation] = useState(null);
  const [userLocation, setUserLocation] = useState([10.877185, 77.005055]);
  const [isLoadingNearby, setIsLoadingNearby] = useState(false);


  useEffect(() => {
    fetchStations();
    fetchUsers();
    getUserLocation();
  }, []);

  useEffect(() => {
    if (userLocation[0] !== 10.877185 || userLocation[1] !== 77.005055) {
      fetchNearbyStations();
    }
  }, [userLocation, filters.distance]);

  const fetchStations = async () => {
    try {
      const response = await fetch('http://localhost:8000/stations');
      if (response.ok) {
        const data = await response.json();
        setStations(data);
      }
    } catch (error) {
      console.error('Error fetching stations:', error);
    }
  };

  const fetchNearbyStations = async () => {
    setIsLoadingNearby(true);
    try {
      const response = await fetch(
        `http://localhost:8000/stations/nearby?lat=${userLocation[0]}&lon=${userLocation[1]}&radius=${filters.distance}&use_ocm=true`
      );
      if (response.ok) {
        const data = await response.json();
        setNearbyStations(data);
      }
    } catch (error) {
      console.error('Error fetching nearby stations:', error);
    } finally {
      setIsLoadingNearby(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://localhost:8000/admin/users');
      if (response.ok) {
        const data = await response.json();
        // Mock user locations around the map
        const mockUsers = data.map((user, index) => ({
          ...user,
          location: [
            10.877185 + (Math.random() - 0.5) * 0.1,
            77.005055 + (Math.random() - 0.5) * 0.1
          ]
        }));
        setUsers(mockUsers);
      }
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const getUserLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation([position.coords.latitude, position.coords.longitude]);
        },
        (error) => {
          console.log('Error getting location:', error);
        }
      );
    }
  };

  const getFilteredStations = () => {
    return stations.filter(station => {
      if (filters.energyType !== 'all' && station.energy_type !== filters.energyType) {
        return false;
      }
      if (filters.availability !== 'all') {
        const isAvailable = filters.availability === 'available' ? true : false;
        if (station.available !== isAvailable) {
          return false;
        }
      }
      return true;
    });
  };

  const getFilteredNearbyStations = () => {
    return nearbyStations.filter(station => {
      if (filters.energyType !== 'all' && station.energy_type !== filters.energyType) {
        return false;
      }
      if (filters.availability !== 'all') {
        const isAvailable = filters.availability === 'available' ? true : false;
        if (station.available !== isAvailable) {
          return false;
        }
      }
      return true;
    });
  };

  const getStationIcon = (station) => {
    const color = station.available ? '#28a745' : '#dc3545';
    const size = station.energy_type === 'DC Fast' ? 12 : 8;
    
    return L.divIcon({
      html: `<div style="
        width: ${size}px; 
        height: ${size}px; 
        background-color: ${color}; 
        border: 2px solid white; 
        border-radius: 50%; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
      "></div>`,
      className: 'custom-marker',
      iconSize: [size, size],
      iconAnchor: [size/2, size/2]
    });
  };

  const getNearbyStationIcon = (station) => {
    const color = station.source === 'ocm' ? '#007bff' : (station.available ? '#28a745' : '#dc3545');
    const size = station.energy_type.includes('DC') ? 12 : 8;
    
    return L.divIcon({
      html: `<div style="
        width: ${size}px; 
        height: ${size}px; 
        background-color: ${color}; 
        border: 2px solid white; 
        border-radius: 50%; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        ${station.source === 'ocm' ? 'border: 2px solid #0056b3;' : ''}
      "></div>`,
      className: 'custom-marker',
      iconSize: [size, size],
      iconAnchor: [size/2, size/2]
    });
  };

  const handleStationClick = (station) => {
    setSelectedStation(station);
  };

  const startCharging = async (stationId) => {
    try {
      const session = {
        user_id: user.id,
        station_id: stationId,
        timestamp: new Date().toISOString()
      };
      
      const response = await fetch('http://localhost:8000/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(session)
      });
      
      if (response.ok) {
        alert('Charging session started!');
        setSelectedStation(null);
      }
    } catch (error) {
      console.error('Error starting charging session:', error);
    }
  };

  const formatTime = (minutes) => {
    if (minutes < 60) {
      return `${minutes} min`;
    } else {
      const hours = Math.floor(minutes / 60);
      const mins = minutes % 60;
      return `${hours}h ${mins}min`;
    }
  };

  return (
    <>
      <ToastContainer position="top-right" autoClose={3000} />
      <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1rem 2rem', 
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <h1 style={{ margin: 0, color: '#28a745' }}>Charging Station Map</h1>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <select 
              value={filters.energyType}
              onChange={(e) => setFilters({...filters, energyType: e.target.value})}
              style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
            >
              <option value="all">All Energy Types</option>
              <option value="Level 1">Level 1</option>
              <option value="Level 2">Level 2</option>
              <option value="DC Fast">DC Fast</option>
            </select>
            <select 
              value={filters.availability}
              onChange={(e) => setFilters({...filters, availability: e.target.value})}
              style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
            >
              <option value="all">All Stations</option>
              <option value="available">Available Only</option>
              <option value="occupied">Occupied Only</option>
            </select>
            <select 
              value={filters.distance}
              onChange={(e) => setFilters({...filters, distance: parseFloat(e.target.value)})}
              style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
            >
              <option value={5}>5 km</option>
              <option value={10}>10 km</option>
              <option value={20}>20 km</option>
              <option value={50}>50 km</option>
            </select>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <input 
                type="checkbox" 
                checked={filters.showUsers}
                onChange={(e) => setFilters({...filters, showUsers: e.target.checked})}
              />
              Show Users
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <input 
                type="checkbox" 
                checked={filters.showNearby}
                onChange={(e) => setFilters({...filters, showNearby: e.target.checked})}
              />
              Show Nearby
            </label>
          </div>
        </div>

        {/* Map Container */}
        <div style={{ flex: 1, position: 'relative' }}>
          <MapContainer 
            center={userLocation} 
            zoom={13} 
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              attribution='&copy; OpenStreetMap contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            
            {/* User Location */}
            <CircleMarker 
              center={userLocation} 
              radius={8} 
              pathOptions={{ color: '#007bff', fillColor: '#007bff', fillOpacity: 0.7 }}
            >
              <Popup>
                <div>
                  <strong>Your Location</strong><br />
                  <small>You are here</small>
                </div>
              </Popup>
            </CircleMarker>

            {/* Regular Charging Stations */}
            {getFilteredStations()
              .filter(station => station.latitude !== undefined && station.longitude !== undefined)
              .map((station) => (
                <Marker 
                  key={station.id} 
                  position={[station.latitude, station.longitude]}
                  icon={getStationIcon(station)}
                  eventHandlers={{
                    click: () => handleStationClick(station)
                  }}
                >
                  <Popup>
                    <div style={{ minWidth: '200px' }}>
                      <h3 style={{ margin: '0 0 0.5rem 0', color: '#28a745' }}>
                        {station.name}
                      </h3>
                      <p style={{ margin: '0 0 0.5rem 0' }}>
                        <strong>Type:</strong> {station.energy_type}
                      </p>
                      <p style={{ margin: '0 0 0.5rem 0' }}>
                        <strong>Status:</strong> 
                        <span style={{ 
                          color: station.available ? '#28a745' : '#dc3545',
                          fontWeight: 'bold'
                        }}>
                          {station.available ? ' Available' : ' Occupied'}
                        </span>
                      </p>
                      <button 
                        onClick={() => startCharging(station.id)}
                        disabled={!station.available}
                        style={{ 
                          padding: '0.5rem 1rem', 
                          backgroundColor: station.available ? '#28a745' : '#6c757d',
                          color: 'white', 
                          border: 'none', 
                          borderRadius: '4px',
                          cursor: station.available ? 'pointer' : 'not-allowed',
                          width: '100%'
                        }}
                      >
                        {station.available ? 'Start Charging' : 'Currently Occupied'}
                      </button>
                    </div>
                  </Popup>
                </Marker>
              ))}

            {/* Nearby Stations */}
            {filters.showNearby && getFilteredNearbyStations()
              .filter(station => station.latitude !== undefined && station.longitude !== undefined)
              .map((station) => (
                <Marker 
                  key={station.id} 
                  position={[station.latitude, station.longitude]}
                  icon={getNearbyStationIcon(station)}
                  eventHandlers={{
                    click: () => handleStationClick(station)
                  }}
                >
                  <Popup>
                    <div style={{ minWidth: '250px' }}>
                      <h3 style={{ margin: '0 0 0.5rem 0', color: '#007bff' }}>
                        {station.name}
                      </h3>
                      <p style={{ margin: '0 0 0.5rem 0' }}>
                        <strong>Type:</strong> {station.energy_type}
                      </p>
                      <p style={{ margin: '0 0 0.5rem 0' }}>
                        <strong>Distance:</strong> {station.distance_km} km
                      </p>
                      <p style={{ margin: '0 0 0.5rem 0' }}>
                        <strong>Travel Time:</strong> {formatTime(station.travel_time_minutes)}
                      </p>
                      <p style={{ margin: '0 0 0.5rem 0' }}>
                        <strong>Source:</strong> 
                        <span style={{ 
                          color: station.source === 'ocm' ? '#007bff' : '#28a745',
                          fontWeight: 'bold'
                        }}>
                          {station.source === 'ocm' ? ' Open Charge Map' : ' Local Database'}
                        </span>
                      </p>
                      <p style={{ margin: '0 0 0.5rem 0' }}>
                        <strong>Status:</strong> 
                        <span style={{ 
                          color: station.available ? '#28a745' : '#dc3545',
                          fontWeight: 'bold'
                        }}>
                          {station.available ? ' Available' : ' Occupied'}
                        </span>
                      </p>
                      <button 
                        onClick={() => startCharging(station.id)}
                        disabled={!station.available}
                        style={{ 
                          padding: '0.5rem 1rem', 
                          backgroundColor: station.available ? '#28a745' : '#6c757d',
                          color: 'white', 
                          border: 'none', 
                          borderRadius: '4px',
                          cursor: station.available ? 'pointer' : 'not-allowed',
                          width: '100%'
                        }}
                      >
                        {station.available ? 'Start Charging' : 'Currently Occupied'}
                      </button>
                    </div>
                  </Popup>
                </Marker>
              ))}

            {/* Other Users */}
            {filters.showUsers && users.map((otherUser) => (
              <CircleMarker 
                key={otherUser.id} 
                center={otherUser.location} 
                radius={6} 
                pathOptions={{ color: '#ffc107', fillColor: '#ffc107', fillOpacity: 0.7 }}
              >
                <Popup>
                  <div>
                    <strong>{otherUser.email}</strong><br />
                    <small>Eco Score: {otherUser.eco_score}%</small>
                  </div>
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>

          {/* Nearby Stations Panel */}
          {filters.showNearby && (
            <div style={{ 
              position: 'absolute', 
              top: '20px', 
              left: '20px', 
              backgroundColor: 'white', 
              padding: '1.5rem', 
              borderRadius: '8px',
              boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
              maxWidth: '350px',
              maxHeight: '70vh',
              overflowY: 'auto',
              zIndex: 1000
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h3 style={{ margin: 0, color: '#007bff' }}>Nearby Stations</h3>
                <button 
                  onClick={() => setFilters({...filters, showNearby: false})}
                  style={{ 
                    background: 'none', 
                    border: 'none', 
                    fontSize: '1.5rem', 
                    cursor: 'pointer',
                    color: '#6c757d'
                  }}
                >
                  ×
                </button>
              </div>
              
              {isLoadingNearby ? (
                <div style={{ textAlign: 'center', padding: '2rem' }}>
                  <div>🔍 Searching nearby stations...</div>
                </div>
              ) : getFilteredNearbyStations().length === 0 ? (
                <div style={{ textAlign: 'center', padding: '2rem', color: '#6c757d' }}>
                  <div>📍 No stations found within {filters.distance}km</div>
                  <div style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
                    Try increasing the search radius
                  </div>
                </div>
              ) : (
                <div>
                  {getFilteredNearbyStations().slice(0, 10).map((station) => (
                    <div 
                      key={station.id}
                      style={{
                        padding: '1rem',
                        border: '1px solid #e9ecef',
                        borderRadius: '8px',
                        marginBottom: '0.5rem',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease',
                        backgroundColor: selectedStation?.id === station.id ? '#f8f9fa' : 'white'
                      }}
                      onClick={() => handleStationClick(station)}
                      onMouseEnter={(e) => {
                        e.target.style.backgroundColor = '#f8f9fa';
                      }}
                      onMouseLeave={(e) => {
                        if (selectedStation?.id !== station.id) {
                          e.target.style.backgroundColor = 'white';
                        }
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                        <div style={{ flex: 1 }}>
                          <h4 style={{ margin: '0 0 0.5rem 0', fontSize: '1rem', color: '#212529' }}>
                            {station.name}
                          </h4>
                          <p style={{ margin: '0 0 0.25rem 0', fontSize: '0.9rem', color: '#6c757d' }}>
                            {station.energy_type}
                          </p>
                          <div style={{ display: 'flex', gap: '1rem', fontSize: '0.8rem', color: '#495057' }}>
                            <span>📍 {station.distance_km} km</span>
                            <span>⏱️ {formatTime(station.travel_time_minutes)}</span>
                          </div>
                        </div>
                        <div style={{ 
                          width: '12px', 
                          height: '12px', 
                          backgroundColor: station.source === 'ocm' ? '#007bff' : (station.available ? '#28a745' : '#dc3545'),
                          borderRadius: '50%',
                          border: station.source === 'ocm' ? '2px solid #0056b3' : '2px solid white'
                        }}></div>
                      </div>
                    </div>
                  ))}
                  {getFilteredNearbyStations().length > 10 && (
                    <div style={{ textAlign: 'center', padding: '1rem', color: '#6c757d', fontSize: '0.9rem' }}>
                      Showing 10 of {getFilteredNearbyStations().length} stations
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Station Details Panel */}
          {selectedStation && (
            <div style={{ 
              position: 'absolute', 
              top: '20px', 
              right: '20px', 
              backgroundColor: 'white', 
              padding: '1.5rem', 
              borderRadius: '8px',
              boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
              maxWidth: '300px',
              zIndex: 1000
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h3 style={{ margin: 0, color: selectedStation.source === 'ocm' ? '#007bff' : '#28a745' }}>Station Details</h3>
                <button 
                  onClick={() => setSelectedStation(null)}
                  style={{ 
                    background: 'none', 
                    border: 'none', 
                    fontSize: '1.5rem', 
                    cursor: 'pointer',
                    color: '#6c757d'
                  }}
                >
                  ×
                </button>
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <strong>Name:</strong> {selectedStation.name}
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <strong>Type:</strong> {selectedStation.energy_type}
              </div>
              {selectedStation.distance_km && (
                <div style={{ marginBottom: '1rem' }}>
                  <strong>Distance:</strong> {selectedStation.distance_km} km
                </div>
              )}
              {selectedStation.travel_time_minutes && (
                <div style={{ marginBottom: '1rem' }}>
                  <strong>Travel Time:</strong> {formatTime(selectedStation.travel_time_minutes)}
                </div>
              )}
              {selectedStation.source && (
                <div style={{ marginBottom: '1rem' }}>
                  <strong>Source:</strong> 
                  <span style={{ 
                    color: selectedStation.source === 'ocm' ? '#007bff' : '#28a745',
                    fontWeight: 'bold'
                  }}>
                    {selectedStation.source === 'ocm' ? ' Open Charge Map' : ' Local Database'}
                  </span>
                </div>
              )}
              <div style={{ marginBottom: '1rem' }}>
                <strong>Status:</strong> 
                <span style={{ 
                  color: selectedStation.available ? '#28a745' : '#dc3545',
                  fontWeight: 'bold'
                }}>
                  {selectedStation.available ? ' Available' : ' Occupied'}
                </span>
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <strong>Location:</strong><br />
                {selectedStation.latitude.toFixed(4)}, {selectedStation.longitude.toFixed(4)}
              </div>
              {selectedStation.available && (
                <button 
                  onClick={() => startCharging(selectedStation.id)}
                  style={{ 
                    padding: '0.75rem 1.5rem', 
                    backgroundColor: '#28a745', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '4px',
                    cursor: 'pointer',
                    width: '100%'
                  }}
                >
                  Start Charging Session
                </button>
              )}
            </div>
          )}

          {/* Map Legend */}
          <div style={{ 
            position: 'absolute', 
            bottom: '20px', 
            left: '20px', 
            backgroundColor: 'white', 
            padding: '1rem', 
            borderRadius: '8px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            zIndex: 1000
          }}>
            <h4 style={{ margin: '0 0 0.5rem 0' }}>Legend</h4>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
              <div style={{ 
                width: '12px', 
                height: '12px', 
                backgroundColor: '#28a745', 
                borderRadius: '50%', 
                marginRight: '0.5rem' 
              }}></div>
              <span>Available Station</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
              <div style={{ 
                width: '12px', 
                height: '12px', 
                backgroundColor: '#dc3545', 
                borderRadius: '50%', 
                marginRight: '0.5rem' 
              }}></div>
              <span>Occupied Station</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
              <div style={{ 
                width: '12px', 
                height: '12px', 
                backgroundColor: '#007bff', 
                borderRadius: '50%', 
                border: '2px solid #0056b3',
                marginRight: '0.5rem' 
              }}></div>
              <span>OCM Station</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
              <div style={{ 
                width: '8px', 
                height: '8px', 
                backgroundColor: '#007bff', 
                borderRadius: '50%', 
                marginRight: '0.5rem' 
              }}></div>
              <span>Your Location</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <div style={{ 
                width: '6px', 
                height: '6px', 
                backgroundColor: '#ffc107', 
                borderRadius: '50%', 
                marginRight: '0.5rem' 
              }}></div>
              <span>Other Users</span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default MapPage; 