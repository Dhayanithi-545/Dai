from datetime import datetime

from app.database.mongodb import MongoDB
from app.utils.date_utils import resolve_period, date_filter


class SalesTool:

    async def execute(
        self,
        model_name=None,
        city=None,
        period=None,
        start_date=None,
        end_date=None,
    ):
        db = MongoDB.get_database()
        query = {}

        if model_name:
            query["model"] = model_name
        if city:
            query["city"] = city

        if period and not start_date:
            start_date, end_date = resolve_period(period)

        query.update(date_filter(start_date, end_date))

        sales = list(db.sales_data.find(query))

        total_units = sum(s["units_sold"] for s in sales)
        total_revenue = sum(s["revenue"] for s in sales)

        by_model = {}
        by_city = {}
        for s in sales:
            by_model[s["model"]] = by_model.get(s["model"], 0) + s["units_sold"]
            by_city[s["city"]] = by_city.get(s["city"], 0) + s["units_sold"]

        return {
            "model": model_name,
            "city": city,
            "period": period,
            "units_sold": total_units,
            "revenue": total_revenue,
            "by_model": by_model,
            "by_city": by_city,
            "record_count": len(sales),
        }
