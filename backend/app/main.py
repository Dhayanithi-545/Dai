from fastapi import (
    FastAPI
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.api.chat import (
    router as chat_router
)

from app.database.mongodb import (
    MongoDB
)

app = FastAPI(
    title="Dai AI Agent"
)

# CORS

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


@app.on_event(
    "startup"
)
async def startup():

    MongoDB.connect()


app.include_router(
    chat_router,
    prefix="/chat"
)


@app.get("/")
def root():

    return {
        "message":
        "Dai Backend Running"
    }