"""ToolCallingAgent: the model sends structured tool names and arguments."""

from smolagents import ToolCallingAgent

from common import make_model
from lesson_tools import calculate_budget, get_party_venue


if __name__ == "__main__":
    agent = ToolCallingAgent(
        tools=[get_party_venue, calculate_budget],
        model=make_model(),
        max_steps=4,
    )
    answer = agent.run(
        "Find a party venue in Mandalay, then calculate the budget "
        "for 12 guests at 20000 MMK each."
    )
    print(f"\nFinal answer: {answer}")
