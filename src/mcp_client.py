import asyncio
from fastmcp import Client, FastMCP
import json

client = Client("agent_demo\src\local_mcp_server.py")
client = Client("https://mcpmarket.cn/mcp/1211afc8fdf0663a3f4f7b9c")

# 本地 Python 脚本
# client = Client("https://mcpmarket.cn/mcp/1211afc8fdf0663a3f4f7b9c")

async def main():
    async with client:
        # 基本服务器交互
        await client.ping()
        
        # 列出可用操作
        tools = await client.list_tools()

        print(tools[0].name, tools[0].description)
        print(json.dumps(tools[0].inputSchema, ensure_ascii=False, indent=2))

asyncio.run(main())