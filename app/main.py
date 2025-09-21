from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_router import router as auth_router
from app.routes.chat_router import router as chat_router
from app.routes.message_router import router as message_router


app = FastAPI(
    title="FastAPI Messenger Backend",
    description="Backend для мобильного мессенджера на FastAPI",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(message_router)


@app.get("/")
def root():
    return {"message": "Backend is running ✅"}
