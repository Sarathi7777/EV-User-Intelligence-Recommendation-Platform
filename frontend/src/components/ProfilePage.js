import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

const ProfilePage = ({ user }) => {
  const [profile, setProfile] = useState({
    firstName: 'John',
    lastName: 'Doe',
    email: user.email,
    phone: '+1 (555) 123-4567',
    address: '123 EV Street, San Francisco, CA 94102',
    memberSince: '2023-01-15',
    totalSessions: 45,
    totalEnergy: 1250,
    averageSession: 28,
    ecoScore: 85,
    carbonSaved: 450,
    favoriteStations: [1, 3, 5]
  });

  const [vehicles, setVehicles] = useState([
    {
      id: 1,
      make: 'Tesla',
      model: 'Model 3',
      year: 2022,
      batteryCapacity: 75,
      currentCharge: 65,
      licensePlate: 'EV-1234'
    },
    {
      id: 2,
      make: 'Nissan',
      model: 'Leaf',
      year: 2021,
      batteryCapacity: 62,
      currentCharge: 45,
      licensePlate: 'LEAF-567'
    }
  ]);

  const [chargingHistory, setChargingHistory] = useState([
    {
      id: 1,
      station: 'Downtown Charging Station',
      date: '2024-01-15',
      duration: '45 min',
      energy: '25 kWh',
      cost: '$5.25'
    },
    {
      id: 2,
      station: 'Mall Parking Garage',
      date: '2024-01-14',
      duration: '30 min',
      energy: '18 kWh',
      cost: '$3.78'
    },
    {
      id: 3,
      station: 'Airport Terminal A',
      date: '2024-01-13',
      duration: '60 min',
      energy: '35 kWh',
      cost: '$7.35'
    }
  ]);

  const [achievements, setAchievements] = useState([
    { id: 1, name: 'First Charge', description: 'Completed your first charging session', earned: '2023-01-15', icon: '⚡' },
    { id: 2, name: 'Eco Warrior', description: 'Saved 100kg of CO2', earned: '2023-03-20', icon: '🌱' },
    { id: 3, name: 'Regular Charger', description: 'Completed 10 charging sessions', earned: '2023-05-10', icon: '🔋' },
    { id: 4, name: 'Green Champion', description: 'Achieved 80% eco score', earned: '2023-07-15', icon: '🏆' }
  ]);

  return (
    <div style={{ padding: '2rem', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      {/* Profile Header */}
      <div style={{ 
        backgroundColor: 'white', 
        padding: '2rem', 
        borderRadius: '8px', 
        marginBottom: '2rem',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        display: 'flex',
        alignItems: 'center',
        gap: '2rem'
      }}>
        <div style={{ 
          width: '100px', 
          height: '100px', 
          backgroundColor: '#28a745', 
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '3rem',
          color: 'white'
        }}>
          {profile.firstName[0]}{profile.lastName[0]}
        </div>
        <div>
          <h1 style={{ margin: '0 0 0.5rem 0', color: '#28a745' }}>
            {profile.firstName} {profile.lastName}
          </h1>
          <p style={{ margin: '0 0 0.5rem 0', color: '#6c757d' }}>
            {profile.email}
          </p>
          <p style={{ margin: 0, color: '#6c757d' }}>
            Member since {new Date(profile.memberSince).toLocaleDateString()}
          </p>
        </div>
        <div style={{ marginLeft: 'auto', textAlign: 'right' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#28a745' }}>
            {profile.ecoScore}%
          </div>
          <div style={{ color: '#6c757d' }}>Eco Score</div>
        </div>
      </div>

      {/* Stats Grid */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
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
          <h3 style={{ margin: '0 0 0.5rem 0' }}>{profile.totalSessions}</h3>
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
          <h3 style={{ margin: '0 0 0.5rem 0' }}>{profile.totalEnergy} kWh</h3>
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
          <h3 style={{ margin: '0 0 0.5rem 0' }}>${(profile.totalEnergy * 0.21).toFixed(2)}</h3>
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
          <h3 style={{ margin: '0 0 0.5rem 0' }}>{profile.carbonSaved} kg</h3>
          <p style={{ color: '#6c757d', margin: 0 }}>CO2 Saved</p>
        </div>
      </div>

      {/* Main Content Grid */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
        gap: '2rem'
      }}>
        {/* Personal Information */}
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1.5rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ marginBottom: '1rem' }}>Personal Information</h3>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              First Name
            </label>
            <input 
              type="text" 
              value={profile.firstName}
              style={{ 
                width: '100%', 
                padding: '0.5rem', 
                border: '1px solid #ddd', 
                borderRadius: '4px' 
              }}
            />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              Last Name
            </label>
            <input 
              type="text" 
              value={profile.lastName}
              style={{ 
                width: '100%', 
                padding: '0.5rem', 
                border: '1px solid #ddd', 
                borderRadius: '4px' 
              }}
            />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              Phone
            </label>
            <input 
              type="tel" 
              value={profile.phone}
              style={{ 
                width: '100%', 
                padding: '0.5rem', 
                border: '1px solid #ddd', 
                borderRadius: '4px' 
              }}
            />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              Address
            </label>
            <textarea 
              value={profile.address}
              rows="3"
              style={{ 
                width: '100%', 
                padding: '0.5rem', 
                border: '1px solid #ddd', 
                borderRadius: '4px' 
              }}
            />
          </div>
          <button style={{ 
            padding: '0.75rem 1.5rem', 
            backgroundColor: '#28a745', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            Save Changes
          </button>
        </div>

        {/* Vehicles */}
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1.5rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ marginBottom: '1rem' }}>My Vehicles</h3>
          {vehicles.map((vehicle, index) => (
            <div key={index} style={{ 
              border: '1px solid #e9ecef', 
              borderRadius: '4px', 
              padding: '1rem', 
              marginBottom: '1rem',
              backgroundColor: '#f8f9fa'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <strong>{vehicle.make} {vehicle.model} ({vehicle.year})</strong>
                <span style={{ 
                  padding: '0.25rem 0.5rem', 
                  backgroundColor: '#28a745', 
                  color: 'white', 
                  borderRadius: '4px',
                  fontSize: '0.8rem'
                }}>
                  {vehicle.licensePlate}
                </span>
              </div>
              <div style={{ fontSize: '0.9rem', color: '#6c757d' }}>
                Battery: {vehicle.currentCharge}% / {vehicle.batteryCapacity} kWh
              </div>
              <div style={{ 
                width: '100%', 
                height: '8px', 
                backgroundColor: '#e9ecef', 
                borderRadius: '4px', 
                marginTop: '0.5rem'
              }}>
                <div style={{ 
                  width: `${(vehicle.currentCharge / vehicle.batteryCapacity) * 100}%`, 
                  height: '100%', 
                  backgroundColor: '#28a745', 
                  borderRadius: '4px' 
                }} />
              </div>
            </div>
          ))}
          <button style={{ 
            padding: '0.75rem 1.5rem', 
            backgroundColor: '#007bff', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            + Add Vehicle
          </button>
        </div>
      </div>

      {/* Charging History */}
      <div style={{ 
        backgroundColor: 'white', 
        padding: '1.5rem', 
        borderRadius: '8px',
        marginTop: '2rem',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h3 style={{ marginBottom: '1rem' }}>Recent Charging History</h3>
        <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
          {chargingHistory.map((session, index) => (
            <div key={index} style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              padding: '1rem', 
              border: '1px solid #e9ecef', 
              borderRadius: '4px', 
              marginBottom: '0.5rem',
              backgroundColor: '#f8f9fa'
            }}>
              <div>
                <strong>{session.station}</strong>
                <div style={{ fontSize: '0.9rem', color: '#6c757d' }}>
                  {session.date} • {session.duration}
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontWeight: 'bold', color: '#28a745' }}>
                  {session.energy}
                </div>
                <div style={{ fontSize: '0.9rem', color: '#6c757d' }}>
                  {session.cost}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Achievements */}
      <div style={{ 
        backgroundColor: 'white', 
        padding: '1.5rem', 
        borderRadius: '8px',
        marginTop: '2rem',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h3 style={{ marginBottom: '1rem' }}>Achievements</h3>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '1rem'
        }}>
          {achievements.map((achievement, index) => (
            <div key={index} style={{ 
              border: '1px solid #e9ecef', 
              borderRadius: '4px', 
              padding: '1rem',
              backgroundColor: '#f8f9fa',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
                {achievement.icon}
              </div>
              <h4 style={{ margin: '0 0 0.5rem 0' }}>{achievement.name}</h4>
              <p style={{ fontSize: '0.9rem', color: '#6c757d', margin: '0 0 0.5rem 0' }}>
                {achievement.description}
              </p>
              <div style={{ fontSize: '0.8rem', color: '#28a745' }}>
                Earned {achievement.earned}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage; 