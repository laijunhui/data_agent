from fastapi import APIRouter, UploadFile, File
from app.agents.agent import DataAnalysisAgent
from app.schemas.chat import ChatMessage, ChatResponse
from app.services.session_manager import SessionManager
import uuid

router = APIRouter(prefix="/api/chat", tags=["chat"])
agent = DataAnalysisAgent()
session_manager = SessionManager()


@router.post("/", response_model=ChatResponse)
async def chat(message: ChatMessage):
    if not message.session_id:
        session = session_manager.create_session()
        message.session_id = session["id"]

    result = agent.analyze(message.message, message.session_id)

    return ChatResponse(
        session_id=result["session_id"],
        message_id=str(uuid.uuid4()),
        response=result["response"],
        sql_queries=result.get("sql_queries", []),
        charts=result.get("charts", [])
    )