AVAILABLE_TOOLS = """

1. vehicle_health_tool
Purpose: Retrieve health diagnostics for a specific vehicle by VIN/vehicle_id.
Use for: battery health, diagnostics, condition, status, overheating, range, temperature.
Arguments: { "vehicle_id": "TN-EV-305" }

2. maintenance_tool
Purpose: Retrieve maintenance history and service details for a vehicle.
Use for: maintenance, service, repair, maintenance due, service history.
Arguments: { "vehicle_id": "TN-EV-305" }

3. telematics_tool
Purpose: Retrieve live telematics telemetry time-series for a vehicle.
Use for: telematics, telemetry, GPS track, speed history, battery drain, motor temperature trend, live vehicle data, driving trace, odometer trace, connectivity status.
Arguments: { "vehicle_id": "TN-DS-545", "minutes": 60 }
Telematics data is currently available for TN-DS-545 (60-minute rolling window).
Returns per-minute: speed, battery %, temperatures, range, GPS, odometer, charging, connectivity, fault codes.

4. vehicle_catalog_tool
Purpose: Retrieve company vehicle model specifications from catalog.
Use for: model specs, top speed, range, category, compare vehicle specifications.
Arguments: { "model_name": "Dhaya Volt" }
For comparisons, call once per model (e.g. Dhaya Volt AND Glide Pro X).

5. fleet_summary_tool
Purpose: Fleet-wide summary counts and optional vehicle lists.
Use for: fleet summary, fleet health overview.
Arguments: { "query_type": null } OR { "query_type": "unhealthy_list" | "maintenance_due_list" | "low_battery" | "overheating" }

6. fleet_analytics_tool
Purpose: Advanced fleet health analytics and operational issue detection.
Use for: unhealthy vehicles list, maintenance due in 30 days, overheating issues, low battery, fleet operational summary.
Arguments: { "query_type": "summary" | "unhealthy" | "maintenance_due_30_days" | "overheating" | "low_battery", "model_name": null }

7. sales_tool
Purpose: Sales data with optional filters.
Use for: sales figures, units sold, revenue, model-wise or city-wise sales.
Arguments: { "model_name": "Dhaya Volt", "city": "Chennai", "period": "yesterday" | "last_month" | "this_month" | "q2" | "last_quarter" | "last_year" | "august" | "september" }
All arguments optional. Use period for time-based queries.

8. production_tool
Purpose: Manufacturing/production statistics with optional filters.
Use for: production numbers, defects, plant efficiency, daily output.
Arguments: { "model_name": "Glide Pro X", "plant": "Chennai Plant", "period": "yesterday" | "last_month" | "q3" | "last_quarter" | "last_6_months" }
All arguments optional.

9. plant_analytics_tool
Purpose: Plant facility details (employees, capacity, status).
Use for: plant details, facility information.
Arguments: { "plant_name": "Chennai Plant" }

10. executive_summary_tool
Purpose: High-level company business overview.
Use for: executive briefing, daily operational report, company summary, business overview.
Arguments: {}

11. analytics_tool
Purpose: Advanced analytics — trends, comparisons, rankings, business performance.
Use for:
- sales_trend: monthly/daily sales trend for a model
- production_trend / manufacturing_trend: production over time
- sales_comparison: compare models (revenue, units)
- plant_comparison: compare Chennai vs Hyderabad production
- city_ranking: top cities for a model
- model_performance: holistic model performance
- business_performance: Q2/Q3 overall business trend
Arguments: {
  "analysis_type": "sales_trend" | "production_trend" | "sales_comparison" | "plant_comparison" | "city_ranking" | "model_performance" | "business_performance" | "manufacturing_trend",
  "model_name": "EV-9 Titan",
  "plant": "Chennai Plant",
  "city": "Chennai",
  "period": "q2" | "last_month" | "yesterday" | "last_quarter" | "last_6_months" | "last_year",
  "compare_models": ["EV-9 Titan", "Dhaya Volt"],
  "compare_plants": ["Chennai Plant", "Hyderabad Plant"]
}

-----------------------------------

MULTI-TOOL ORCHESTRATION RULES:

- "How is EV-9 Titan doing?" → analytics_tool(model_performance) + sales_tool + production_tool
- "Compare Chennai and Hyderabad production" → production_tool(plant=Chennai) + production_tool(plant=Hyderabad) OR analytics_tool(plant_comparison)
- "Compare top speed of Glide Pro X and Dhaya Volt" → vehicle_catalog_tool x2
- "Overall business performance Q2" → analytics_tool(business_performance, period=q2) + executive_summary_tool
- "Fleet health and operational issues" → fleet_analytics_tool(summary) + fleet_analytics_tool(unhealthy) + fleet_analytics_tool(overheating)
- "Diagnostics for VIN X" → vehicle_health_tool + maintenance_tool
- "Telematics for TN-DS-545" / "speed history" / "battery drain last hour" → telematics_tool(vehicle_id=TN-DS-545)
- "Executive briefing Q3" → analytics_tool(business_performance, period=q3) + executive_summary_tool

Models: Dhaya Volt, Glide Pro X, EV-9 Titan
Plants: Chennai Plant, Hyderabad Plant

"""
