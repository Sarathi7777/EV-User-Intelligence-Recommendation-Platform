import React, { useState, useEffect } from "react";

const StationSearch = ({ onStationSelect }) => {
  const [stations, setStations] = useState([]);
  const [filteredStations, setFilteredStations] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [energyType, setEnergyType] = useState("all");

  useEffect(() => {
    fetch("http://localhost:8000/stations")
      .then((res) => res.json())
      .then(setStations)
      .catch(console.error);
  }, []);

  useEffect(() => {
    let filtered = stations;
    
    if (searchTerm) {
      filtered = filtered.filter(station => 
        station.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    if (energyType !== "all") {
      filtered = filtered.filter(station => 
        station.energy_type === energyType
      );
    }
    
    setFilteredStations(filtered);
  }, [stations, searchTerm, energyType]);

  return (
    <div style={{ padding: "20px", border: "1px solid #ccc", margin: "10px" }}>
      <h3>Search Stations</h3>
      
      <div style={{ marginBottom: "10px" }}>
        <input
          type="text"
          placeholder="Search by station name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{ width: "200px", padding: "5px" }}
        />
      </div>
      
      <div style={{ marginBottom: "10px" }}>
        <select 
          value={energyType} 
          onChange={(e) => setEnergyType(e.target.value)}
          style={{ padding: "5px" }}
        >
          <option value="all">All Energy Types</option>
          <option value="Level 2">Level 2</option>
          <option value="DC Fast">DC Fast</option>
          <option value="Level 1">Level 1</option>
        </select>
      </div>
      
      <div style={{ maxHeight: "300px", overflowY: "auto" }}>
        {filteredStations.map((station) => (
          <div 
            key={station.id}
            onClick={() => onStationSelect(station)}
            style={{
              padding: "10px",
              border: "1px solid #ddd",
              margin: "5px 0",
              cursor: "pointer",
              backgroundColor: station.available ? "#e8f5e8" : "#ffe8e8"
            }}
          >
            <strong>{station.name}</strong><br />
            Type: {station.energy_type}<br />
            Status: {station.available ? "Available" : "Occupied"}
          </div>
        ))}
      </div>
    </div>
  );
};

export default StationSearch; 