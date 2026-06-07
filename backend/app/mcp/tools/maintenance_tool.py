from app.mcp.tools.base_tool import (
    BaseTool
)

from app.mcp.resources.vehicle_resource import (
    VehicleResource
)


class MaintenanceTool(
    BaseTool
):

    name = "maintenance_tool"

    description = (
        "Get maintenance "
        "details of a vehicle"
    )

    async def execute(
        self,
        vehicle_id: str
    ):

        vehicle = (
            await VehicleResource
            .get_vehicle(
                vehicle_id
            )
        )

        if not vehicle:

            return {
                "error":
                "Vehicle not found"
            }

        return {
            "vehicle_id":
            vehicle["vehicle_id"],

            "maintenance_due":
            vehicle[
                "maintenance_due"
            ],

            "last_service_date":
            vehicle[
                "last_service_date"
            ],

            "maintenance_notes":
            vehicle[
                "maintenance_notes"
            ]
        }