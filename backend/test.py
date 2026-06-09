import asyncio
import traceback
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
 
async def main():
    try:
        async with streamable_http_client(
            "http://34.131.112.231/mcp"
        ) as (read, write, _):
 
            async with ClientSession(read, write) as session:
                result = await session.initialize()
                print(result)
 
                tools = await session.list_tools()
                print(tools)
 
    except Exception:
        traceback.print_exc()
 
if __name__ == "__main__":
    asyncio.run(main())