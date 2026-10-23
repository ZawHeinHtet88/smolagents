"""A manager delegates retrieval to a named specialist agent."""

from smolagents import CodeAgent, ToolCallingAgent

from common import make_model
from lesson_tools import calculate_budget, get_party_venue


if __name__ == "__main__":
    model = make_model()
    venue_researcher = ToolCallingAgent(
        tools=[get_party_venue],
        model=model,
        name="venue_researcher",
        description="Looks up a venue in Yangon or Mandalay.",
        max_steps=3,
    )
    manager = CodeAgent(
        tools=[calculate_budget],
        model=model,
        managed_agents=[venue_researcher],
        max_steps=5,
    )
    answer = manager.run(
        "Ask the venue researcher for a venue in Yangon. "
        "Then calculate the budget for 10 guests at 15000 MMK each."
    )
    print(f"\nFinal answer: {answer}")
