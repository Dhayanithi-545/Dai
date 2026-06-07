from datetime import (
    datetime
)

from app.database.mongodb import (
    MongoDB
)


class SalesTool:

    async def execute(
        self,
        model_name=None
    ):

        db = (
            MongoDB
            .get_database()
        )

        today = (
            datetime.now()
            .date()
        )

        query = {}

        if model_name:

            query[
                "model"
            ] = model_name

        sales = list(

            db.sales_data
            .find(query)
        )

        total_units = sum(
            sale[
                "units_sold"
            ]
            for sale in sales
        )

        total_revenue = sum(
            sale[
                "revenue"
            ]
            for sale in sales
        )

        return {

            "model":
            model_name,

            "units_sold":
            total_units,

            "revenue":
            total_revenue
        }