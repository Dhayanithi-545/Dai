import asyncio
import sys
import os

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
 

# Make sure the backend root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from app.mcp.client.mcp_client import MCPClient

async def main():
    print(f"Connecting to: {os.getenv('MCP_SERVER_URL', 'NOT SET')}")
    print(f"Transport: {os.getenv('MCP_TRANSPORT', 'NOT SET')}")
    print("-" * 40)

    try:
        await MCPClient.connect()
        print("✅ Connected!")
        print(f"Server info: {MCPClient.get_connection_info()}")
        print(f"Tools: {MCPClient.get_tools_summary()}")
        result = await session.initialize()
        print(result)

        tools = await session.list_tools()
        print(tools)
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        await MCPClient.disconnect()

if __name__ == "__main__":
    asyncio.run(main())