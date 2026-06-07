from app.mcp.server.mcp_server import (
    MCPServer
)




class MCPClient:

    @classmethod
    async def call_tool(
        cls,
        tool_name: str,
        arguments: dict
    ):

        result = await MCPServer.execute_tool(
            tool_name,
            arguments
        )

        return result