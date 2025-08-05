from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from ..schemas.chatbot import ChatMessage, ChatResponse, ChatRequest, ChatSession, ChatHistory
from ..utils.database import get_db
from ..utils.chatbot_service import ChatbotService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Chat with AI tutor"""
    try:
        chatbot_service = ChatbotService(db)
        response = chatbot_service.process_chat_message(request)
        return response
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process chat message")

@router.get("/sessions/{session_id}", response_model=ChatHistory)
async def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get chat history for a session"""
    try:
        chatbot_service = ChatbotService(db)
        history = chatbot_service.get_chat_history(session_id)
        if not history:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return history
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching chat history for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat history")

@router.get("/sessions/", response_model=List[ChatSession])
async def get_user_sessions(
    user_id: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get user's chat sessions"""
    try:
        chatbot_service = ChatbotService(db)
        sessions = chatbot_service.get_user_sessions(user_id, limit)
        return sessions
    except Exception as e:
        logger.error(f"Error fetching user sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch user sessions")

@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Delete a chat session"""
    try:
        chatbot_service = ChatbotService(db)
        success = chatbot_service.delete_chat_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return {"message": "Chat session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting chat session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete chat session")

@router.post("/sessions/{session_id}/clear")
async def clear_chat_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Clear messages from a chat session"""
    try:
        chatbot_service = ChatbotService(db)
        success = chatbot_service.clear_chat_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return {"message": "Chat session cleared successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing chat session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear chat session")

@router.get("/materials/{material_id}/chat")
async def start_material_chat(
    material_id: int,
    db: Session = Depends(get_db)
):
    """Start a chat session focused on a specific material"""
    try:
        chatbot_service = ChatbotService(db)
        session = chatbot_service.start_material_chat(material_id)
        return session
    except Exception as e:
        logger.error(f"Error starting material chat for material {material_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start material chat")

@router.get("/context/{material_id}")
async def get_material_context(
    material_id: int,
    db: Session = Depends(get_db)
):
    """Get context information for a material to help with chat"""
    try:
        chatbot_service = ChatbotService(db)
        context = chatbot_service.get_material_context(material_id)
        if not context:
            raise HTTPException(status_code=404, detail="Material not found")
        return context
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching material context for material {material_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch material context")

@router.post("/feedback")
async def submit_chat_feedback(
    session_id: str,
    message_id: int,
    rating: int,
    feedback: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Submit feedback for a chat message"""
    try:
        chatbot_service = ChatbotService(db)
        success = chatbot_service.submit_feedback(session_id, message_id, rating, feedback)
        if not success:
            raise HTTPException(status_code=404, detail="Message not found")
        return {"message": "Feedback submitted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback") 