# my_server.py
from fastmcp import FastMCP

mcp = FastMCP(name="MyServer")

@mcp.tool
def get_height(place: str) -> str:
    """获取指定地点的高度。"""
    return f"{place}的高度是100米"


@mcp.tool
def greet(name: str) -> str:
    """按名称向用户打招呼。"""
    return f"Hello, {name}!"
@mcp.tool
def add(a: int, b: int) -> int:
    """将两个整数相加。"""
    return a + b
@mcp.tool
def sub(a: int, b: int) -> int:
    """将两个整数相去。"""
    return a - b
@mcp.tool
def write_to_file(file_path, content):
    """
    将指定内容写入指定文件
    Args:
        file_path: 文件路径
        content: 要写入的内容
    Returns:
        写入成功字符串
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.replace("\\n", "\n"))
    return "写入成功"
@mcp.tool
def read_file(file_path):
    """用于读取文件内容"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool
def run_terminal_command(command):
    """
        用于执行终端命令
        Args:
            command: 终端命令字符串
        Returns:
            执行结果字符串
    """
    import subprocess
    run_result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return "执行成功" if run_result.returncode == 0 else run_result.stderr

if __name__ == "__main__":
    # 这会运行服务器，默认使用 STDIO 传输
    # mcp.run()
    mcp.run(transport="http", host="127.0.0.1", port=9000)
    # 要使用不同的传输，例如 HTTP：
    # mcp.run(transport="http", host="127.0.0.1", port=9000)