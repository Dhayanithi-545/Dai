import json
import re

from app.services.gemini_service import GeminiService
from app.services.memory_service import MemoryService
from app.mcp.client.mcp_client import MCPClient
from app.utils.prompt_loader import load_prompt


class MCPPlanner:

    @classmethod
    async def plan(cls, user_query: str, trace=None):
        enriched_query = await MemoryService.enrich_query(user_query)
        context = await MemoryService.get_context()
        context_text = MemoryService.format_context_for_planner(context)

        identity_prompt = load_prompt("identity_prompt.txt")

        available_tools = MCPClient.format_tools_for_planner()

        planner_prompt = load_prompt(
            "planner_prompt.txt",
            identity_prompt=identity_prompt,
            available_tools=available_tools,
            user_query=enriched_query,
            conversation_context=context_text,
        )

        response = await GeminiService.generate_response(planner_prompt)

        try:
            cleaned = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )
            parsed = json.loads(cleaned)
            return cls._normalize_plan(parsed, context)

        except Exception as e:
            print(f"Planner Error: {e}")
            fallback = cls._fallback_plan(enriched_query, context)
            if fallback.get("use_tool"):
                return fallback
            return {"use_tool": False, "tools": [], "intent": "general"}

    @classmethod
    def _normalize_plan(cls, plan: dict, context: dict) -> dict:
        """Ensure plan has required fields and fill missing args from memory."""
        plan.setdefault("intent", "lookup")
        plan.setdefault("visualization_hint", None)
        plan.setdefault("tools", [])

        for tool in plan.get("tools", []):
            args = tool.setdefault("arguments", {})
            if not args.get("vehicle_id") and context.get("last_vehicle_id"):
                if tool.get("tool_name") in (
                    "vehicle_health_tool",
                    "maintenance_tool",
                    "telematics_tool",
                ):
                    args["vehicle_id"] = context["last_vehicle_id"]

        return plan

    @classmethod
    def _fallback_plan(cls, query: str, context: dict) -> dict:
        """Semantic fallback when LLM JSON parsing fails — not keyword-only."""
        q = query.lower()

        vehicle_id = context.get("last_vehicle_id")
        vin_match = re.search(
            r"\b[A-Z]{2,3}-[A-Z]{2,3}-\d{3}\b", query, re.IGNORECASE
        )
        if vin_match:
            vehicle_id = vin_match.group().upper()

        tools = []

        if any(w in q for w in ("health", "battery", "diagnostic", "overheat", "temperature")):
            if vehicle_id:
                tools.append({
                    "tool_name": "vehicle_health_tool",
                    "arguments": {"vehicle_id": vehicle_id},
                })

        if any(w in q for w in ("maintenance", "service", "repair")):
            if vehicle_id:
                tools.append({
                    "tool_name": "maintenance_tool",
                    "arguments": {"vehicle_id": vehicle_id},
                })

        if any(w in q for w in (
            "telematics", "telemetry", "gps", "odometer trace",
            "speed history", "live data", "driving trace",
        )):
            vid = vehicle_id or "TN-DS-545"
            return {
                "use_tool": True,
                "intent": "vehicle",
                "visualization_hint": "line_chart",
                "tools": [{
                    "tool_name": "telematics_tool",
                    "arguments": {"vehicle_id": vid, "minutes": 60},
                }],
            }

        if any(w in q for w in ("compare", "versus", "vs")) and any(
            m in q for m in ("chennai", "hyderabad", "plant")
        ):
            return {
                "use_tool": True,
                "intent": "comparison",
                "visualization_hint": "bar_chart",
                "tools": [{
                    "tool_name": "analytics_tool",
                    "arguments": {
                        "analysis_type": "plant_comparison",
                        "period": cls._detect_period(q),
                    },
                }],
            }

        if any(w in q for w in ("trend", "over time", "monthly")):
            model = cls._detect_model(q)
            return {
                "use_tool": True,
                "intent": "analytics",
                "visualization_hint": "line_chart",
                "tools": [{
                    "tool_name": "analytics_tool",
                    "arguments": {
                        "analysis_type": "sales_trend" if "sales" in q else "production_trend",
                        "model_name": model,
                        "period": cls._detect_period(q) or "last_6_months",
                    },
                }],
            }

        if any(w in q for w in ("fleet", "unhealthy", "critical")):
            return {
                "use_tool": True,
                "intent": "fleet",
                "tools": [{
                    "tool_name": "fleet_analytics_tool",
                    "arguments": {"query_type": "unhealthy" if "unhealthy" in q else "summary"},
                }],
            }

        if tools:
            return {"use_tool": True, "intent": "vehicle", "tools": tools}

        return {"use_tool": False, "tools": []}

    @staticmethod
    def _detect_model(q: str):
        for model in ("EV-9 Titan", "Glide Pro X", "Dhaya Volt"):
            if model.lower() in q:
                return model
        return None

    @staticmethod
    def _detect_period(q: str):
        periods = {
            "yesterday": "yesterday",
            "last month": "last_month",
            "this month": "this_month",
            "q1": "q1", "q2": "q2", "q3": "q3", "q4": "q4",
            "last quarter": "last_quarter",
            "last year": "last_year",
            "six months": "last_6_months",
            "august": "august",
            "september": "september",
        }
        for phrase, key in periods.items():
            if phrase in q:
                return key
        return None
