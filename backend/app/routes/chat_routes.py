from fastapi import APIRouter, Header, status
from fastapi.responses import StreamingResponse
from typing import Optional

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with Groq LLM (Standard Blocking Response)"
)
async def chat_with_llm(
    request: ChatRequest,
    x_groq_api_key: Optional[str] = Header(None, description="Optional custom Groq API key")
):
    """
    Start or continue a chat conversation with the Groq LLM model.
    This endpoint returns the complete response after generation finishes.
    You can optionally provide the Groq API key through:
    1. The request body `api_key`
    2. The request header `X-Groq-API-Key`
    3. If neither is provided, the backend falls back to the server-configured environment variable.
    """
    # Resolve the API key
    api_key = ChatService.get_api_key(
        custom_key=request.api_key,
        header_key=x_groq_api_key
    )

    # Generate response asynchronously
    return await ChatService.generate_chat_response(
        message=request.message,
        history=request.history or [],
        model=request.model or "llama-3.3-70b-versatile",
        temperature=request.temperature if request.temperature is not None else 0.7,
        api_key=api_key
    )

@router.post(
    "/stream",
    status_code=status.HTTP_200_OK,
    summary="Chat with Groq LLM (Real-time Streaming Response)"
)
async def chat_with_llm_stream(
    request: ChatRequest,
    x_groq_api_key: Optional[str] = Header(None, description="Optional custom Groq API key")
):
    """
    Start or continue a chat conversation with the Groq LLM model, streaming the output
    chunk-by-chunk in real-time as a Server-Sent Events (SSE) stream.
    
    Yields data in format: `data: {"text": "chunk_content", "model": "model_name"}`
    """
    # Resolve the API key
    api_key = ChatService.get_api_key(
        custom_key=request.api_key,
        header_key=x_groq_api_key
    )

    # Return StreamingResponse with text/event-stream media type
    return StreamingResponse(
        ChatService.generate_chat_stream(
            message=request.message,
            history=request.history or [],
            model=request.model or "llama-3.3-70b-versatile",
            temperature=request.temperature if request.temperature is not None else 0.7,
            api_key=api_key
        ),
        media_type="text/event-stream"
    )
