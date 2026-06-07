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


class MCPPlanner:

    @classmethod
    async def plan(
        cls,
        user_query: str,
        trace=None
    ):

        identity_prompt = (
            load_prompt(
                "identity_prompt.txt"
            )
        )

        planner_prompt = (
            load_prompt(
                "planner_prompt.txt",

                identity_prompt=
                identity_prompt,

                available_tools=
                AVAILABLE_TOOLS,

                user_query=
                user_query
            )
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

            return (
                parsed_response
            )

        except Exception as e:

            print(
                f"Planner Error: {e}"
            )

            return {

                "use_tool":
                False,

                "tools":
                []
            }