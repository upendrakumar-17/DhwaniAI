import os
from fastapi import HTTPException, status
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import List, Optional
from app.schemas.chat_schema import ChatMessage, ChatResponse

class ChatService:
    @staticmethod
    def get_api_key(custom_key: Optional[str] = None, header_key: Optional[str] = None) -> str:
        """
        Determines which Gemini API key to use.
        Priority:
        1. Custom key passed in request body
        2. Key passed in custom header (X-Gemini-API-Key)
        3. GEMINI_API_KEY environment variable
        """
        api_key = custom_key or header_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Gemini API Key is missing. Please provide it in the 'X-Gemini-API-Key' header, in the request body, or configure 'GEMINI_API_KEY' in the environment variables."
            )
        return api_key

    @classmethod
    def generate_chat_response(
        cls,
        message: str,
        history: List[ChatMessage],
        model: str,
        temperature: float,
        api_key: str
    ) -> ChatResponse:
        """
        Creates a ChatGoogleGenerativeAI instance and gets a response for the user prompt
        considering the conversation history.
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
            llm = ChatGoogleGenerativeAI(
                model=model,
                google_api_key=api_key,
                temperature=temperature
            )
            
            response = llm.invoke(langchain_messages)
            
            return ChatResponse(
                response=response.content,
                model=model
            )
        except Exception as e:
            # Handle potential API errors gracefully
            error_message = str(e)
            if "API_KEY_INVALID" in error_message or "API key not valid" in error_message:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="The provided Gemini API key is invalid. Please check your key and try again."
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating chat response: {error_message}"
            )
