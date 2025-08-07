import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Snowflake settings
    SNOWFLAKE_USER: str = os.getenv("SNOWFLAKE_USER", "")
    SNOWFLAKE_PASSWORD: str = os.getenv("SNOWFLAKE_PASSWORD", "")
    SNOWFLAKE_ACCOUNT: str = os.getenv("SNOWFLAKE_ACCOUNT", "")
    SNOWFLAKE_WAREHOUSE: str = os.getenv("SNOWFLAKE_WAREHOUSE", "")
    SNOWFLAKE_DATABASE: str = os.getenv("SNOWFLAKE_DATABASE", "")
    SNOWFLAKE_SCHEMA: str = os.getenv("SNOWFLAKE_SCHEMA", "")
    
    # Open Charge Map settings
    OCM_API_KEY: str = os.getenv("OCM_API_KEY", "")
    
    # ML Model settings
    RECOMMENDATION_MODEL_PATH: str = os.getenv("RECOMMENDATION_MODEL_PATH", "models/lightfm_model.pkl")
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "EV User Intelligence & Recommendation Platform"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings() 