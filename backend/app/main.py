from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import sessions, chat, files
from app.agents.agent import DataAnalysisAgent

app = FastAPI(title="Data Analysis Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(",") if settings.allowed_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router)
app.include_router(chat.router)
app.include_router(files.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# WebSocket 支持
class ConnectionManager:
    def __init__(self):
        self.active_connections = set()

    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket):
        self.active_connections.discard(websocket)

    async def send_message(self, message: str, websocket):
        await websocket.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            agent = DataAnalysisAgent()
            result = agent.analyze(data, session_id)
            await websocket.send_json({"type": "result", "data": result})
    except Exception as e:
        manager.disconnect(websocket)
        await websocket.send_json({"type": "error", "message": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)