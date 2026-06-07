AVAILABLE_TOOLS = """

1. vehicle_health_tool

Purpose:
Retrieve health diagnostics
for a vehicle.

Use when user asks:

- vehicle health
- battery health
- diagnostics
- condition
- status
- battery condition
- overheating
- range
- temperature

Arguments:

{
    "vehicle_id":
    "TN-EV-305"
}

-----------------------------------

2. maintenance_tool

Purpose:
Retrieve maintenance
details.

Use when user asks:

- maintenance
- service
- repair
- maintenance due
- service history

Arguments:

{
    "vehicle_id":
    "TN-EV-305"
}

-----------------------------------

3. vehicle_catalog_tool

Purpose:
Retrieve company vehicle
model information.

Use when user asks:

- Tell me about Dhaya Volt
- vehicle specs
- compare vehicles
- top speed
- range
- category
- model details

Arguments:

{
    "model_name":
    "Dhaya Volt"
}

-----------------------------------

4. fleet_summary_tool

Purpose:
Get overall fleet summary.

Use when user asks:

- unhealthy vehicles
- critical vehicles
- fleet summary
- maintenance due vehicles
- fleet health

Arguments:

{}

-----------------------------------

5. sales_tool

Purpose:
Get sales information.

Use when user asks:

- sales report
- units sold
- revenue
- best selling vehicle
- sales summary

Arguments:

{
    "model_name":
    "Dhaya Volt"
}

model_name optional

-----------------------------------

6. production_tool

Purpose:
Retrieve manufacturing
statistics.

Use when user asks:

- production
- manufacturing
- plant production
- defects
- efficiency

Arguments:

{
    "model_name":
    "EV-9 Titan",

    "plant":
    "Chennai Plant"
}

Both optional

-----------------------------------

7. plant_analytics_tool

Purpose:
Retrieve plant details.

Use when user asks:

- plant details
- Chennai plant
- Hyderabad plant
- plant analytics

Arguments:

{
    "plant_name":
    "Chennai Plant"
}

-----------------------------------

8. executive_summary_tool

Purpose:
Generate company summary.

Use when user asks:

- executive summary
- company report
- business overview
- performance report
- daily summary

Arguments:

{}

"""