from fastapi import APIRouter, HTTPException
from app.services.session_manager import SessionManager
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse
from typing import List

router = APIRouter(prefix="/api/sessions", tags=["sessions"])
manager = SessionManager()


@router.post("/", response_model=SessionResponse)
async def create_session(session: SessionCreate):
    return manager.create_session(title=session.title)


@router.get("/", response_model=List[SessionResponse])
async def list_sessions(user_id: str = None, limit: int = 50):
    return manager.list_sessions(user_id=user_id, limit=limit)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    session = manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.patch("/{session_id}", response_model=SessionResponse)
async def update_session(session_id: str, session: SessionUpdate):
    return manager.update_session(session_id, **session.dict(exclude_unset=True))


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    manager.delete_session(session_id)
    return {"status": "deleted"}


@router.post("/{session_id}/share")
async def share_session(session_id: str):
    token = manager.share_session(session_id)
    return {"share_token": token}


@router.get("/shared/{share_token}")
async def get_shared_session(share_token: str):
    session = manager.get_shared_session(share_token)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/search")
async def search_sessions(q: str):
    return manager.search_sessions(q)