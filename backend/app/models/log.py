from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.sql import func
from app.database import Base


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(String, primary_key=True)
    session_id = Column(String, nullable=False)
    request_id = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    step = Column(String)  # INPUT | TOOL_CALL | LLM_RESPONSE | RESULT
    content = Column(Text)  # JSON
    duration_ms = Column(Integer, nullable=True)
