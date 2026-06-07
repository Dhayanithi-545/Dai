from app.mcp.tools.vehicle_health_tool import (
    VehicleHealthTool
)

from app.mcp.tools.maintenance_tool import (
    MaintenanceTool
)


class ToolRegistry:

    tools = {

        "vehicle_health_tool":
        VehicleHealthTool(),

        "maintenance_tool":
        MaintenanceTool()
    }

    @classmethod
    def get_tool(
        cls,
        tool_name: str
    ):
        return cls.tools.get(
            tool_name
        )