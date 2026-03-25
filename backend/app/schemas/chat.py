from pydantic import BaseModel
from typing import Optional, List, Any


class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    files: Optional[List[str]] = []  # File IDs


class ChatResponse(BaseModel):
    session_id: str
    message_id: str
    response: str
    charts: Optional[List[dict]] = None
    sql_queries: Optional[List[str]] = None