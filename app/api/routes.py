from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import get_llm, get_retriever

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class AskRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/search", summary="Search for movies")
def search(request: SearchRequest, retriever=Depends(get_retriever)):
    """
    Search for movies in the vector store based on a query.
    """
    try:
        results = retriever(request.query, top_k=request.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask", summary="Ask a question about movies")
def ask(request: AskRequest, retriever=Depends(get_retriever), llm=Depends(get_llm)):
    """
    Ask a question and get an answer from the RAG pipeline.
    """
    try:
        # 1. Retrieve context
        context_docs = retriever(request.query, top_k=request.top_k)
        context = "\n".join([doc["metadata"]["text"] for doc in context_docs])

        # 2. Generate prompt
        prompt = f"""
        Use the following context to answer the question.
        If you don't know the answer, just say that you don't know.

        Context:
        {context}

        Question: {request.query}
        Answer:
        """

        # 3. Get completion
        answer = llm(prompt)
        return {"answer": answer, "context": context_docs}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
