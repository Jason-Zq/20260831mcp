# 3.1 创建简单的MCP服务器
# 只需要定义几个方法，然后利用FastMCP提供的装饰器即可：
# - @mcp.tool : 作为MCP中的工具
# - @mcp.resources : 返回MCP需要的resources，类似拓展知识库
# - @mcp.prompt : 返回MCP预定义的Prompt，预设的提示词

# 1. MCP是什么
#   - 开放协议，标准化LLM应用获取工具的方式
#   - 客户端-服务器架构
# 2. 连接方式
#   - STDIO: 本地MCP服务器
#   - HTTP: 远程MCP服务器
# 3. 使用流程
#   - 配置MultiServerMCPClient
#   - 调用get_tools()获取工具
#   - 创建Agent并调用
# 4. 自定义MCP Server
#   - 导入FastMCP
#   - 使用@mcp.tool装饰函数，定义工具（必备）
#   - 使用@mcp.resource装饰函数，返回resources（可选）
#   - 使用@mcp.prompt装饰函数，返回Prompt（可选）
#   - 使用mcp.run()启动MCP服务



from fastmcp import FastMCP

# 初始化mcp
mcp = FastMCP("Math")


# mcp tools
@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b


@mcp.tool
def square_root(x: float) -> float:
    """Calculate the square root of a number"""
    return x ** 0.5


# 启动mcp服务，通信方式设置为stdio
if __name__ == "__main__":
    mcp.run(transport="stdio")