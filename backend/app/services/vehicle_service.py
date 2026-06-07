from app.database.mongodb import (
    MongoDB
)


class VehicleService:

    @classmethod
    async def get_vehicle(
        cls,
        vehicle_id: str
    ):

        db = MongoDB.get_database()

        vehicle = db.vehicles.find_one({
            "vehicle_id": vehicle_id
        })

        return vehicle