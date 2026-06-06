from fastapi import APIRouter
from pydantic import BaseModel

from app.services.gemini_service import (
    GeminiService
)

from app.mcp.planner.planner import (
    MCPPlanner
)

from app.mcp.client.mcp_client import (
    MCPClient
)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(
    request: ChatRequest
):

    plan = await MCPPlanner.plan(
        request.message
    )

    if plan["use_tool"]:

        tool_result = (
            await MCPClient.call_tool(
                plan["tool_name"],
                plan["arguments"]
            )
        )

        final_prompt = f"""
User Question:
{request.message}

Tool Result:
{tool_result}

Answer professionally.
"""

        response = (
            await GeminiService
            .generate_response(
                final_prompt
            )
        )

        return {
            "tool_used":
            plan["tool_name"],

            "tool_result":
            tool_result,

            "response":
            response
        }

    response = (
        await GeminiService
        .generate_response(
            request.message
        )
    )

    return {
        "tool_used": None,
        "response": response
    }