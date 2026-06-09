"""
MCP Server — exposes Dai tools via the Model Context Protocol.

Supports stdio (local subprocess) and streamable-http (remote/cloud) transports.
"""

from __future__ import annotations

import argparse
from contextlib import asynccontextmanager
from typing import Any

from mcp.server.fastmcp import FastMCP

from app.database.mongodb import MongoDB
from app.mcp.tools.tool_registry import ToolRegistry


@asynccontextmanager
async def server_lifespan(_server: FastMCP):
    MongoDB.connect()
    try:
        yield
    finally:
        MongoDB.close()


mcp = FastMCP(
    "Dai MCP Server",
    json_response=True,
    lifespan=server_lifespan,
    instructions=(
        "Dhaya Electrics fleet, manufacturing, sales, and analytics tools. vehicle health tool "
        "Use these tools to answer employee queries about vehicles, plants, and business data."
    ),
)


async def _run_tool(tool_name: str, **kwargs: Any) -> dict:
    tool = ToolRegistry.get_tool(tool_name)
    if not tool:
        raise ValueError(f"Tool not found: {tool_name}")

    filtered = {k: v for k, v in kwargs.items() if v is not None}
    return await tool.execute(**filtered)


@mcp.tool(name="vehicle_health_tool", description="Retrieve health diagnostics for a specific vehicle by VIN/vehicle_id.")
async def vehicle_health_tool(vehicle_id: str) -> dict:
    return await _run_tool("vehicle_health_tool", vehicle_id=vehicle_id)


@mcp.tool(name="maintenance_tool", description="Retrieve maintenance history and service details for a vehicle.")
async def maintenance_tool(vehicle_id: str) -> dict:
    return await _run_tool("maintenance_tool", vehicle_id=vehicle_id)


@mcp.tool(
    name="telematics_tool",
    description="Retrieve live telematics telemetry time-series for a vehicle.",
)
async def telematics_tool(vehicle_id: str, minutes: int = 60) -> dict:
    return await _run_tool("telematics_tool", vehicle_id=vehicle_id, minutes=minutes)


@mcp.tool(name="vehicle_catalog_tool", description="Retrieve company vehicle model specifications from catalog.")
async def vehicle_catalog_tool(model_name: str) -> dict:
    return await _run_tool("vehicle_catalog_tool", model_name=model_name)


@mcp.tool(name="fleet_summary_tool", description="Fleet-wide summary counts and optional vehicle lists.")
async def fleet_summary_tool(query_type: str | None = None) -> dict:
    return await _run_tool("fleet_summary_tool", query_type=query_type)


@mcp.tool(
    name="fleet_analytics_tool",
    description="Advanced fleet health analytics and operational issue detection.",
)
async def fleet_analytics_tool(
    query_type: str = "summary",
    model_name: str | None = None,
) -> dict:
    return await _run_tool("fleet_analytics_tool", query_type=query_type, model_name=model_name)


@mcp.tool(name="sales_tool", description="Sales data with optional model, city, and period filters.")
async def sales_tool(
    model_name: str | None = None,
    city: str | None = None,
    period: str | None = None,
) -> dict:
    return await _run_tool("sales_tool", model_name=model_name, city=city, period=period)


@mcp.tool(name="production_tool", description="Manufacturing/production statistics with optional filters.")
async def production_tool(
    model_name: str | None = None,
    plant: str | None = None,
    period: str | None = None,
) -> dict:
    return await _run_tool("production_tool", model_name=model_name, plant=plant, period=period)


@mcp.tool(name="plant_analytics_tool", description="Plant facility details (employees, capacity, status).")
async def plant_analytics_tool(plant_name: str) -> dict:
    return await _run_tool("plant_analytics_tool", plant_name=plant_name)


@mcp.tool(name="executive_summary_tool", description="High-level company business overview.")
async def executive_summary_tool() -> dict:
    return await _run_tool("executive_summary_tool")


@mcp.tool(
    name="analytics_tool",
    description="Advanced analytics: trends, comparisons, rankings, business performance.",
)
async def analytics_tool(
    analysis_type: str,
    model_name: str | None = None,
    plant: str | None = None,
    city: str | None = None,
    period: str | None = None,
    compare_models: list[str] | None = None,
    compare_plants: list[str] | None = None,
) -> dict:
    return await _run_tool(
        "analytics_tool",
        analysis_type=analysis_type,
        model_name=model_name,
        plant=plant,
        city=city,
        period=period,
        compare_models=compare_models,
        compare_plants=compare_plants,
    )


def run_server(transport: str = "stdio", host: str = "0.0.0.0", port: int = 8001) -> None:
    if transport == "stdio":
        mcp.run(transport="stdio")
    elif transport == "streamable-http":
        mcp.settings.host = host
        mcp.settings.port = port
        mcp.run(transport="streamable-http")
    else:
        raise ValueError(f"Unsupported transport: {transport}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Dai MCP Server")
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=["stdio", "streamable-http"],
        help="MCP transport (stdio for local, streamable-http for remote)",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host for streamable-http transport")
    parser.add_argument("--port", type=int, default=8001, help="Port for streamable-http transport")
    args = parser.parse_args()
    run_server(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
