from app.database.mongodb import (
    MongoDB
)


class FleetSummaryTool:

    async def execute(
        self
    ):

        db = (
            MongoDB
            .get_database()
        )

        total = (
            db.vehicles
            .count_documents({})
        )

        healthy = (
            db.vehicles
            .count_documents({
                "status":
                "Healthy"
            })
        )

        critical = (
            db.vehicles
            .count_documents({
                "status":
                "Critical"
            })
        )

        maintenance_due = (
            db.vehicles
            .count_documents({
                "maintenance_due":
                True
            })
        )

        return {

            "total_vehicles":
            total,

            "healthy":
            healthy,

            "critical":
            critical,

            "maintenance_due":
            maintenance_due
        }