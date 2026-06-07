from fastapi import (
    APIRouter
)

from pydantic import (
    BaseModel
)

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

from app.services.trace_service import (
    TraceService
)

from app.services.tool_validation_service import (
    ToolValidationService
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

    # -------------------------
    # Initialize Trace
    # -------------------------

    trace = (
        TraceService
        .initialize()
    )

    # -------------------------
    # Planner
    # -------------------------

    plan = await (
        MCPPlanner.plan(
            request.message
        )
    )

    TraceService.add_step(

        trace,

        "Planner Decision",

        f"Tool count: "
        f"{len(plan.get('tools', []))}"
    )

    # -------------------------
    # TOOL FLOW
    # -------------------------

    if plan.get(
        "use_tool"
    ):

        tool_outputs = []

        for tool in (
            plan.get(
                "tools",
                []
            )
        ):

            tool_name = (
                tool.get(
                    "tool_name"
                )
            )

            arguments = (
                tool.get(
                    "arguments",
                    {}
                )
            )

            vehicle_id = (
                arguments.get(
                    "vehicle_id"
                )
            )

            # -------------------------
            # Trace Tool Selected
            # -------------------------

            TraceService.add_step(

                trace,

                "Tool Selected",

                tool_name
            )

            # -------------------------
            # Save Vehicle Memory
            # -------------------------

            if vehicle_id:

                await (
                    MemoryService
                    .save_vehicle_context(
                        vehicle_id
                    )
                )

            # -------------------------
            # Execute MCP Tool
            # -------------------------

            result = (
                await MCPClient
                .call_tool(
                    tool_name,
                    arguments
                )
            )

            # -------------------------
            # Tool Validation
            # -------------------------

            validation = (
                ToolValidationService
                .validate_tool_result(
                    tool_name,
                    result
                )
            )

            if not validation[
                "valid"
            ]:

                TraceService.add_step(

                    trace,

                    "Tool Failure",

                    validation[
                        "message"
                    ]
                )

                return {

                    "trace":
                    trace,

                    "response":
                    (
                        "I could not "
                        "complete the "
                        "request.\n\n"
                        f"Reason: "
                        f"{validation['message']}"
                    )
                }

            # -------------------------
            # Trace Tool Execution
            # -------------------------

            TraceService.add_step(

                trace,

                "Tool Executed",

                tool_name
            )

            tool_outputs.append({

                "tool_name":
                tool_name,

                "result":
                result
            })

        # -------------------------
        # Identity Prompt
        # -------------------------

        identity_prompt = (
            load_prompt(
                "identity_prompt.txt"
            )
        )

        # -------------------------
        # Final Response Prompt
        # -------------------------

        final_prompt = (
            load_prompt(

                "response_prompt.txt",

                identity_prompt=
                identity_prompt,

                user_query=
                request.message,

                tool_results=
                tool_outputs
            )
        )

        TraceService.add_step(

            trace,

            "Response Generation",

            "Gemini synthesizing "
            "tool outputs"
        )

        response = (
            await GeminiService
            .generate_response(
                final_prompt
            )
        )

        return {

            "trace":
            trace,

            "tools_used":
            tool_outputs,

            "response":
            response
        }

    # -------------------------
    # NO TOOL FLOW
    # -------------------------

    identity_prompt = (
        load_prompt(
            "identity_prompt.txt"
        )
    )

    general_prompt = f"""
{identity_prompt}

User Query:
{request.message}

Instructions:

1. Respond strictly
as Dai.

2. Never say
you are Google,
Gemini, or a
general AI model.

3. Stay inside
Dhaya Electrics
domain.

4. If unrelated
query:

Politely explain
that you are
Dhaya Electrics'
internal AI
assistant.

5. Maintain
professional tone.

6. Assume
employee context.

Generate response.
"""

    response = (
        await GeminiService
        .generate_response(
            general_prompt
        )
    )

    return {

        "trace":
        trace,

        "response":
        response
    }