"""CodeAgent: the model writes Python that calls the tools."""

from smolagents import CodeAgent

from common import make_model
from lesson_tools import calculate_budget, get_party_venue


if __name__ == "__main__":
    agent = CodeAgent(
        tools=[get_party_venue, calculate_budget],
        model=make_model(),
        max_steps=4,
    )
    answer = agent.run(
        "Plan a small party in Yangon for 20 guests. "
        "Use the tools to find a venue and calculate the budget at 15000 MMK per guest."
    )
    print(f"\nFinal answer: {answer}")
