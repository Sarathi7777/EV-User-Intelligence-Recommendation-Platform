from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from backend.api import stations, recommendations, sessions, users, admin, forecast
from api import stations, recommendations, sessions, users, admin, forecast
from api import map_features


app = FastAPI(title="EV User Intelligence & Recommendation Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stations.router)
app.include_router(recommendations.router)
app.include_router(sessions.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(forecast.router)
app.include_router(map_features.router)