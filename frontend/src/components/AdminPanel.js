import React, { useState, useEffect } from "react";

const AdminPanel = () => {
  const [users, setUsers] = useState([]);
  const [stations, setStations] = useState([]);
  const [activeTab, setActiveTab] = useState("users");

  useEffect(() => {
    fetchUsers();
    fetchStations();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch("http://localhost:8000/admin/users");
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      }
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  const fetchStations = async () => {
    try {
      const response = await fetch("http://localhost:8000/stations");
      if (response.ok) {
        const data = await response.json();
        setStations(data);
      }
    } catch (error) {
      console.error("Error fetching stations:", error);
    }
  };

  const deleteStation = async (stationId) => {
    try {
      const response = await fetch(`http://localhost:8000/admin/stations/${stationId}`, {
        method: "DELETE"
      });
      if (response.ok) {
        fetchStations(); // Refresh the list
      }
    } catch (error) {
      console.error("Error deleting station:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Admin Panel</h2>
      
      <div style={{ marginBottom: "20px" }}>
        <button 
          onClick={() => setActiveTab("users")}
          style={{ 
            padding: "10px 20px", 
            marginRight: "10px",
            backgroundColor: activeTab === "users" ? "#007bff" : "#f8f9fa",
            color: activeTab === "users" ? "white" : "black",
            border: "1px solid #ddd"
          }}
        >
          Users
        </button>
        <button 
          onClick={() => setActiveTab("stations")}
          style={{ 
            padding: "10px 20px",
            backgroundColor: activeTab === "stations" ? "#007bff" : "#f8f9fa",
            color: activeTab === "stations" ? "white" : "black",
            border: "1px solid #ddd"
          }}
        >
          Stations
        </button>
      </div>

      {activeTab === "users" && (
        <div>
          <h3>Users ({users.length})</h3>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>ID</th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>Email</th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>Eco Score</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{user.id}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{user.email}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{user.eco_score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === "stations" && (
        <div>
          <h3>Stations ({stations.length})</h3>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>ID</th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>Name</th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>Energy Type</th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>Available</th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {stations.map(station => (
                <tr key={station.id}>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{station.id}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{station.name}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{station.energy_type}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {station.available ? "Yes" : "No"}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    <button 
                      onClick={() => deleteStation(station.id)}
                      style={{ 
                        padding: "5px 10px", 
                        backgroundColor: "#dc3545", 
                        color: "white", 
                        border: "none",
                        cursor: "pointer"
                      }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AdminPanel; 