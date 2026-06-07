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

from app.utils.prompt_loader import (
    load_prompt
)

from app.services.memory_service import (
    MemoryService
)


router = APIRouter()


class ChatRequest(
    BaseModel
):
    message: str


@router.post("/")
async def chat(
    request: ChatRequest
):

    plan = await MCPPlanner.plan(
        request.message
    )

    if plan["use_tool"]:

        tool_outputs = []

        for tool in plan["tools"]:

            vehicle_id = (
                tool["arguments"]
                .get("vehicle_id")
            )

            if vehicle_id:

                await MemoryService.save_vehicle_context(
                    vehicle_id
                )
            else:

                await MemoryService.clear_vehicle_context()

            if not vehicle_id:

                return {
                    "response":
                    "Please provide the vehicle ID."
                }


            result = (
                await MCPClient.call_tool(
                    tool["tool_name"],
                    tool["arguments"]
                )
            )

            tool_outputs.append({

                "tool_name":
                tool["tool_name"],

                "result":
                result
            })

        final_prompt = load_prompt(
            "response_prompt.txt",
            user_query=
            request.message,

            tool_results=
            tool_outputs
        )

        response = (
            await GeminiService
            .generate_response(
                final_prompt
            )
        )

        return {

            "tools_used":
            tool_outputs,

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
        "response":
        response
    }