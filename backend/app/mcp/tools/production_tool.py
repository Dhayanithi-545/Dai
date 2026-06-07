from app.database.mongodb import (
    MongoDB
)


class ProductionTool:

    async def execute(
        self,
        model_name=None,
        plant=None
    ):

        db = (
            MongoDB
            .get_database()
        )

        query = {}

        if model_name:

            query[
                "model"
            ] = model_name

        if plant:

            query[
                "plant"
            ] = plant

        records = list(

            db.manufacturing_data
            .find(query)
        )

        total = sum(

            record[
                "produced_count"
            ]

            for record
            in records
        )

        defects = sum(

            record[
                "defect_count"
            ]

            for record
            in records
        )

        avg_efficiency = round(

            sum(
                record[
                    "efficiency"
                ]
                for record
                in records
            )

            / max(
                len(records),
                1
            ),

            2
        )

        return {

            "total_produced":
            total,

            "defects":
            defects,

            "avg_efficiency":
            avg_efficiency
        }