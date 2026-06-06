from app.mcp.tools.tool_registry import (
    ToolRegistry
)


class MCPServer:

    @classmethod
    async def execute_tool(
        cls,
        tool_name: str,
        arguments: dict
    ):

        tool = ToolRegistry.get_tool(
            tool_name
        )

        if not tool:
            raise Exception(
                f"Tool not found: "
                f"{tool_name}"
            )

        result = await tool.execute(
            **arguments
        )

        return result