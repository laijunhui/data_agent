import uuid
from typing import List, Optional
from datetime import datetime
from supabase import create_client, Client
from app.config import settings


class SessionManager:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )

    def create_session(self, title: str = "新会话", user_id: str = None) -> dict:
        session_id = str(uuid.uuid4())
        data = {
            "id": session_id,
            "title": title,
            "user_id": user_id
        }
        self.supabase.table("sessions").insert(data).execute()
        return data

    def get_session(self, session_id: str) -> Optional[dict]:
        response = self.supabase.table("sessions").select("*").eq("id", session_id).execute()
        return response.data[0] if response.data else None

    def list_sessions(self, user_id: str = None, limit: int = 50) -> List[dict]:
        query = self.supabase.table("sessions").select("*").order("updated_at", desc=True).limit(limit)
        if user_id:
            query = query.eq("user_id", user_id)
        return query.execute().data

    def update_session(self, session_id: str, **kwargs) -> dict:
        self.supabase.table("sessions").update(kwargs).eq("id", session_id).execute()
        return self.get_session(session_id)

    def delete_session(self, session_id: str) -> bool:
        self.supabase.table("sessions").delete().eq("id", session_id).execute()
        return True

    def share_session(self, session_id: str) -> str:
        share_token = str(uuid.uuid4())[:8]
        self.supabase.table("sessions").update({
            "is_shared": True,
            "share_token": share_token
        }).eq("id", session_id).execute()
        return share_token

    def get_shared_session(self, share_token: str) -> Optional[dict]:
        response = self.supabase.table("sessions").select("*").eq("share_token", share_token).execute()
        return response.data[0] if response.data else None

    def search_sessions(self, query: str) -> List[dict]:
        sessions = self.supabase.table("sessions").select("*").ilike("title", f"%{query}%").execute().data
        messages = self.supabase.table("messages").select("session_id").ilike("content", f"%{query}%").execute().data
        session_ids = list(set(m.get("session_id") for m in messages if m.get("session_id")))
        if session_ids:
            related_sessions = self.supabase.table("sessions").select("*").in_("id", session_ids).execute().data
            session_dict = {s["id"]: s for s in sessions}
            for s in related_sessions:
                if s["id"] not in session_dict:
                    sessions.append(s)
        return sessions