from fastapi import APIRouter, HTTPException, Query
from app.database import supabase
from app.schemas.session import MessageResponse
from typing import List
import json

router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.get("/{session_id}", response_model=List[MessageResponse])
async def list_messages(
    session_id: str,
    limit: int = Query(100, le=500),
    offset: int = 0
):
    """获取会话消息列表"""
    response = supabase.table("messages").select("*").eq("session_id", session_id).order("created_at").limit(limit).offset(offset).execute()
    messages = response.data
    for msg in messages:
        if msg.get("metadata"):
            msg["metadata"] = json.dumps(msg["metadata"])
    return messages


@router.post("/{session_id}")
async def create_message(session_id: str, role: str, content: str, metadata: str = None):
    """创建消息"""
    import uuid
    message_id = str(uuid.uuid4())
    data = {
        "id": message_id,
        "session_id": session_id,
        "role": role,
        "content": content,
        "metadata": metadata
    }
    supabase.table("messages").insert(data).execute()
    return data


@router.get("/{session_id}/search")
async def search_messages(session_id: str, q: str = Query(..., min_length=1)):
    """搜索会话消息"""
    response = supabase.table("messages").select("*").eq("session_id", session_id).ilike("content", f"%{q}%").execute()
    return response.data