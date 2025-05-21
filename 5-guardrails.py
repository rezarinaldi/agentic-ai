from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
)
from pydantic import BaseModel
import asyncio

load_dotenv()


class GuardrailOutputType(BaseModel):
    is_django_python_question: bool
    reasoning: str


guardrails_agent = Agent(
    name="Guardrails Agent",
    instructions="Check if user asking Django and Python.",
    output_type=GuardrailOutputType,
)


@input_guardrail
async def django_python_guardrail(ctx, agent, input):
    result = await Runner.run(guardrails_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_django_python_question,
    )


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4.1",
    input_guardrails=[django_python_guardrail],
)


async def main():
    try:
        result = await Runner.run(agent, input="Can you help me with React.js?")
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("We can't answer this question.")


if __name__ == "__main__":
    asyncio.run(main())
