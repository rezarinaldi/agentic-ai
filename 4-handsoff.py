from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field
from typing import List
import json
import asyncio

load_dotenv()

# Travel Agent
# - Travel Planner Agent
# - Hotel Agent
# - Flight Agent


# HOTEL AGENT
@function_tool
def search_hotels():
    # Fetch API to get the hotels
    hotels = [
        {
            "name": "City Center Hotel",
            "location": "Downtown",
            "price_per_night": 99.99,
            "amenities": ["Pool", "Spa", "Gym"],
        },
        {
            "name": "Beach Resort",
            "location": "Beach",
            "price_per_night": 149.99,
            "amenities": ["Pool", "Spa", "Gym"],
        },
        {
            "name": "Mountain Retreat",
            "location": "Mountain",
            "price_per_night": 199.99,
            "amenities": ["Pool", "Spa", "Gym"],
        },
    ]

    return json.dumps(hotels)


class HotelRecommendation(BaseModel):
    name: str
    location: str
    price_per_night: float
    amenities: List[str]
    recommendation_reason: str


hotel_agent = Agent(
    name="Hotel Agent",
    instructions="""
    You are a hotel specialist who help user find the best accomodation for their trip.
    Use the search_hotels to find hotel options and then provide personalized recommendation.
    """,
    model="gpt-4.1",
    output_type=HotelRecommendation,
    tools=[search_hotels],
)


# FLIGHT AGENT
@function_tool
def search_flights() -> str:
    # Fetch API to get the flights
    flights = [
        {
            "airline": "Delta",
            "departure_time": "10:00",
            "arrival_time": "12:00",
            "price": 99.99,
        },
        {
            "airline": "United",
            "departure_time": "11:00",
            "arrival_time": "13:00",
            "price": 149.99,
        },
        {
            "airline": "Southwest",
            "departure_time": "12:00",
            "arrival_time": "14:00",
            "price": 199.99,
        },
    ]

    return json.dumps(flights)


class FlightRecommendation(BaseModel):
    airline: str
    departure_time: str
    arrival_time: str
    price: float
    recommendation_reason: str


flight_agent = Agent(
    name="Flight Agent",
    instructions="""
    You are a flight specialist who help user find the best accomodation for their trip.
    Use the search_flights to find flight options and then provide personalized recommendation.
    """,
    model="gpt-4.1",
    output_type=FlightRecommendation,
    tools=[search_flights],
)


# TRAVEL PLANNER AGENT (Main Agent)
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
    name="Travel Planner Agent",
    instructions="""
    You are a comprehensive travel planner that helps user plan their perfect trip.
    You can always create personalized travel itenerary based on use interest.
    
    Be a fun and helpful when assisting the user.
    
    Consider to have:
    - Local attractions and activites.
    - Budget consideration and constrains.
    - Travel duration.

    If the user asks specifically about flights or hotels, hand off to the appropriate specialist agent.
    """,
    model="gpt-4.1",
    output_type=TravelPlan,
    handoffs=[hotel_agent, flight_agent],
)

queries = [
    "I am going to Japan, find me best flight option!",
    "I'd love to go to Hawaii, find me best hotel option!",
]

for query in queries:
    result = Runner.run_sync(travel_agent, input=query)

    if hasattr(result.final_output, "airline"):
        flight = result.final_output
        print("\n✈ FLIGHT RECOMMENDATION ✈")
        print(f"Airline: {flight.airline}")
        print(f"Departure Time: {flight.departure_time}")
        print(f"Arrival Time: {flight.arrival_time}")
        print(f"Price: {flight.price}")
        print(f"Recommendation Reason: {flight.recommendation_reason}")
        print("===" * 40)

    if hasattr(result.final_output, "name"):
        hotel = result.final_output
        print("\n🏨 HOTEL RECOMMENDATION 🏨")
        print(f"Hotel Name: {hotel.name}")
        print(f"Location: {hotel.location}")
        print(f"Price per Night: {hotel.price_per_night}")
        print(f"Amenities: {hotel.amenities}")
        print(f"Recommendation Reason: {hotel.recommendation_reason}")
        print("===" * 40)

# async def main():
#     queries = [
#         "I am going to Switzerland, find me best flight option!",
#         "I'd love to go to San Francisco, find me best hotel option!",
#     ]

#     for query in queries:
#         print("\n" + "=" * 50)
#         print(f"Query: {query}")

#     result = await Runner.run(travel_agent, query)

#     print("\nFinal Response:")

#     if hasattr(result.final_output, "airline"):
#         flight = result.final_output
#         print("\n✈ FLIGHT RECOMMENDATION ✈")
#         print(f"Airline: {flight.airline}")
#         print(f"Departure Time: {flight.departure_time}")
#         print(f"Arrival Time: {flight.arrival_time}")
#         print(f"Price: {flight.price}")
#         print(f"\nWhy this flight is recommended: {flight.recommendation_reason}")
#         print("===" * 40)

#     elif hasattr(result.final_output, "name") and hasattr(
#         result.final_output, "amenities"
#     ):
#         hotel = result.final_output
#         print("\n🏨 HOTEL RECOMMENDATION 🏨")
#         print(f"Hotel Name: {hotel.name}")
#         print(f"Location: {hotel.location}")
#         print(f"Price per Night: {hotel.price_per_night}")

#         print("\nAmenities:")
#         for i, amenity in enumerate(hotel.amenities, 1):
#             print(f"{i}. {amenity}")

#         print(f"\nWhy this hotel is recommended: {hotel.recommendation_reason}")
#         print("===" * 40)

#     elif hasattr(result.final_output, "destination"):
#         travel_plan = result.final_output
#         print(f"\n🌟 TRAVEL PLAN FOR {travel_plan.destination.upper()}🌟")
#         print(f"Trip Duration: {travel_plan.trip_duration} days")
#         print(f"Budget: {travel_plan.budget}")

#         print("\nRecommended Activities:")
#         for i, activity in enumerate(travel_plan.activities, 1):
#             print(f"{i}. {activity}")

#         print("\n📝 Notes:")
#         for i, note in enumerate(travel_plan.notes, 1):
#             print(f"{i}. {note}")
#         print("===" * 40)

#     else:  # Generic Response
#         print(result.final_output)


# if __name__ == "__main__":
#     asyncio.run(main())
