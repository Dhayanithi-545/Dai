"""
MCP Client — connects to the MCP server over stdio or streamable-http.

Handles initialize handshake, list_tools, and call_tool per the Model Context Protocol.
"""

from __future__ import annotations

import json
import os
import sys
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client
from mcp.types import CallToolResult, Tool

from app.config.settings import settings

BACKEND_DIR = Path(__file__).resolve().parents[3]


class MCPClient:
    """Singleton MCP client that owns the session and transport to the MCP server."""

    _exit_stack: AsyncExitStack | None = None
    _session: ClientSession | None = None
    _tools: list[Tool] = []
    _init_result: Any = None
    _connected = False

    @classmethod
    async def connect(cls) -> None:
        if cls._connected:
            return

        cls._exit_stack = AsyncExitStack()

        if settings.MCP_TRANSPORT == "stdio":
            read, write = await cls._exit_stack.enter_async_context(
                stdio_client(cls._stdio_params())
            )
        elif settings.MCP_TRANSPORT == "streamable-http":
            read, write, _ = await cls._exit_stack.enter_async_context(
                streamable_http_client(settings.MCP_SERVER_URL)
            )
        else:
            raise ValueError(
                f"Unsupported MCP_TRANSPORT: {settings.MCP_TRANSPORT}. "
                "Use 'stdio' or 'streamable-http'."
            )

        cls._session = await cls._exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        cls._init_result = await cls._session.initialize()

        tools_response = await cls._session.list_tools()
        cls._tools = tools_response.tools
        cls._connected = True

    @classmethod
    async def disconnect(cls) -> None:
        if cls._exit_stack:
            await cls._exit_stack.aclose()
        cls._exit_stack = None
        cls._session = None
        cls._tools = []
        cls._init_result = None
        cls._connected = False

    @classmethod
    def is_connected(cls) -> bool:
        return cls._connected and cls._session is not None

    @classmethod
    def get_tools(cls) -> list[Tool]:
        return list(cls._tools)

    @classmethod
    def get_connection_info(cls) -> str:
        if not cls._connected:
            return "Not connected"

        server_name = getattr(cls._init_result, "serverInfo", None)
        if server_name:
            name = getattr(server_name, "name", "unknown")
            version = getattr(server_name, "version", "unknown")
            return f"{settings.MCP_TRANSPORT} | {name} v{version}"

        return f"{settings.MCP_TRANSPORT} | handshake complete"

    @classmethod
    def get_tools_summary(cls) -> str:
        if not cls._tools:
            return "No tools available"
        names = [tool.name for tool in cls._tools]
        return f"{len(names)} tools: {', '.join(names)}"

    @classmethod
    def format_tools_for_planner(cls) -> str:
        if not cls._tools:
            return "No MCP tools available."

        lines = []
        for index, tool in enumerate(cls._tools, start=1):
            lines.append(f"{index}. {tool.name}")
            if tool.description:
                lines.append(f"Description: {tool.description}")
            if tool.inputSchema:
                lines.append(f"Arguments schema: {json.dumps(tool.inputSchema)}")
            lines.append("")

        lines.append(
            "Models: Dhaya Volt, Glide Pro X, EV-9 Titan\n"
            "Plants: Chennai Plant, Hyderabad Plant"
        )
        return "\n".join(lines)

    @classmethod
    async def call_tool(cls, tool_name: str, arguments: dict) -> dict:
        if not cls._session:
            raise RuntimeError("MCP client is not connected. Call MCPClient.connect() first.")

        result: CallToolResult = await cls._session.call_tool(tool_name, arguments)
        return cls._parse_tool_result(result)

    @classmethod
    def _stdio_params(cls) -> StdioServerParameters:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(BACKEND_DIR)

        return StdioServerParameters(
            command=settings.MCP_SERVER_COMMAND or sys.executable,
            args=settings.mcp_server_args_list(),
            env=env,
            cwd=str(BACKEND_DIR),
        )

    @classmethod
    def _parse_tool_result(cls, result: CallToolResult) -> dict:
        if result.isError:
            messages = []
            for content in result.content:
                if hasattr(content, "text"):
                    messages.append(content.text)
            return {"error": " | ".join(messages) or "MCP tool call failed"}

        texts = []
        for content in result.content:
            if hasattr(content, "text"):
                texts.append(content.text)

        combined = "".join(texts).strip()
        if not combined:
            return {}

        try:
            return json.loads(combined)
        except json.JSONDecodeError:
            return {"result": combined}
