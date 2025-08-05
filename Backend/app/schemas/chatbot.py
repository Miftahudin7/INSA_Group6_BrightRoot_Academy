from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessageBase(BaseModel):
    content: str = Field(..., description="Message content")
    role: MessageRole = Field(..., description="Role of the message sender")
    session_id: Optional[str] = Field(None, description="Chat session ID")
    material_id: Optional[int] = Field(None, description="ID of the material being discussed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    message: str = Field(..., description="AI response message")
    sources: Optional[List[str]] = Field(None, description="Source materials used")
    confidence: Optional[float] = Field(None, description="Confidence score of the response")
    session_id: str = Field(..., description="Chat session ID")

class ChatSession(BaseModel):
    id: str = Field(..., description="Session ID")
    user_id: Optional[int] = Field(None, description="User ID")
    material_id: Optional[int] = Field(None, description="Material being discussed")
    created_at: datetime
    last_activity: datetime
    message_count: int = Field(0, description="Number of messages in session")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Existing session ID")
    material_id: Optional[int] = Field(None, description="Material to focus on")
    context: Optional[str] = Field(None, description="Additional context for the AI")

class ChatHistory(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    material_info: Optional[Dict[str, Any]] = Field(None, description="Information about the material being discussed") 