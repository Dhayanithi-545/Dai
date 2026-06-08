from datetime import datetime

from app.database.mongodb import MongoDB


class MemoryService:

    COLLECTION_NAME = "conversation_memory"
    DEFAULT_SESSION_ID = "default_user"

    @classmethod
    def _collection(cls):
        return MongoDB.get_database()[cls.COLLECTION_NAME]

    @classmethod
    async def get_context(cls) -> dict:
        memory = cls._collection().find_one(
            {"session_id": cls.DEFAULT_SESSION_ID}
        )
        if not memory:
            return {}
        return {
            "last_vehicle_id": memory.get("last_vehicle_id"),
            "last_model_name": memory.get("last_model_name"),
            "last_plant": memory.get("last_plant"),
            "last_intent": memory.get("last_intent"),
            "last_query": memory.get("last_query"),
        }

    @classmethod
    async def save_context(
        cls,
        *,
        vehicle_id=None,
        model_name=None,
        plant=None,
        intent=None,
        query=None,
    ):
        updates = {"updated_at": datetime.utcnow()}
        if vehicle_id:
            updates["last_vehicle_id"] = vehicle_id
        if model_name:
            updates["last_model_name"] = model_name
        if plant:
            updates["last_plant"] = plant
        if intent:
            updates["last_intent"] = intent
        if query:
            updates["last_query"] = query

        cls._collection().update_one(
            {"session_id": cls.DEFAULT_SESSION_ID},
            {"$set": updates},
            upsert=True,
        )

    @classmethod
    async def save_vehicle_context(cls, vehicle_id: str):
        await cls.save_context(vehicle_id=vehicle_id)

    @classmethod
    async def get_last_vehicle(cls):
        ctx = await cls.get_context()
        return ctx.get("last_vehicle_id")

    @classmethod
    def format_context_for_planner(cls, context: dict) -> str:
        if not context:
            return "No prior conversation context."

        lines = ["Conversation context from previous messages:"]
        if context.get("last_vehicle_id"):
            lines.append(f"- Last vehicle discussed: {context['last_vehicle_id']}")
        if context.get("last_model_name"):
            lines.append(f"- Last model discussed: {context['last_model_name']}")
        if context.get("last_plant"):
            lines.append(f"- Last plant discussed: {context['last_plant']}")
        if context.get("last_intent"):
            lines.append(f"- Previous intent: {context['last_intent']}")
        if context.get("last_query"):
            lines.append(f"- Previous query: {context['last_query']}")

        lines.append(
            "If the current query is a follow-up (e.g. 'maintenance?', "
            "'which is more efficient?', 'and sales?'), reuse relevant context."
        )
        return "\n".join(lines)

    @classmethod
    async def enrich_query(cls, user_query: str) -> str:
        """Expand terse follow-up queries using stored context."""
        ctx = await cls.get_context()
        q = user_query.strip().lower()

        follow_ups = {
            "maintenance", "maintenance?", "health", "health?",
            "diagnostics", "diagnostics?", "service", "service?",
            "and sales", "sales?", "production?", "efficiency?",
        }

        if q in follow_ups or len(q.split()) <= 2:
            parts = [user_query]
            if ctx.get("last_vehicle_id") and any(
                w in q for w in ("maintenance", "health", "diagnostic", "service")
            ):
                parts.append(f"(for vehicle {ctx['last_vehicle_id']})")
            if ctx.get("last_plant") and any(
                w in q for w in ("efficiency", "production", "plant", "sales")
            ):
                parts.append(f"(for {ctx['last_plant']})")
            if ctx.get("last_model_name") and "sales" in q:
                parts.append(f"(for {ctx['last_model_name']})")
            return " ".join(parts)

        return user_query
