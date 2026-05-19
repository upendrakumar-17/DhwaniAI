import os
import json
from fastapi import HTTPException, status
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import List, Optional
from app.schemas.chat_schema import ChatMessage, ChatResponse

class ChatService:
    @staticmethod
    def get_api_key(custom_key: Optional[str] = None, header_key: Optional[str] = None) -> str:
        """
        Determines which Groq API key to use.
        Priority:
        1. Custom key passed in request body
        2. Key passed in custom header (X-Groq-API-Key)
        3. GROQ_API_KEY environment variable
        """
        api_key = custom_key or header_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Groq API Key is missing. Please provide it in the 'X-Groq-API-Key' header, in the request body, or configure 'GROQ_API_KEY' in the environment variables."
            )
        return api_key

    @classmethod
    async def generate_chat_response(
        cls,
        message: str,
        history: List[ChatMessage],
        model: str,
        temperature: float,
        api_key: str
    ) -> ChatResponse:
        """
        Creates a ChatGoogleGenerativeAI instance and asynchronously gets the full response.
        """
        # Convert history and current message into LangChain format
        langchain_messages = []
        for msg in history:
            role = msg.role.lower()
            if role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif role in ("assistant", "model"):
                langchain_messages.append(AIMessage(content=msg.content))
            elif role == "system":
                langchain_messages.append(SystemMessage(content=msg.content))
            else:
                langchain_messages.append(HumanMessage(content=msg.content))

        # Add the current message
        langchain_messages.append(HumanMessage(content=message))

        try:
            llm = ChatGroq(
                model=model,
                groq_api_key=api_key,
                temperature=temperature
            )
            
            # Using async ainvoke to prevent blocking the event loop
            response = await llm.ainvoke(langchain_messages)
            
            return ChatResponse(
                response=response.content,
                model=model
            )
        except Exception as e:
            # Handle potential API errors gracefully
            error_message = str(e)
            if "API_KEY_INVALID" in error_message or "API key not valid" in error_message or "invalid_api_key" in error_message:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="The provided Groq API key is invalid. Please check your key and try again."
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating chat response: {error_message}"
            )

    @classmethod
    async def generate_chat_stream(
        cls,
        message: str,
        history: List[ChatMessage],
        model: str,
        temperature: float,
        api_key: str
    ):
        """
        Asynchronously streams the chat response chunk-by-chunk in real-time.
        Yields standard SSE formatted events: data: { "text": "chunk" }
        """
        # Convert history and current message into LangChain format
        langchain_messages = []
        for msg in history:
            role = msg.role.lower()
            if role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif role in ("assistant", "model"):
                langchain_messages.append(AIMessage(content=msg.content))
            elif role == "system":
                langchain_messages.append(SystemMessage(content=msg.content))
            else:
                langchain_messages.append(HumanMessage(content=msg.content))

        # Add current message
        langchain_messages.append(HumanMessage(content=message))

        try:
            llm = ChatGroq(
                model=model,
                groq_api_key=api_key,
                temperature=temperature
            )
            
            # Use LangChain astream to asynchronously stream chunks from the API
            async for chunk in llm.astream(langchain_messages):
                if chunk.content:
                    # Yield SSE structured data chunk
                    yield f"data: {json.dumps({'text': chunk.content, 'model': model})}\n\n"
                    
        except Exception as e:
            error_message = str(e)
            if "API_KEY_INVALID" in error_message or "API key not valid" in error_message or "invalid_api_key" in error_message:
                yield f"data: {json.dumps({'error': 'The provided Groq API key is invalid.'})}\n\n"
            else:
                yield f"data: {json.dumps({'error': error_message})}\n\n"
