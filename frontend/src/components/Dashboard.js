import React from "react";
import Plot from "react-plotly.js";

const Dashboard = ({ energyData }) => (
  <div>
    <h2>Energy Consumption</h2>
    <Plot
      data={[
        {
          x: energyData.dates,
          y: energyData.kWh,
          type: "bar",
        },
      ]}
      layout={{ title: "Energy Consumption" }}
    />
  </div>
);

export default Dashboard;