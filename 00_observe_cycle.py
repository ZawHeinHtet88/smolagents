"""Offline Thought -> Action -> Observation example. No account needed."""


def weather_tool(city):
    data = {"yangon": "28 C, cloudy", "mandalay": "31 C, sunny"}
    return data.get(city.lower(), "No local weather data for that city")


if __name__ == "__main__":
    question = "What is the weather in Yangon?"
    thought = "I need a weather observation for Yangon."
    action = ("weather_tool", {"city": "Yangon"})
    observation = weather_tool(**action[1])
    answer = f"Yangon weather: {observation}"

    print(f"User: {question}")
    print(f"Thought: {thought}")
    print(f"Action: {action[0]}({action[1]})")
    print(f"Observation: {observation}")
    print(f"Final answer: {answer}")
