"""Rule-based visualization widget generation from tool outputs."""


class VisualizationService:

    @classmethod
    def generate_widgets(cls, tool_outputs: list, plan: dict) -> list:
        widgets = []
        intent = plan.get("intent", "lookup")
        viz_hint = plan.get("visualization_hint")

        catalog_rows = [
            o["result"]
            for o in tool_outputs
            if o.get("tool_name") == "vehicle_catalog_tool"
            and o.get("result") and not o["result"].get("error")
        ]
        if len(catalog_rows) >= 2:
            widgets.append({
                "type": "table",
                "title": "Vehicle Specification Comparison",
                "columns": ["model_name", "category", "range_km", "top_speed", "price"],
                "rows": catalog_rows,
            })

        for output in tool_outputs:
            if output.get("error"):
                continue

            result = output.get("result", {})
            tool_name = output.get("tool_name", "")

            if tool_name == "vehicle_catalog_tool" and len(catalog_rows) >= 2:
                continue

            widgets.extend(cls._widgets_from_result(tool_name, result, intent, viz_hint))

        return cls._dedupe_widgets(widgets)

    @classmethod
    def _widgets_from_result(cls, tool_name, result, intent, viz_hint):
        widgets = []

        if tool_name == "analytics_tool":
            atype = result.get("analysis_type", "")

            if atype in ("sales_trend", "production_trend", "manufacturing_trend"):
                series = result.get("series", [])
                if series:
                    key = "units" if "units" in series[0] else "produced"
                    widgets.append({
                        "type": "line_chart",
                        "title": f"{atype.replace('_', ' ').title()}",
                        "data": [
                            {"name": p["date"], "value": p.get(key, p.get("produced", 0))}
                            for p in series
                        ],
                        "xKey": "name",
                        "yKey": "value",
                    })

            if atype in ("sales_comparison", "plant_comparison"):
                comp = result.get("comparison", [])
                if comp:
                    label_key = "model" if "model" in comp[0] else "plant"
                    value_key = "units_sold" if "units_sold" in comp[0] else "total_produced"
                    widgets.append({
                        "type": "bar_chart",
                        "title": atype.replace("_", " ").title(),
                        "data": [
                            {"name": c[label_key], "value": c.get(value_key, 0)}
                            for c in comp
                        ],
                        "xKey": "name",
                        "yKey": "value",
                    })
                    if any("revenue" in c for c in comp):
                        widgets.append({
                            "type": "bar_chart",
                            "title": "Revenue Comparison",
                            "data": [
                                {"name": c[label_key], "value": c.get("revenue", 0)}
                                for c in comp
                            ],
                            "xKey": "name",
                            "yKey": "value",
                        })

            if atype == "city_ranking":
                ranking = result.get("ranking", [])
                if ranking:
                    widgets.append({
                        "type": "bar_chart",
                        "title": "Top Cities by Sales",
                        "data": [
                            {"name": r["city"], "value": r["units"]}
                            for r in ranking
                        ],
                        "xKey": "name",
                        "yKey": "value",
                    })

            if atype == "business_performance":
                widgets.extend(cls._kpi_widgets([
                    ("Total Sales Units", result.get("total_sales_units", 0)),
                    ("Total Revenue", f"₹{result.get('total_revenue', 0):,}"),
                    ("Total Produced", result.get("total_produced", 0)),
                    ("Fleet Size", result.get("fleet_size", 0)),
                    ("Avg Efficiency", f"{result.get('avg_plant_efficiency', 0)}%"),
                ]))

        if tool_name == "sales_tool":
            if result.get("by_model") and (intent in ("comparison", "analytics") or viz_hint == "bar_chart"):
                widgets.append({
                    "type": "bar_chart",
                    "title": "Sales by Model",
                    "data": [
                        {"name": k, "value": v}
                        for k, v in result["by_model"].items()
                    ],
                    "xKey": "name",
                    "yKey": "value",
                })
            if result.get("by_city"):
                widgets.append({
                    "type": "pie_chart",
                    "title": "Sales Distribution by City",
                    "data": [
                        {"name": k, "value": v}
                        for k, v in result["by_city"].items()
                    ],
                })
            widgets.extend(cls._kpi_widgets([
                ("Units Sold", result.get("units_sold", 0)),
                ("Revenue", f"₹{result.get('revenue', 0):,}"),
            ]))

        if tool_name == "production_tool":
            if result.get("by_plant") and intent in ("comparison", "analytics", "plant_comparison"):
                widgets.append({
                    "type": "bar_chart",
                    "title": "Production by Plant",
                    "data": [
                        {"name": k, "value": v}
                        for k, v in result["by_plant"].items()
                    ],
                    "xKey": "name",
                    "yKey": "value",
                })
            widgets.extend(cls._kpi_widgets([
                ("Total Produced", result.get("total_produced", 0)),
                ("Defects", result.get("defects", 0)),
                ("Avg Efficiency", f"{result.get('avg_efficiency', 0)}%"),
            ]))

        if tool_name in ("fleet_summary_tool", "fleet_analytics_tool"):
            widgets.extend(cls._kpi_widgets([
                ("Total Vehicles", result.get("total_vehicles", 0)),
                ("Healthy", result.get("healthy", 0)),
                ("Critical", result.get("critical", 0)),
                ("Maintenance Due", result.get("maintenance_due", 0)),
            ]))
            vehicles = result.get("vehicles", [])
            if vehicles:
                widgets.append({
                    "type": "table",
                    "title": "Fleet Details",
                    "columns": list(vehicles[0].keys()),
                    "rows": vehicles[:20],
                })

        if tool_name == "executive_summary_tool":
            widgets.extend(cls._kpi_widgets([
                ("Fleet Size", result.get("fleet_size", 0)),
                ("Maintenance Due", result.get("maintenance_due", 0)),
                ("Total Sales", result.get("total_sales", 0)),
                ("Revenue", f"₹{result.get('revenue', 0):,}"),
            ]))

        if tool_name == "vehicle_catalog_tool" and intent == "comparison":
            widgets.append({
                "type": "table",
                "title": "Vehicle Specifications",
                "columns": ["model_name", "category", "range_km", "top_speed", "price"],
                "rows": [result] if isinstance(result, dict) else result,
            })

        if tool_name == "telematics_tool":
            widgets.extend(cls._telematics_widgets(result))

        return widgets

    @classmethod
    def _telematics_widgets(cls, result):
        widgets = []
        summary = result.get("summary", {})
        records = result.get("records", [])
        vehicle_id = result.get("vehicle_id", "")

        if not records:
            return widgets

        widgets.extend(cls._kpi_widgets([
            ("Speed", f"{summary.get('latest_speed_kmph', 0)} km/h"),
            ("Battery", f"{summary.get('latest_battery_percentage', 0)}%"),
            ("Range", f"{summary.get('latest_range_km', 0)} km"),
            ("Motor Temp", f"{summary.get('latest_motor_temperature', 0)}°C"),
            ("Connectivity", summary.get("latest_connectivity", "—")),
        ]))

        chart_data = [
            {
                "time": r["time_label"],
                "speed": r["speed_kmph"],
                "battery": r["battery_percentage"],
            }
            for r in records
        ]
        widgets.append({
            "type": "telematics_chart",
            "title": f"Telemetry — {vehicle_id} (Last {len(records)} min)",
            "data": chart_data,
        })

        widgets.append({
            "type": "temperature_chart",
            "title": "Temperature Trend",
            "data": [
                {
                    "time": r["time_label"],
                    "motor_temp": r["motor_temperature"],
                    "battery_temp": r["battery_temperature"],
                }
                for r in records
            ],
        })

        table_rows = [
            {
                "time": r["time_label"],
                "speed_kmph": r["speed_kmph"],
                "battery_%": r["battery_percentage"],
                "motor_temp": r["motor_temperature"],
                "range_km": r["range_remaining_km"],
                "charging": "Yes" if r["charging_status"] else "No",
                "status": r["connectivity"],
                "faults": ", ".join(r["fault_codes"]) or "—",
            }
            for r in records[-15:]
        ]
        widgets.append({
            "type": "table",
            "title": "Recent Telemetry Records",
            "columns": list(table_rows[0].keys()),
            "rows": table_rows,
        })

        return widgets

    @classmethod
    def _kpi_widgets(cls, items):
        return [
            {"type": "kpi", "title": title, "value": str(value)}
            for title, value in items
        ]

    @classmethod
    def _dedupe_widgets(cls, widgets):
        seen = set()
        unique = []
        for w in widgets:
            key = (w.get("type"), w.get("title"))
            if key not in seen:
                seen.add(key)
                unique.append(w)
        return unique[:12]

    @classmethod
    def generate_insights(cls, tool_outputs: list, plan: dict) -> list:
        insights = []
        intent = plan.get("intent", "")

        for output in tool_outputs:
            result = output.get("result", {})
            if result.get("error"):
                continue

            if result.get("analysis_type") == "plant_comparison":
                comp = result.get("comparison", [])
                if len(comp) >= 2:
                    best = max(comp, key=lambda x: x.get("total_produced", 0))
                    insights.append(
                        f"{best['plant']} leads production with "
                        f"{best['total_produced']} units."
                    )

            if result.get("analysis_type") == "sales_comparison":
                comp = result.get("comparison", [])
                if comp:
                    top = max(comp, key=lambda x: x.get("units_sold", 0))
                    insights.append(
                        f"{top['model']} is the top seller with "
                        f"{top['units_sold']} units."
                    )

            if result.get("critical", 0) > 0:
                insights.append(
                    f"{result['critical']} vehicles are in critical condition."
                )

            if output.get("tool_name") == "telematics_tool":
                summary = result.get("summary", {})
                if summary.get("fault_events", 0) > 0:
                    insights.append(
                        f"{summary['fault_events']} fault events detected in the "
                        f"last {result.get('record_count', 0)} minutes."
                    )
                if summary.get("offline_events", 0) > 0:
                    insights.append(
                        f"Vehicle went offline {summary['offline_events']} time(s) "
                        "during the telemetry window."
                    )
                if summary.get("latest_fault_codes"):
                    insights.append(
                        f"Active fault codes: "
                        f"{', '.join(summary['latest_fault_codes'])}."
                    )
                if summary.get("min_battery_percentage", 100) < 40:
                    insights.append(
                        f"Battery dropped to "
                        f"{summary['min_battery_percentage']}% — monitor charging."
                    )

        if intent == "comparison" and not insights:
            insights.append("Comparison data retrieved — see charts for details.")

        return insights[:5]
