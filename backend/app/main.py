from fastapi import FastAPI

from app.database.mongodb import MongoDB
from app.services.gemini_service import (
    GeminiService
)

from app.api.chat import (
    router as chat_router
)

app = FastAPI(
    title="Dai AI Agent",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():

    MongoDB.connect()

    GeminiService.initialize()


app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)


@app.get("/")
async def root():
    return {
        "message": "Dai Backend Running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


@app.get("/health/db")
async def db_health_check():

    try:
        db = MongoDB.get_database()

        db.command("ping")

        return {
            "status": "connected",
            "database": db.name
        }

    except Exception as e:
        return {
            "status": "disconnected",
            "error": str(e)
        }


@app.get("/health/ai")
async def ai_health_check():

    client = GeminiService.get_client()

    if client:
        return {
            "status": "connected",
            "model": "gemini-2.5-flash"
        }

    return {
        "status": "disconnected"
    }