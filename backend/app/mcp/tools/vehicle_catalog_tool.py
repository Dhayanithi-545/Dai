from app.database.mongodb import (
    MongoDB
)


class VehicleCatalogTool:

    async def execute(
        self,
        model_name: str
    ):

        db = MongoDB.get_database()

        vehicle = (
            db.vehicle_catalog
            .find_one({

                "model_name":
                model_name
            })
        )

        if not vehicle:

            return {
                "error":
                "Vehicle model "
                "not found"
            }

        vehicle["_id"] = str(
            vehicle["_id"]
        )

        return vehicle