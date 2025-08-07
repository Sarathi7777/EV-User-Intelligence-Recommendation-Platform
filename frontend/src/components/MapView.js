import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const API_URL = "http://localhost:8000/stations";

const MapView = () => {
  const [stations, setStations] = useState([]);

  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then(setStations)
      .catch(console.error);
  }, []);

  return (
    <MapContainer center={[10.877185, 77.005055]} zoom={12} style={{ height: "80vh", width: "100%" }}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" 
      />
      {stations
        .filter(station => station.latitude !== undefined && station.longitude !== undefined)
        .map((station) => (
          <Marker key={station.id} position={[station.latitude, station.longitude]}>
            <Popup>
              <b>{station.name}</b><br />
              Energy: {station.energy_type}<br />
              {station.available ? "Available" : "Occupied"}
            </Popup>
          </Marker>
        ))}
    </MapContainer>
  );
};

export default MapView;