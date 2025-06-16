from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import RecommendationRequest, RecommendationResponse
from .core.rag import get_rag_recommendation
from .core.config import settings

app = FastAPI(
    title="Movie Recommendation API",
    description="A RAG-based API for providing movie recommendations.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
def on_startup():
    """
    Perform a health check on the required services at startup.
    This is a good practice to ensure the API starts in a healthy state.
    """
    if not settings.PINECONE_API_KEY or not settings.OPENAI_API_KEY:
        raise RuntimeError("API keys for Pinecone or OpenAI are not set. Please check your .env file.")
    
    # You might add more sophisticated health checks here,
    # like trying to connect to Pinecone or making a small OpenAI API call.
    print("FastAPI application startup complete. Configuration loaded.")


@app.post("/recommend", response_model=RecommendationResponse)
def recommend_movies(request: RecommendationRequest):
    """
    Receives user's mood, past movies, and a specific request to generate
    movie recommendations using a RAG pipeline.
    """
    try:
        recommendations = get_rag_recommendation(
            user_mood=request.user_mood,
            past_movies=request.past_movies or [],
            user_request=request.user_request
        )
        
        if not recommendations or "Could not retrieve" in recommendations or "had trouble" in recommendations:
            raise HTTPException(status_code=500, detail=recommendations)

        return RecommendationResponse(recommendations=recommendations)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Recommendation API. Use the /docs endpoint to see the API documentation."}
