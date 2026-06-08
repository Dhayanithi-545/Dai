from app.mcp.tools.vehicle_health_tool import VehicleHealthTool
from app.mcp.tools.maintenance_tool import MaintenanceTool
from app.mcp.tools.vehicle_catalog_tool import VehicleCatalogTool
from app.mcp.tools.fleet_summary_tool import FleetSummaryTool
from app.mcp.tools.sales_tool import SalesTool
from app.mcp.tools.production_tool import ProductionTool
from app.mcp.tools.plant_analytics_tool import PlantAnalyticsTool
from app.mcp.tools.executive_summary_tool import ExecutiveSummaryTool
from app.mcp.tools.analytics_tool import AnalyticsTool
from app.mcp.tools.fleet_analytics_tool import FleetAnalyticsTool
from app.mcp.tools.telematics_tool import TelematicsTool


class ToolRegistry:

    tools = {
        "vehicle_health_tool": VehicleHealthTool(),
        "maintenance_tool": MaintenanceTool(),
        "vehicle_catalog_tool": VehicleCatalogTool(),
        "fleet_summary_tool": FleetSummaryTool(),
        "sales_tool": SalesTool(),
        "production_tool": ProductionTool(),
        "plant_analytics_tool": PlantAnalyticsTool(),
        "executive_summary_tool": ExecutiveSummaryTool(),
        "analytics_tool": AnalyticsTool(),
        "fleet_analytics_tool": FleetAnalyticsTool(),
        "telematics_tool": TelematicsTool(),
    }

    @classmethod
    def get_tool(cls, tool_name: str):
        return cls.tools.get(tool_name)
