from app.mcp.tools.base_tool import (
    BaseTool
)

from app.mcp.resources.vehicle_resource import (
    VehicleResource
)


class VehicleHealthTool(BaseTool):

    name = "vehicle_health_tool"

    description = "Get EV vehicle health"
    
    async def execute(
        self,
        vehicle_id: str
    ):

        vehicle = await VehicleResource.get_vehicle(vehicle_id)
        
        if not vehicle:

            return {
                "error":
                "Vehicle not found"
            }

        return {
            "vehicle_id":
            vehicle["vehicle_id"],

            "battery_health":
            vehicle[
                "battery_health"
            ],

            "temperature":
            vehicle[
                "temperature"
            ],

            "status":
            vehicle["status"],

            "range_km":
            vehicle["range_km"],

            "maintenance_due":
            vehicle[
                "maintenance_due"
            ]
        }