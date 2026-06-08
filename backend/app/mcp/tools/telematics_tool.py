from datetime import datetime

from app.database.mongodb import MongoDB
from app.mcp.tools.base_tool import BaseTool


class TelematicsTool(BaseTool):

    name = "telematics_tool"
    description = "Get live telematics telemetry for a vehicle"

    async def execute(
        self,
        vehicle_id: str,
        minutes: int = 60,
    ):
        db = MongoDB.get_database()

        records = list(
            db.vehicle_telematics.find(
                {"vehicle_id": vehicle_id}
            ).sort("timestamp", 1)
        )

        if not records:
            return {
                "error": (
                    f"No telematics data found for vehicle {vehicle_id}. "
                    "Telematics is currently available for TN-DS-545."
                )
            }

        if minutes and minutes < len(records):
            records = records[-minutes:]

        formatted = []
        for record in records:
            ts = record.get("timestamp")
            if isinstance(ts, datetime):
                ts_iso = ts.isoformat()
                ts_label = ts.strftime("%H:%M")
            else:
                ts_iso = str(ts)
                ts_label = ts_iso[-8:-3] if len(ts_iso) >= 8 else ts_iso

            formatted.append({
                "timestamp": ts_iso,
                "time_label": ts_label,
                "speed_kmph": record.get("speed_kmph", 0),
                "battery_percentage": record.get("battery_percentage", 0),
                "battery_temperature": record.get("battery_temperature", 0),
                "motor_temperature": record.get("motor_temperature", 0),
                "range_remaining_km": record.get("range_remaining_km", 0),
                "latitude": record.get("latitude"),
                "longitude": record.get("longitude"),
                "odometer_km": record.get("odometer_km", 0),
                "charging_status": record.get("charging_status", False),
                "connectivity": record.get("connectivity", "unknown"),
                "fault_codes": record.get("fault_codes", []),
            })

        latest = formatted[-1]
        fault_events = sum(
            1 for r in formatted if r.get("fault_codes")
        )
        offline_events = sum(
            1 for r in formatted if r.get("connectivity") == "offline"
        )
        charging_events = sum(
            1 for r in formatted if r.get("charging_status")
        )
        moving_minutes = sum(
            1 for r in formatted if r.get("speed_kmph", 0) > 0
        )

        return {
            "vehicle_id": vehicle_id,
            "record_count": len(formatted),
            "time_range": {
                "start": formatted[0]["timestamp"],
                "end": latest["timestamp"],
                "minutes": len(formatted),
            },
            "summary": {
                "latest_speed_kmph": latest["speed_kmph"],
                "latest_battery_percentage": latest["battery_percentage"],
                "latest_battery_temperature": latest["battery_temperature"],
                "latest_motor_temperature": latest["motor_temperature"],
                "latest_range_km": latest["range_remaining_km"],
                "latest_odometer_km": latest["odometer_km"],
                "latest_connectivity": latest["connectivity"],
                "latest_charging": latest["charging_status"],
                "latest_fault_codes": latest["fault_codes"],
                "avg_speed_kmph": round(
                    sum(r["speed_kmph"] for r in formatted) / len(formatted),
                    1,
                ),
                "min_battery_percentage": min(
                    r["battery_percentage"] for r in formatted
                ),
                "max_motor_temperature": max(
                    r["motor_temperature"] for r in formatted
                ),
                "moving_minutes": moving_minutes,
                "fault_events": fault_events,
                "offline_events": offline_events,
                "charging_events": charging_events,
            },
            "records": formatted,
        }
