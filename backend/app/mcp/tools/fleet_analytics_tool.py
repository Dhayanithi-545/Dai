from datetime import datetime, timedelta

from app.database.mongodb import MongoDB


class FleetAnalyticsTool:
    """Detailed fleet health analytics and operational issue detection."""

    async def execute(self, query_type="summary", model_name=None):
        db = MongoDB.get_database()
        base_filter = {}
        if model_name:
            base_filter["model_name"] = model_name

        if query_type == "unhealthy":
            vehicles = list(
                db.vehicles.find(
                    {**base_filter, "status": {"$in": ["Critical", "Needs Attention"]}},
                    {"_id": 0},
                ).limit(50)
            )
            return {
                "query_type": query_type,
                "count": len(vehicles),
                "vehicles": vehicles,
            }

        if query_type == "maintenance_due_30_days":
            cutoff = datetime.now() + timedelta(days=30)
            vehicles = list(
                db.vehicles.find(
                    {**base_filter, "maintenance_due": True},
                    {"_id": 0, "vehicle_id": 1, "model_name": 1,
                     "last_service_date": 1, "maintenance_notes": 1},
                ).limit(50)
            )
            return {
                "query_type": query_type,
                "count": len(vehicles),
                "vehicles": vehicles,
                "note": "Vehicles flagged for scheduled maintenance within 30 days",
            }

        if query_type == "overheating":
            vehicles = list(
                db.vehicles.find(
                    {**base_filter, "temperature": {"$gt": 40}},
                    {"_id": 0, "vehicle_id": 1, "model_name": 1,
                     "temperature": 1, "status": 1},
                ).limit(50)
            )
            return {
                "query_type": query_type,
                "count": len(vehicles),
                "vehicles": vehicles,
            }

        if query_type == "low_battery":
            vehicles = list(
                db.vehicles.find(
                    {**base_filter, "battery_health": {"$lt": 20}},
                    {"_id": 0, "vehicle_id": 1, "model_name": 1, "battery_health": 1},
                ).limit(50)
            )
            return {
                "query_type": query_type,
                "count": len(vehicles),
                "vehicles": vehicles,
            }

        # summary
        total = db.vehicles.count_documents(base_filter)
        return {
            "query_type": "summary",
            "total_vehicles": total,
            "healthy": db.vehicles.count_documents({**base_filter, "status": "Healthy"}),
            "critical": db.vehicles.count_documents({**base_filter, "status": "Critical"}),
            "needs_attention": db.vehicles.count_documents(
                {**base_filter, "status": "Needs Attention"}
            ),
            "maintenance_due": db.vehicles.count_documents(
                {**base_filter, "maintenance_due": True}
            ),
            "overheating": db.vehicles.count_documents(
                {**base_filter, "temperature": {"$gt": 40}}
            ),
            "low_battery": db.vehicles.count_documents(
                {**base_filter, "battery_health": {"$lt": 20}}
            ),
        }
