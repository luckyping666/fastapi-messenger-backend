from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_router import router



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


app.include_router(router)


@app.get("/")
def root():
    return {"message": "Backend is running ✅"}
