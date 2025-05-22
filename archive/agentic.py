from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_client
import os
import asyncio

load_dotenv()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
set_default_openai_client(client)

agent = Agent(
    name="Assistant", instructions="You are a helpful assistant.", model="gpt-4.1-mini"
)


async def main():
    result = await Runner.run(agent, input="Write a joke about programmer!")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
