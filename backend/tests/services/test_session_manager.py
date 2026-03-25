import pytest
from app.services.session_manager import SessionManager
from uuid import uuid4


def test_create_session():
    manager = SessionManager()
    session = manager.create_session()
    assert session["id"] is not None
    assert session["title"] == "新会话"


def test_get_session():
    manager = SessionManager()
    session = manager.create_session()
    retrieved = manager.get_session(session["id"])
    assert retrieved["id"] == session["id"]