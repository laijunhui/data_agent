from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SessionCreate(BaseModel):
    title: Optional[str] = "新会话"


class SessionUpdate(BaseModel):
    title: Optional[str] = None
    is_shared: Optional[bool] = None


class SessionResponse(BaseModel):
    id: str
    title: str
    user_id: Optional[str]
    is_shared: bool
    share_token: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    session_id: str
    role: str
    content: str
    metadata: Optional[str] = None


class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    metadata: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True