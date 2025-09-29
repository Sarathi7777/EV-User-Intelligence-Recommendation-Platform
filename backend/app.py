import os
from dotenv import load_dotenv
import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from api import stations, recommendations, sessions, users, admin, forecast
from api import map_features, chatbot
from api import realtime

# Load environment variables from .env file
load_dotenv()


# Sentry integration
SENTRY_DSN = os.getenv('SENTRY_DSN')
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=1.0)

app = FastAPI(title="EV User Intelligence & Recommendation Platform")

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Please try again later."})

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
app.include_router(chatbot.router)
app.include_router(realtime.router)

# Startup tasks: begin Kafka consumers if available and run as background tasks
@app.on_event("startup")
async def startup_event():
    try:
        from api.realtime import start_kafka_home_consumer, start_kafka_location_consumer
        import asyncio
        home_runner = await start_kafka_home_consumer()
        loc_runner = await start_kafka_location_consumer()
        if home_runner:
            asyncio.create_task(home_runner())
        if loc_runner:
            asyncio.create_task(loc_runner())
    except Exception as e:
        print(f"Kafka consumers not started: {e}")