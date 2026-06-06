class MCPPlanner:

    @classmethod
    async def plan(
        cls,
        user_query: str
    ):

        query = user_query.lower()

        if "health" in query:

            return {
                "use_tool": True,
                "tool_name":
                "vehicle_health_tool",
                "arguments": {
                    "vehicle_id":
                    "TN-EV-204"
                }
            }

        return {
            "use_tool": False
        }