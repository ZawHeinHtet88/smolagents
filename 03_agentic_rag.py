"""Local BM25 retrieval tool that an agent can call when it needs facts."""

import re

from rank_bm25 import BM25Okapi
from smolagents import ToolCallingAgent, tool

from common import make_model


NOTES = [
    "Yangon venue: Inya Lake Garden holds 80 guests and is outdoors.",
    "Mandalay venue: Mandalay Hall holds 120 guests and is indoors.",
    "Catering: vegetarian meals cost 15000 MMK per guest.",
    "Catering: standard meals cost 12000 MMK per guest.",
    "Transport: a bus from Yangon city center to Inya Lake costs 80000 MMK.",
]


def words(text):
    return re.findall(r"\w+", text.lower())


INDEX = BM25Okapi([words(note) for note in NOTES])


@tool
def search_party_notes(query: str) -> str:
    """Search local party-planning notes for relevant facts.

    Args:
        query: Search terms about venues, catering, or transport.
    """
    scores = INDEX.get_scores(words(query))
    ranked = sorted(range(len(NOTES)), key=lambda i: scores[i], reverse=True)
    matches = [NOTES[i] for i in ranked if scores[i] > 0][:1]
    return "\n".join(matches) if matches else "No matching notes found."


if __name__ == "__main__":
    agent = ToolCallingAgent(
        tools=[search_party_notes], model=make_model(), max_steps=5
    )
    answer = agent.run(
        "Find the yangon venue capacity and the vegetarian meal price. "
        "Use the notes for both facts."
    )
    print(f"\nFinal answer: {answer}")
