from fastapi import APIRouter, Query
from typing import List
import numpy as np
from datetime import datetime, timedelta

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("/energy-demand")
def get_energy_demand_forecast(days: int = Query(7, description="Number of days to forecast")):
    """Get energy demand forecast for the next N days."""
    # Mock implementation - replace with actual ML model
    dates = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    demand = np.random.normal(100, 20, days).tolist()  # Mock data
    
    return {
        "forecast_dates": dates,
        "predicted_demand_kwh": demand,
        "model_used": "XGBoost Time Series",
        "confidence_interval": [max(0, d - 10) for d in demand]
    }

@router.get("/station-usage/{station_id}")
def get_station_usage_forecast(station_id: int, hours: int = Query(24)):
    """Get usage forecast for a specific station."""
    # Mock implementation
    hours_list = list(range(hours))
    usage = np.random.poisson(5, hours).tolist()  # Mock Poisson distribution
    
    return {
        "station_id": station_id,
        "forecast_hours": hours_list,
        "predicted_usage": usage,
        "peak_hours": [8, 12, 18]  # Mock peak hours
    } 