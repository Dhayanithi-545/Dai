import json

from app.services.gemini_service import (
    GeminiService
)

from app.mcp.tools.tool_descriptions import (
    AVAILABLE_TOOLS
)

from app.utils.prompt_loader import (
    load_prompt
)

from app.services.memory_service import (
    MemoryService
)

class MCPPlanner:

    @classmethod
    async def plan(
        cls,
        user_query: str
    ):

        previous_vehicle = (
            await MemoryService
            .get_last_vehicle()
        )

        planner_prompt = load_prompt(
            "planner_prompt.txt",
            available_tools=
            AVAILABLE_TOOLS,
            user_query=
            user_query,

            previous_vehicle=
            previous_vehicle
        )

        response = (
            await GeminiService
            .generate_response(
                planner_prompt
            )
        )

        try:

            cleaned_response = (
                response
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )

            parsed_response = (
                json.loads(
                    cleaned_response
                )
            )

            print(
                "\nPlanner Decision:"
            )
            print(
                parsed_response
            )

            return parsed_response

        except Exception as e:

            print(
                f"Planner Error: {e}"
            )

            return {
                "use_tool": False,
                "tools": []
            }