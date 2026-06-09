import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings:
    APP_NAME = "Dai AI Agent"
    APP_VERSION = "1.0.0"

    MONGO_URI = os.getenv("MONGO_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS"
    )

    GOOGLE_PROJECT_ID = os.getenv(
        "GOOGLE_PROJECT_ID"
    )

    GOOGLE_LOCATION = os.getenv(
        "GOOGLE_LOCATION"
    )

    # MCP transport: "stdio" (spawn local server) or "streamable-http" (remote URL)
    MCP_TRANSPORT = os.getenv("MCP_TRANSPORT")

    # stdio transport — command to spawn the MCP server subprocess
    MCP_SERVER_COMMAND = os.getenv("MCP_SERVER_COMMAND", sys.executable)

    # JSON array or comma-separated args, e.g. '["mcp_server.py","--transport","stdio"]'
    MCP_SERVER_ARGS = os.getenv(
        "MCP_SERVER_ARGS",
        '["mcp_server.py", "--transport", "stdio"]',
    )

    # streamable-http transport — URL of a remote/cloud MCP server
    MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8001/mcp")
 
    def mcp_server_args_list(self) -> list[str]:
        raw = self.MCP_SERVER_ARGS.strip()
        if raw.startswith("["):
            return json.loads(raw)
        return [part.strip() for part in raw.split(",") if part.strip()]


settings = Settings()
