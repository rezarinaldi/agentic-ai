from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field
from typing import List

load_dotenv()


# OpenAI would inspect this function (arguments and output)
@function_tool
def get_weather(city: str) -> str:
    # Fetch API to get the weather
    weathers = {
        "Switzerland": "Snowy",
        "New York": "Cloudy",
        "London": "Rainy",
        "Paris": "Sunny",
        "Toronto": "Cloudy",
        "Sydney": "Rainy",
        "Moscow": "Snowy",
        "Turkey": "Sunny",
    }

    if city in weathers:
        return weathers[city]
    else:
        return "Unknown"


class TravelPlan(BaseModel):
    destination: str
    trip_duration: str
    budget: float
    activities: List[str] = Field(
        description="List of recommended activities for the trip."
    )
    notes: List[str] = Field(
        description="List of additional notes or recommendations for the trip."
    )


travel_agent = Agent(
    name="Travel Planner",
    instructions="""
    You are a comprehensive travel planner that helps user plan their perfect trip.
    You can always create personalized travel itenerary based on use interest.
    
    Be a fun and helpful when assisting the user.
    
    Consider to have:
    - Local attractions and activites.
    - Budget consideration and constrains.
    - Travel duration.
    """,
    model="gpt-4.1",
    output_type=TravelPlan,
    tools=[get_weather],
)

result = Runner.run_sync(
    travel_agent,
    input="I am planning to have a trip to Switzerland, with budget $1000. What should I do there? And tell me the weather in Switzerland.",
)
travel_plan = result.final_output

print("TRAVEL PLAN AND ITENERARIES")
print(f"Destination: {travel_plan.destination}")
print(f"Trip Duration: {travel_plan.trip_duration}")
print(f"Budget: {travel_plan.budget}")
print("List of Activities:")
for activity in travel_plan.activities:
    print(f"- {activity}")
print("List of Notes:")
for note in travel_plan.notes:
    print(f"- {note}")
