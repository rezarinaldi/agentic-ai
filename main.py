# MCP (Model Context Protocol)
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServer, MCPServerStdio
import os

load_dotenv()


async def run(mcp_servers: list[MCPServer]):
    agent = Agent(
        name="Assistant",
        instructions="""You are a helpful assistant.
        Only use mcp_severs available if needed.
        """,
        model="gpt-4.1",
        mcp_servers=mcp_servers,
    )

    result = await Runner.run(
        agent, input="Go to indrazm.com and summarize the content!"
    )
    print(result.final_output)


async def main():
    async with MCPServerStdio(
        {"command": "npx", "args": ["mcp-remote", "http://localhost:8000/mcp", "8080"]}
    ) as mcp_server:
        await run([mcp_server])


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
