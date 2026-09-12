# Multi Agent，既多智能体协作系统，专门用来处理复杂的任务流程。

# 1.1 使用场景
# 通常在以下几种情况下我们会使用Multi Agent：
# - 上下文管理(Context Management)：如果同时需要调用的工具很多，或者上下文内容很多，我们可以将任务拆分，交给不同的Agent处理
# - 分布式开发(Distributed development)：不同的团队独立开发和维护自己的Agent，并将他们组合成一个更大的Agent
# - 并行(Parallelization)：将任务拆分为多个子任务，并交给专门的Agent处理，并同时执行它们以加快处理速度

# 1.2 常见模式
# 多智能体协作的模式有很多种，比较常见的有：
# - Subagents：子代理模式，一个主Agent将多个子Agent作为Tool来协调使用。所有请求都由主Agent处理，决定何时以及如何调用每个子Agent
# - Handoffs：传递模型，随着任务的执行改变state中的任务状态，从而触发路由变更或者触发Agent的配置变更，从而切换到其它Agent或者改变Agent的工具或系统提示（类似与一个新agent）。因此每个Agent都可以与用户交互，处理用户请求并返回响应。
# - Skills：技能模式，只有1个Agent，根据任务按需加载Skill或知识
# - Router：路由模式，1个负责路由的Agent对用户请求进行分类，将请求导向给一个或多个专门的Agent。最后再由一个Agent负责总结结果。



# 解决mcp在Windows平台运行的问题
# import sys
# import asyncio

# # Fix for Windows issues in Jupyter notebooks
# if sys.platform == "win32":
#     # 1. Use ProactorEventLoop for subprocess support
#     if not isinstance(asyncio.get_event_loop_policy(), asyncio.WindowsProactorEventLoopPolicy):
#         asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

#     # 2. Redirect stderr to avoid fileno() error when launching MCP servers
#     if "ipykernel" in sys.modules:
#         sys.stderr = sys.__stderr__


import asyncio
from typing import Any
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_community.utilities import SQLDatabase
from langchain.agents import AgentState
from tavily import TavilyClient
from langchain.tools import tool
from langchain.tools import ToolRuntime
from langchain.messages import HumanMessage, ToolMessage, AIMessage
from langgraph.types import Command
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

# 定义Tavily web_search工具
tavily_client = TavilyClient()

@tool
def web_search(query: str) -> dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)


import os
db_path = os.path.join(os.path.dirname(__file__), "Chinook.db")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

# db = SQLDatabase.from_uri("sqlite:///20260905multiagent/Chinook.db")

@tool
def query_playlist_db(query: str) -> str:

    """Query the database for playlist information"""

    try:
        return db.run(query)
    except Exception as e:
        return f"Error querying database: {e}"



# MCP客户端，包含Time、Kiwi两个MCP
client = MultiServerMCPClient(
    {
        "travel_server": {
                "transport": "http",
                "url": "https://mcp.kiwi.com"
        },
        "time": {
            "transport": "stdio",
            "command": "uvx",
            "args": [
                "mcp-server-time",
                "--local-timezone=Asia/Shanghai"
            ]
        }
    }
)


class WeddingState(AgentState):
    origin: str
    destination: str
    guest_count: str
    genre: str


@tool
def update_state(origin: str, destination: str, guest_count: str, genre: str, runtime: ToolRuntime) -> str:
    """Update the state when you know all of the values: origin, destination, guest_count, genre"""
    return Command(update={
        "origin": origin,
        "destination": destination,
        "guest_count": guest_count,
        "genre": genre,
        "messages": [ToolMessage("Successfully updated state", tool_call_id=runtime.tool_call_id)]}
        )







# 注意MultiServerMCPClient是异步的，结果都是协程对象，需要await
async def main():
    tools = await client.get_tools()


    # Travel agent
    travel_agent = create_agent(
        model="deepseek-chat",
        tools=tools,
        system_prompt="""
        You are a travel agent. Search for flights to the desired destination wedding location, you must call tool to get current time.
        You are not allowed to ask any more follow up questions, you must find the best flight options based on the following criteria:
        - Price (lowest, economy class)
        - Duration (shortest)
        - Date (time of year which you believe is best for a wedding at this location)
        To make things easy, only look for one ticket, one way.
        You may need to make multiple searches to iteratively find the best options.
        You will be given no extra information, only the origin and destination. It is your job to think critically about the best options.
        Once you have found the best options, let the user know your shortlist of options.
        Remember call tool to get current time when you need.
        """
    )


    # 创建 Venue agent
    venue_agent = create_agent(
        model="deepseek-chat",
        tools=[web_search],
        system_prompt="""
        You are a venue specialist. Search for venues in the desired location, and with the desired capacity.
        You are not allowed to ask any more follow up questions, you must find the best venue options based on the following criteria:
        - Price (lowest)
        - Capacity (exact match)
        - Reviews (highest)
        You may need to make multiple searches to iteratively find the best options.
        """
    )

    # Playlist agent
    playlist_agent = create_agent(
        model="deepseek-chat",
        tools=[query_playlist_db],
        system_prompt="""
        You are a playlist specialist. Query the sql database and curate the perfect playlist for a wedding given a genre.
        Once you have your playlist, calculate the total duration and cost of the playlist, each song has an associated price.
        If you run into errors when querying the database, try to fix them by making changes to the query.
        Do not come back empty handed, keep trying to query the db until you find a list of songs.
        You may need to make multiple queries to iteratively find the best options.
        """
    )


    @tool
    async def search_flights(runtime: ToolRuntime) -> str:
        """Travel agent searches for flights to the desired destination wedding location."""
        origin = runtime.state["origin"]
        destination = runtime.state["destination"]
        response = await travel_agent.ainvoke({"messages": [HumanMessage(content=f"Find flights from {origin} to {destination}")]})
        return response['messages'][-1].content

    @tool
    def search_venues(runtime: ToolRuntime) -> str:
        """Venue agent chooses the best venue for the given location and capacity."""
        destination = runtime.state["destination"]
        capacity = runtime.state["guest_count"]
        query = f"Find wedding venues in {destination} for {capacity} guests"
        response = venue_agent.invoke({"messages": [HumanMessage(content=query)]})
        return response['messages'][-1].content

    @tool
    def suggest_playlist(runtime: ToolRuntime) -> str:
        """Playlist agent curates the perfect playlist for the given genre."""
        genre = runtime.state["genre"]
        query = f"Find {genre} tracks for wedding playlist"
        response = playlist_agent.invoke({"messages": [HumanMessage(content=query)]})
        return response['messages'][-1].content


    coordinator = create_agent(
        model="deepseek-chat",
        tools=[search_flights, search_venues, suggest_playlist, update_state],
        state_schema=WeddingState,
        system_prompt="""
        You are a wedding coordinator. Delegate tasks to your specialists for flights, venues and playlists.
        First find all the information you need to update the state. Once that is done you can delegate the tasks.
        Once you have received their answers, coordinate the perfect wedding for me.
        """
    )

    response = await coordinator.ainvoke(
        {
            "messages": [HumanMessage(content="我来自伦敦，我想在巴黎举办一场100人的婚礼，爵士风格的，请用中文回答")],
        }
    )

    for message in response["messages"]:
        message.pretty_print()


if __name__ == "__main__":
    asyncio.run(main())
