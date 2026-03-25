import uuid
import time
import json
from typing import Any, Dict, Optional
from datetime import datetime
from supabase import create_client, Client
from app.config import settings


class AgentLogger:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )

    def log(
        self,
        session_id: str,
        request_id: str,
        step: str,
        content: Any,
        duration_ms: Optional[int] = None
    ) -> dict:
        """记录日志"""
        log_id = str(uuid.uuid4())
        data = {
            "id": log_id,
            "session_id": session_id,
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "step": step,
            "content": json.dumps(content, ensure_ascii=False, default=str),
            "duration_ms": duration_ms
        }
        self.supabase.table("agent_logs").insert(data).execute()
        return data

    def log_input(self, session_id: str, request_id: str, message: str):
        return self.log(session_id, request_id, "INPUT", {"message": message})

    def log_tool_call(self, session_id: str, request_id: str, tool: str, input_data: dict):
        return self.log(session_id, request_id, "TOOL_CALL", {"tool": tool, "input": input_data})

    def log_llm_response(self, session_id: str, request_id: str, response: str, duration_ms: int):
        return self.log(session_id, request_id, "LLM_RESPONSE", {"response": response}, duration_ms)

    def log_result(self, session_id: str, request_id: str, result: dict):
        return self.log(session_id, request_id, "RESULT", result)

    def get_session_logs(self, session_id: str) -> list:
        response = self.supabase.table("agent_logs").select("*").eq("session_id", session_id).order("timestamp").execute()
        return response.data
