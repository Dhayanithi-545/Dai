from datetime import datetime, timedelta

from app.database.mongodb import MongoDB


class FleetSummaryTool:

    async def execute(self, query_type=None):
        db = MongoDB.get_database()

        total = db.vehicles.count_documents({})
        healthy = db.vehicles.count_documents({"status": "Healthy"})
        critical = db.vehicles.count_documents({"status": "Critical"})
        needs_attention = db.vehicles.count_documents({"status": "Needs Attention"})
        maintenance_due = db.vehicles.count_documents({"maintenance_due": True})

        result = {
            "total_vehicles": total,
            "healthy": healthy,
            "critical": critical,
            "needs_attention": needs_attention,
            "maintenance_due": maintenance_due,
        }

        if query_type == "unhealthy_list":
            vehicles = list(
                db.vehicles.find(
                    {"status": {"$in": ["Critical", "Needs Attention"]}},
                    {"_id": 0, "vehicle_id": 1, "model_name": 1, "status": 1,
                     "battery_health": 1, "temperature": 1},
                ).limit(50)
            )
            result["vehicles"] = vehicles

        elif query_type == "maintenance_due_list":
            vehicles = list(
                db.vehicles.find(
                    {"maintenance_due": True},
                    {"_id": 0, "vehicle_id": 1, "model_name": 1,
                     "last_service_date": 1, "maintenance_notes": 1},
                ).limit(50)
            )
            result["vehicles"] = vehicles

        elif query_type == "low_battery":
            vehicles = list(
                db.vehicles.find(
                    {"battery_health": {"$lt": 20}},
                    {"_id": 0, "vehicle_id": 1, "model_name": 1, "battery_health": 1},
                ).limit(50)
            )
            result["vehicles"] = vehicles
            result["count"] = len(vehicles)

        elif query_type == "overheating":
            vehicles = list(
                db.vehicles.find(
                    {"temperature": {"$gt": 40}},
                    {"_id": 0, "vehicle_id": 1, "model_name": 1, "temperature": 1},
                ).limit(50)
            )
            result["vehicles"] = vehicles
            result["count"] = len(vehicles)

        return result
