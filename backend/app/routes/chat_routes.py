from fastapi import APIRouter, Header, status
from typing import Optional

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with Gemini LLM"
)
def chat_with_llm(
    request: ChatRequest,
    x_gemini_api_key: Optional[str] = Header(None, description="Optional custom Gemini API key")
):
    """
    Start or continue a chat conversation with the Gemini LLM model.
    You can optionally provide the Gemini API key through:
    1. The request body `api_key`
    2. The request header `X-Gemini-API-Key`
    3. If neither is provided, the backend falls back to the server-configured environment variable.
    """
    # Resolve the API key
    api_key = ChatService.get_api_key(
        custom_key=request.api_key,
        header_key=x_gemini_api_key
    )

    # Generate response
    return ChatService.generate_chat_response(
        message=request.message,
        history=request.history or [],
        model="gemini-2.5-flash-lite",
        temperature=request.temperature if request.temperature is not None else 0.7,
        api_key=api_key
    )
