import React, { useEffect, useState } from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  ArcElement
} from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, PointElement, LineElement, ArcElement);

const AdminPanel = () => {
  const [userGrowth, setUserGrowth] = useState([]);
  const [sessionStats, setSessionStats] = useState([]);
  const [stationUsage, setStationUsage] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/admin/analytics/user-growth')
      .then(res => res.json())
      .then(setUserGrowth);
    fetch('http://localhost:8000/admin/analytics/session-stats')
      .then(res => res.json())
      .then(setSessionStats);
    fetch('http://localhost:8000/admin/analytics/station-usage')
      .then(res => res.json())
      .then(setStationUsage);
  }, []);

  return (
    <div style={{ padding: 32 }}>
      <h2>Admin Analytics</h2>
      <div style={{ display: 'flex', gap: 32, flexWrap: 'wrap' }}>
        <div style={{ width: 400 }}>
          <h3>User Growth (Last 30 Days)</h3>
          <Line
            data={{
              labels: userGrowth.map(d => d.date),
              datasets: [{
                label: 'Registrations',
                data: userGrowth.map(d => d.count),
                borderColor: '#28a745',
                backgroundColor: 'rgba(40,167,69,0.2)',
                tension: 0.3
              }]
            }}
          />
        </div>
        <div style={{ width: 400 }}>
          <h3>Sessions & Energy (Last 30 Days)</h3>
          <Bar
            data={{
              labels: sessionStats.map(d => d.date),
              datasets: [
                {
                  label: 'Sessions',
                  data: sessionStats.map(d => d.sessions),
                  backgroundColor: '#007bff',
                },
                {
                  label: 'Total Energy (kWh)',
                  data: sessionStats.map(d => d.total_energy),
                  backgroundColor: '#ffc107',
                }
              ]
            }}
            options={{ responsive: true, plugins: { legend: { position: 'top' } } }}
          />
        </div>
        <div style={{ width: 400 }}>
          <h3>Top Stations by Usage</h3>
          <Pie
            data={{
              labels: stationUsage.map(d => d.name),
              datasets: [{
                label: 'Sessions',
                data: stationUsage.map(d => d.total_sessions),
                backgroundColor: [
                  '#28a745', '#007bff', '#ffc107', '#dc3545', '#20c997'
                ]
              }]
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default AdminPanel; 