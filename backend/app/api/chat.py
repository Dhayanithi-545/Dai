import json

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.gemini_service import GeminiService
from app.mcp.planner.planner import MCPPlanner
from app.mcp.client.mcp_client import MCPClient
from app.utils.prompt_loader import load_prompt
from app.services.memory_service import MemoryService
from app.services.trace_service import TraceService
from app.services.tool_validation_service import ToolValidationService
from app.services.visualization_service import VisualizationService


router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(request: ChatRequest):
    trace = TraceService.initialize()

    plan = await MCPPlanner.plan(request.message)
    intent = plan.get("intent", "lookup")
    tools_planned = plan.get("tools", [])

    TraceService.add_step(
        trace,
        "Planner Decision",
        f"Intent: {intent} | Tools: {len(tools_planned)}",
    )

    await MemoryService.save_context(
        intent=intent,
        query=request.message,
    )

    if plan.get("use_tool") and tools_planned:
        tool_outputs = []
        errors = []

        for tool in tools_planned:
            tool_name = tool.get("tool_name")
            arguments = tool.get("arguments", {})

            TraceService.add_step(trace, "Tool Selected", f"{tool_name} | {arguments}")

            if arguments.get("vehicle_id"):
                await MemoryService.save_context(vehicle_id=arguments["vehicle_id"])
            if arguments.get("model_name"):
                await MemoryService.save_context(model_name=arguments["model_name"])
            if arguments.get("plant") or arguments.get("plant_name"):
                await MemoryService.save_context(
                    plant=arguments.get("plant") or arguments.get("plant_name")
                )

            result = await MCPClient.call_tool(tool_name, arguments)
            validation = ToolValidationService.validate_tool_result(tool_name, result)

            if not validation["valid"]:
                TraceService.add_step(trace, "Tool Warning", validation["message"])
                errors.append({"tool_name": tool_name, "error": validation["message"]})
                tool_outputs.append({
                    "tool_name": tool_name,
                    "result": {"error": validation["message"]},
                })
                continue

            TraceService.add_step(trace, "Tool Executed", tool_name)
            tool_outputs.append({"tool_name": tool_name, "result": result})

        if not any(not o["result"].get("error") for o in tool_outputs):
            return {
                "type": "analytics_response",
                "trace": trace,
                "response": (
                    "I could not retrieve the requested data.\n\n"
                    + "\n".join(f"- {e['tool_name']}: {e['error']}" for e in errors)
                ),
                "widgets": [],
                "insights": [],
            }

        widgets = VisualizationService.generate_widgets(tool_outputs, plan)
        insights = VisualizationService.generate_insights(tool_outputs, plan)

        identity_prompt = load_prompt("identity_prompt.txt")

        final_prompt = load_prompt(
            "response_prompt.txt",
            identity_prompt=identity_prompt,
            user_query=request.message,
            intent=intent,
            tool_results=json.dumps(tool_outputs, indent=2, default=str),
        )

        TraceService.add_step(trace, "Response Generation", "Gemini synthesizing tool outputs")

        response = await GeminiService.generate_response(final_prompt)

        return {
            "type": "analytics_response",
            "trace": trace,
            "tools_used": tool_outputs,
            "response": response,
            "summary": response,
            "widgets": widgets,
            "insights": insights,
            "intent": intent,
        }

    identity_prompt = load_prompt("identity_prompt.txt")

    general_prompt = load_prompt(
        "fallback_prompt.txt",
        identity_prompt=identity_prompt,
        user_query=request.message,
    )

    TraceService.add_step(trace, "Response Generation", "Direct response (no tools)")

    response = await GeminiService.generate_response(general_prompt)

    return {
        "type": "analytics_response",
        "trace": trace,
        "response": response,
        "widgets": [],
        "insights": [],
    }
