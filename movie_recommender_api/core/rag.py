import httpx
from openai import OpenAI
from pinecone import Pinecone
from .config import settings
from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# Initialize clients
try:
    # Set up a proxy if you are behind a corporate proxy
    # proxies = {"http://": "http://user:pass@host:port", "https://": "http://user:pass@host:port"}
    # http_client = httpx.Client(proxies=proxies)
    
    # If no proxy is needed, initialize without the http_client
    openai_client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_API_BASE
    )
    
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    print("Pinecone and OpenAI clients initialized successfully.")

except Exception as e:
    print(f"Error initializing clients: {e}")
    # Handle the error appropriately, maybe raise it to be caught by the FastAPI app
    raise

def get_embedding(text: str):
    """Generates an embedding for the given text using the configured model."""
    try:
        response = openai_client.embeddings.create(
            input=text,
            model=settings.EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def find_similar_movies(embedding, top_k=10):
    """Queries the Pinecone index to find the most similar movies."""
    if not embedding:
        return ""
    try:
        query_response = index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True
        )
        # Format the context for the prompt
        context = "\\n\\n---\\n\\n".join([match['metadata']['text'] for match in query_response['matches']])
        return context
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return ""

def get_rag_recommendation(user_mood: str, past_movies: list, user_request: str):
    """
    Performs the full RAG pipeline to get movie recommendations.
    """
    # 1. Create a combined query for embedding
    combined_query = f"Mood: {user_mood}. Past Movies: {', '.join(past_movies)}. Request: {user_request}"

    # 2. Get the embedding for the query
    query_embedding = get_embedding(combined_query)

    # 3. Retrieve relevant context from Pinecone
    movie_context = find_similar_movies(query_embedding)
    
    if not movie_context:
        return "Could not retrieve relevant movies from the database. Please try a different query."

    # 4. Construct the prompt for the reasoning model
    past_movies_str = ", ".join(past_movies) if past_movies else "None"
    user_prompt = USER_PROMPT_TEMPLATE.format(
        user_mood=user_mood,
        past_movies=past_movies_str,
        user_request=user_request,
        context=movie_context
    )

    # 5. Call the OpenAI API to get the final recommendation
    try:
        chat_completion = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            model=settings.RAG_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error getting completion from OpenAI: {e}")
        return "Sorry, I had trouble generating a recommendation. Please try again."
