# 访问多个 MCP 服务器
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, AIMessage, SystemMessage, RemoveMessage

import asyncio
import json


client = MultiServerMCPClient(
    {
        "local":{
            # 本地：本地MCP工具服务器
            "transport": "http",  
            "url": "http://127.0.0.1:9000/mcp",
            # "transport": "stdio",
            # "command": "python",  # 本地子进程通信，新手不推荐，可能导致系统卡死（你的电脑卡死）;
            # # local_mcp_server.py 文件的绝对路径
            # "args": ["/root/langchain-mcp-easyframe/src/local_mcp_server.py"],
        },
        # "amap": {
        #     # 远程：高德地图工具
        #     "transport": "http",  # 基于 HTTP 的远程服务器
        #     # amap 服务器的 URL
        #     "url": "https://mcpmarket.cn/mcp/xxx",
        # },
        # "12306": {
        #     # 远程：12306工具
        #     "transport": "http",  # 基于 HTTP 的远程服务器
        #     # 12306 服务器的 URL
        #     "url": "https://mcpmarket.cn/mcp/xxx",
        # }
    }
)
async def get_tools():
    return await client.get_tools()
'''
'stdio', 'sse', 'websocket', 'http'

总结：
http URL：transport 使用 http 或 streamable_http
本地子进程通信：transport 使用 stdio
'''
tools = asyncio.run(get_tools())
for tool in tools:
    print(tool.name, tool.description)
    # print(json.dumps(tool.args_schema, ensure_ascii=False, indent=2))
    # print(json.dumps(tool.inputSchema, ensure_ascii=False, indent=2))
    print("="*50)


# React 风格系统提示词
react_system_prompt = """
你是一个 React 风格的代理，需要：
1. 首先分析问题，进行推理（Reasoning）
2. 然后决定是否需要使用工具（Acting）
3. 根据工具执行结果，再次推理并决定下一步行动
4. 最终给出答案

请在思考过程中明确标记你的推理过程，使用 <think>...</think> 格式。
"""

async def main():
    # 初始化模型
    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key="sk-xx",
        base_url="https://xxx/api/v1/"
        )
    
    # 创建 React Agent
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=react_system_prompt,
        debug=True
    )
    system_msg = SystemMessage(content=react_system_prompt)
    messages = [system_msg]
    
    # 运行React Agent
    while True:
        human_input = input("用户输入：")
        messages.append(HumanMessage(content=human_input))
        # 大模型回答
        result = await agent.ainvoke({
            "messages": messages
        })
        # 将模型消息添加到消息列表
        messages.append(result["messages"][-1])
        print("模型输出：", result["messages"][-1].content)
        print("="*50)
    
    # 查看结果
    # print(result["messages"][-1]["content"])

if __name__ == "__main__":
    asyncio.run(main())
