from app.database.mongodb import (
    MongoDB
)


class PlantAnalyticsTool:

    async def execute(
        self,
        plant_name: str
    ):

        db = (
            MongoDB
            .get_database()
        )

        plant = (
            db.plants
            .find_one({

                "plant_name":
                plant_name
            })
        )

        if not plant:

            return {
                "error":
                "Plant not found"
            }

        return {

            "plant_name":
            plant[
                "plant_name"
            ],

            "employees":
            plant[
                "employees"
            ],

            "capacity":
            plant[
                "daily_capacity"
            ],

            "status":
            plant[
                "status"
            ]
        }