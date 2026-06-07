from app.services.vehicle_service import (
    VehicleService
)


class VehicleResource:

    @classmethod
    async def get_vehicle(
        cls,
        vehicle_id: str
    ):

        vehicle = (
            await VehicleService
            .get_vehicle(
                vehicle_id
            )
        )

        if not vehicle:
            return None

        vehicle.pop("_id", None)

        return vehicle