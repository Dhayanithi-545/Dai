from app.database.mongodb import (
    MongoDB
)


class ExecutiveSummaryTool:

    async def execute(
        self
    ):

        db = (
            MongoDB
            .get_database()
        )

        vehicles = (
            db.vehicles
            .count_documents({})
        )

        maintenance_due = (
            db.vehicles
            .count_documents({
                "maintenance_due":
                True
            })
        )

        sales = list(
            db.sales_data.find()
        )

        total_sales = sum(
            sale[
                "units_sold"
            ]
            for sale
            in sales
        )

        revenue = sum(
            sale[
                "revenue"
            ]
            for sale
            in sales
        )

        return {

            "fleet_size":
            vehicles,

            "maintenance_due":
            maintenance_due,

            "total_sales":
            total_sales,

            "revenue":
            revenue
        }