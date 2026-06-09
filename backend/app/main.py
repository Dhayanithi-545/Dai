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

from app.mcp.client.mcp_client import (
    MCPClient
)

app = FastAPI(
    title="Dai AI Agent for Dhaya Electric :)"
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
    await MCPClient.connect()


@app.on_event(
    "shutdown"
)
async def shutdown():

    await MCPClient.disconnect()
    MongoDB.close()


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