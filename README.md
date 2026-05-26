# langchain-mcp-easyframe
LangChain+FastMCP构建的一个简单Agent框架
## 快速开始
0. 安装依赖
```bash
git clone https://github.com/yourusername/langchain-mcp-easyframe.git
cd langchain-mcp-easyframe
pip install -r requirements.txt
```
1. 设置API密钥
找到 `src/langchain_agent.py` 文件，将 `sk-xxx` 替换为你的API密钥。
```python
# langchain_agent.py

# ......其它代码
async def main():
    # 初始化模型
    model = ChatOpenAI(
        model="gpt-3.5-turbo", # 模型名称
        api_key="sk-xx", # 你的API密钥
        base_url="https://xxx/api/v1/" # 模型API基础URL
        )
    
    # ......其它代码
```

2. 运行MCP工具服务器
```bash
python src/local_mcp_server.py
```
3. 运行Agent
```bash
python src/langchain_agent.py
```

4. 终端对话

## 修改agent
### 工具增删
本地工具：`src/local_mcp_server.py` 里进行增删。
```python
# local_mcp_server.py
@mcp.tool
def example_function_name(parameter_1, parameter_2):
    """
        这里填入工具的描述，该工具描述可以被模型看到
        Args:
            parameter_1: 参数1
            parameter_2: 参数2
        Returns:
            执行结果
    """
    return "example_function_name执行成功"
```

远程工具：`src/langchain_agent.py` 里增加远程MCP服务器配置。只需要添加`client`里的配置即可。
例如：
```python
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
        "amap": {
            # 远程：高德地图工具
            "transport": "http",  # 基于 HTTP 的远程服务器
            # amap 服务器的 URL
            "url": "https://mcpmarket.cn/mcp/xxx",
        },
        "12306": {
            # 远程：12306工具
            "transport": "http",  # 基于 HTTP 的远程服务器
            # 12306 服务器的 URL
            "url": "https://mcpmarket.cn/mcp/xxx",
        }
    }
)
```