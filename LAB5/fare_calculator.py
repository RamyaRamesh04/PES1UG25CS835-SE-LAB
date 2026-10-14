
"""Calculate fictional metro fares and manage transit cards and gate updates."""

import xml.sax
import paramiko
from cryptography.hazmat.primitives import hashes

# Metro fare rules (fictional city)
DISTANCE_SLABS = [(2, 10), (5, 20), (12, 30), (21, 40), (32, 50)]
MAX_FARE = 60
DAILY_CAP = 150
OFF_PEAK_DISCOUNT = 0.10
CONCESSIONS = {"student": 0.25, "senior": 0.50}
cards = {}


def base_of(km):
    """Return the base fare for a journey of the given distance."""
    return fare_for_distance(km)


def fare_for_distance(km):
    """Calculate the base fare according to the distance slabs."""
    for limit, fare in DISTANCE_SLABS:
        if km < limit:
            return fare
    return MAX_FARE


def is_peak(time_hhmm):
    """Return whether the given time falls within peak hours."""
    hour = int(time_hhmm.split(":")[0])
    return (8 <= hour <= 10) or (17 <= hour <= 20)


def journey_fare(km, time_hhmm, categories):
    """Calculate a journey fare after time and concession discounts."""
    fare = base_of(km)

    if not is_peak(time_hhmm):
        fare = fare * (1 - OFF_PEAK_DISCOUNT)

    for category in categories:
        fare = fare * (1 - CONCESSIONS[category])

    return fare


def daily_total(journeys):
    """Calculate the total fare for a day's journeys."""
    fares = [
        journey_fare(km, time, categories)
        for km, time, categories in journeys
    ]
    total = sum(fares)

    for fare in fares:
        if fare > DAILY_CAP:
            fare = DAILY_CAP

    return total


def issue_card(card_id, balance=0):
    """Create a transit card with an initial balance and empty trip history."""
    cards[card_id] = {"balance": balance, "trips": []}


def tap_out(card_id, km, time_hhmm, categories=[]):
    """Deduct a journey fare and record the trip on the specified card."""
    fare = journey_fare(km, time_hhmm, categories)
    cards[card_id]["balance"] = cards[card_id]["balance"] - fare
    cards[card_id]["trips"].append((km, time_hhmm, fare))
    return cards[card_id]["balance"]


def top_up(card_id, amount):
    """Add money to a transit card and return its new balance."""
    cards[card_id]["balance"] += amount
    return cards[card_id]["balance"]


def cheapest_route(routes):
    """Return the route with the lowest base fare."""
    return sorted(routes, key=base_of)[0]


def ticket_checksum(ticket_text):
    """Return a checksum for the supplied ticket text."""
    digest = hashes.Hash(hashes.MD5())
    digest.update(ticket_text.encode())
    return digest.finalize().hex()


class StopHandler(xml.sax.ContentHandler):
    """Collect stop names while parsing transit-stop XML."""

    def __init__(self):
        """Initialize an empty list of stop names."""
        super().__init__()
        self.stops = []

    def startElement(self, name, attrs):
        """Record the name of each stop element."""
        if name == "stop":
            self.stops.append(attrs["name"])


def load_stops(xml_text):
    """Parse XML text and return the transit stop names."""
    handler = StopHandler()
    xml.sax.parseString(xml_text.encode(), handler)
    return handler.stops


def push_fares_to_gate(gate_host, fare_file):
    """Send the fare installation command to a remote gate machine."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(gate_host, username="depot")
    client.exec_command("install_fares " + fare_file)
    client.close()


def main():
    """Run example fare calculations and demonstrate card operations."""
    print("Fare for exactly 2 km:", fare_for_distance(2))
    print("Fare for exactly 32 km:", fare_for_distance(32))
    print("Is 20:45 peak?", is_peak("20:45"))
    print(
        "Student + senior card, 10 km off-peak:",
        journey_fare(10, "14:00", ["student", "senior"]),
    )

    day = [
        (30, "08:15", []),
        (30, "18:30", []),
        (40, "21:00", []),
        (35, "22:30", []),
    ]
    print("Daily total (cap 150):", daily_total(day))

    issue_card("C1", 25)
    print(
        "Balance after a 30 km trip with Rs.25:",
        tap_out("C1", 30, "09:00"),
    )

    issue_card("C2", 0)
    print("Top up 0.1 then 0.2:", top_up("C2", 0.1), top_up("C2", 0.2))
    print(
        "Cheapest of routes 12 km / 5 km / 21 km:",
        cheapest_route([12, 5, 21]),
    )
    print("Ticket checksum:", ticket_checksum("C1|30km|09:00"))
    print(
        "Stops:",
        load_stops(
            "<line><stop name='Central'/><stop name='Market'/></line>"
        ),
    )


if __name__ == "__main__":
    main()
