from app.mcp.tools.vehicle_health_tool import (
    VehicleHealthTool
)


class ToolRegistry:

    tools = {
        "vehicle_health_tool":
        VehicleHealthTool()
    }

    @classmethod
    def get_tool(
        cls,
        tool_name: str
    ):
        return cls.tools.get(tool_name)