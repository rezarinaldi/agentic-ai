# MCP (Model Context Protocol)
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServer, MCPServerStdio
import asyncio
import os

load_dotenv()


async def run(mcp_servers: list[MCPServer]):
    agent = Agent(
        name="Assistant",
        instructions="""You are a funny person, and helpful assistant.
        Only use mcp_severs available if needed.
        """,
        model="gpt-4.1",
        mcp_servers=mcp_servers,
    )

    result = await Runner.run(agent, input="Write a jokes about designer!")
    print(result.final_output)


async def main():
    async with MCPServerStdio(
        {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")},
        }
    ) as mcp_server:
        await run([mcp_server])


if __name__ == "__main__":
    asyncio.run(main())
