from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message author: 'user', 'assistant' or 'system'")
    content: str = Field(..., description="The content of the message")

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="The current user prompt/message to the LLM")
    history: Optional[List[ChatMessage]] = Field(default=[], description="The chat history of previous messages between the user and the LLM")
    model: Optional[str] = Field(default="llama-3.3-70b-versatile", description="The Groq model name to use (e.g. llama-3.3-70b-versatile, llama3-8b-8192, etc.)")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="The sampling temperature to use")
    api_key: Optional[str] = Field(default=None, description="Optional custom Groq API key. If not provided, fallback to the server's GROQ_API_KEY environment variable.")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The generated response from the LLM")
    model: str = Field(..., description="The exact model name used to generate the response")

    class Config:
        from_attributes = True
