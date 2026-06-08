from collections import defaultdict
from datetime import datetime

from app.database.mongodb import MongoDB
from app.utils.date_utils import resolve_period, date_filter


class AnalyticsTool:
    """Unified analytics: trends, comparisons, rankings, business performance."""

    async def execute(
        self,
        analysis_type: str,
        model_name=None,
        plant=None,
        city=None,
        period=None,
        compare_models=None,
        compare_plants=None,
        metric="units_sold",
    ):
        db = MongoDB.get_database()
        start_date, end_date = resolve_period(period) if period else (None, None)

        if analysis_type == "sales_trend":
            return await self._sales_trend(db, model_name, start_date, end_date)

        if analysis_type == "production_trend":
            return await self._production_trend(db, model_name, plant, start_date, end_date)

        if analysis_type == "sales_comparison":
            models = compare_models or ["Dhaya Volt", "Glide Pro X", "EV-9 Titan"]
            return await self._sales_comparison(db, models, start_date, end_date)

        if analysis_type == "plant_comparison":
            plants = compare_plants or ["Chennai Plant", "Hyderabad Plant"]
            return await self._plant_comparison(db, plants, model_name, start_date, end_date)

        if analysis_type == "city_ranking":
            return await self._city_ranking(db, model_name, start_date, end_date, limit=3)

        if analysis_type == "model_performance":
            return await self._model_performance(db, model_name, start_date, end_date)

        if analysis_type == "business_performance":
            return await self._business_performance(db, start_date, end_date)

        if analysis_type == "manufacturing_trend":
            return await self._production_trend(db, model_name, plant, start_date, end_date)

        return {"error": f"Unknown analysis_type: {analysis_type}"}

    async def _sales_trend(self, db, model_name, start_date, end_date):
        query = date_filter(start_date, end_date)
        if model_name:
            query["model"] = model_name

        records = list(db.sales_data.find(query).sort("date", 1))
        daily = defaultdict(lambda: {"units": 0, "revenue": 0})

        for r in records:
            day = r["date"].strftime("%Y-%m-%d") if isinstance(r["date"], datetime) else str(r["date"])[:10]
            daily[day]["units"] += r["units_sold"]
            daily[day]["revenue"] += r["revenue"]

        series = [{"date": d, **v} for d, v in sorted(daily.items())]
        return {
            "analysis_type": "sales_trend",
            "model": model_name,
            "series": series,
            "total_units": sum(p["units"] for p in series),
            "total_revenue": sum(p["revenue"] for p in series),
        }

    async def _production_trend(self, db, model_name, plant, start_date, end_date):
        query = date_filter(start_date, end_date)
        if model_name:
            query["model"] = model_name
        if plant:
            query["plant"] = plant

        records = list(db.manufacturing_data.find(query).sort("date", 1))
        daily = defaultdict(lambda: {"produced": 0, "defects": 0, "efficiency_sum": 0, "count": 0})

        for r in records:
            day = r["date"].strftime("%Y-%m-%d") if isinstance(r["date"], datetime) else str(r["date"])[:10]
            daily[day]["produced"] += r["produced_count"]
            daily[day]["defects"] += r["defect_count"]
            daily[day]["efficiency_sum"] += r["efficiency"]
            daily[day]["count"] += 1

        series = []
        for d, v in sorted(daily.items()):
            series.append({
                "date": d,
                "produced": v["produced"],
                "defects": v["defects"],
                "avg_efficiency": round(v["efficiency_sum"] / max(v["count"], 1), 2),
            })

        return {
            "analysis_type": "production_trend",
            "model": model_name,
            "plant": plant,
            "series": series,
            "total_produced": sum(p["produced"] for p in series),
            "total_defects": sum(p["defects"] for p in series),
        }

    async def _sales_comparison(self, db, models, start_date, end_date):
        query = date_filter(start_date, end_date)
        comparison = []

        for model in models:
            q = {**query, "model": model}
            records = list(db.sales_data.find(q))
            comparison.append({
                "model": model,
                "units_sold": sum(r["units_sold"] for r in records),
                "revenue": sum(r["revenue"] for r in records),
            })

        return {
            "analysis_type": "sales_comparison",
            "comparison": comparison,
            "period": {"start": str(start_date), "end": str(end_date)},
        }

    async def _plant_comparison(self, db, plants, model_name, start_date, end_date):
        query = date_filter(start_date, end_date)
        if model_name:
            query["model"] = model_name

        comparison = []
        for plant in plants:
            q = {**query, "plant": plant}
            records = list(db.manufacturing_data.find(q))
            comparison.append({
                "plant": plant,
                "total_produced": sum(r["produced_count"] for r in records),
                "defects": sum(r["defect_count"] for r in records),
                "avg_efficiency": round(
                    sum(r["efficiency"] for r in records) / max(len(records), 1), 2
                ),
            })

        return {
            "analysis_type": "plant_comparison",
            "model": model_name,
            "comparison": comparison,
        }

    async def _city_ranking(self, db, model_name, start_date, end_date, limit=3):
        query = date_filter(start_date, end_date)
        if model_name:
            query["model"] = model_name

        records = list(db.sales_data.find(query))
        by_city = defaultdict(lambda: {"units": 0, "revenue": 0})

        for r in records:
            by_city[r["city"]]["units"] += r["units_sold"]
            by_city[r["city"]]["revenue"] += r["revenue"]

        ranking = sorted(
            [{"city": c, **v} for c, v in by_city.items()],
            key=lambda x: x["units"],
            reverse=True,
        )[:limit]

        return {
            "analysis_type": "city_ranking",
            "model": model_name,
            "ranking": ranking,
        }

    async def _model_performance(self, db, model_name, start_date, end_date):
        sales_q = date_filter(start_date, end_date)
        prod_q = date_filter(start_date, end_date)
        if model_name:
            sales_q["model"] = model_name
            prod_q["model"] = model_name

        sales = list(db.sales_data.find(sales_q))
        production = list(db.manufacturing_data.find(prod_q))

        return {
            "analysis_type": "model_performance",
            "model": model_name,
            "units_sold": sum(s["units_sold"] for s in sales),
            "revenue": sum(s["revenue"] for s in sales),
            "total_produced": sum(p["produced_count"] for p in production),
            "defects": sum(p["defect_count"] for p in production),
            "avg_efficiency": round(
                sum(p["efficiency"] for p in production) / max(len(production), 1), 2
            ),
        }

    async def _business_performance(self, db, start_date, end_date):
        sales_q = date_filter(start_date, end_date)
        prod_q = date_filter(start_date, end_date)

        sales = list(db.sales_data.find(sales_q))
        production = list(db.manufacturing_data.find(prod_q))
        fleet_total = db.vehicles.count_documents({})
        maintenance_due = db.vehicles.count_documents({"maintenance_due": True})

        return {
            "analysis_type": "business_performance",
            "total_sales_units": sum(s["units_sold"] for s in sales),
            "total_revenue": sum(s["revenue"] for s in sales),
            "total_produced": sum(p["produced_count"] for p in production),
            "total_defects": sum(p["defect_count"] for p in production),
            "avg_plant_efficiency": round(
                sum(p["efficiency"] for p in production) / max(len(production), 1), 2
            ),
            "fleet_size": fleet_total,
            "maintenance_due": maintenance_due,
        }
