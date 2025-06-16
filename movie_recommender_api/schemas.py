from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    user_mood: str
    past_movies: Optional[List[str]] = None
    user_request: str

class RecommendationResponse(BaseModel):
    recommendations: str
