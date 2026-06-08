from app.database.mongodb import MongoDB
from app.utils.date_utils import resolve_period, date_filter


class ProductionTool:

    async def execute(
        self,
        model_name=None,
        plant=None,
        period=None,
        start_date=None,
        end_date=None,
    ):
        db = MongoDB.get_database()
        query = {}

        if model_name:
            query["model"] = model_name
        if plant:
            query["plant"] = plant

        if period and not start_date:
            start_date, end_date = resolve_period(period)

        query.update(date_filter(start_date, end_date))

        records = list(db.manufacturing_data.find(query))

        total = sum(r["produced_count"] for r in records)
        defects = sum(r["defect_count"] for r in records)
        avg_efficiency = round(
            sum(r["efficiency"] for r in records) / max(len(records), 1),
            2,
        )

        by_plant = {}
        by_model = {}
        for r in records:
            by_plant[r["plant"]] = by_plant.get(r["plant"], 0) + r["produced_count"]
            by_model[r["model"]] = by_model.get(r["model"], 0) + r["produced_count"]

        return {
            "model": model_name,
            "plant": plant,
            "period": period,
            "total_produced": total,
            "defects": defects,
            "avg_efficiency": avg_efficiency,
            "by_plant": by_plant,
            "by_model": by_model,
            "record_count": len(records),
        }
