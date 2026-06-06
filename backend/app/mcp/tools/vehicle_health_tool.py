from app.mcp.tools.base_tool import (
    BaseTool
)


class VehicleHealthTool(BaseTool):

    name = "vehicle_health_tool"

    description = (
        "Get health information "
        "about an EV vehicle"
    )

    async def execute(
        self,
        vehicle_id: str
    ):

        # fake data for now
        return {
            "vehicle_id": vehicle_id,
            "battery_health": "92%",
            "status": "Healthy",
            "temperature": "34°C"
        }