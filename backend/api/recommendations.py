from fastapi import APIRouter, Query
# from backend.models.schemas import RecommendationResponse
from models.schemas import RecommendationResponse
# from models.recommendation import load_recommendation_model, recommend_stations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.post("/", response_model=RecommendationResponse)
def get_recommendations(user_id: int = Query(...)):
    model = load_recommendation_model()
    recommended_station_ids = recommend_stations(model, user_id)
    return RecommendationResponse(user_id=user_id, recommended_station_ids=recommended_station_ids)