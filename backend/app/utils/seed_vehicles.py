from app.database.mongodb import (
    MongoDB
)


def seed_vehicles():

    db = MongoDB.get_database()

    db.vehicles.delete_many({})

    vehicles = [
        {
            "vehicle_id": "TN-EV-204",
            "battery_health": 92,
            "temperature": 34,
            "status": "Healthy",
            "range_km": 180,
            "maintenance_due": False,
            "last_service_date":
            "2026-05-10",
            "maintenance_notes":
            "No issues"
        },
        {
            "vehicle_id": "TN-EV-305",
            "battery_health": 71,
            "temperature": 41,
            "status":
            "Needs Attention",
            "range_km": 120,
            "maintenance_due": True,
            "last_service_date":
            "2026-02-15",
            "maintenance_notes":
            "Battery overheating"
        }
    ]

    db.vehicles.insert_many(
        vehicles
    )

    print(
        "Vehicles inserted successfully"
    )