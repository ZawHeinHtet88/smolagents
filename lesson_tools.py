"""Small, deterministic tools shared by the online agent lessons."""

from smolagents import tool


@tool
def get_party_venue(city: str) -> str:
    """Find a practice venue in a city.

    Args:
        city: City name to look up.
    """
    venues = {
        "yangon": "Inya Lake Garden, capacity 80, outdoor",
        "mandalay": "Mandalay Hall, capacity 120, indoor",
    }
    return venues.get(city.lower(), f"No venue in the practice data for {city}.")


@tool
def calculate_budget(guests: int, price_per_guest: int) -> int:
    """Calculate the total party budget from the guest count.

    Args:
        guests: Number of guests.
        price_per_guest: Cost for one guest in MMK.
    """
    return guests * price_per_guest
