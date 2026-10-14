
"""Calculate fictional metro fares and manage transit cards."""

import paramiko
from cryptography.hazmat.primitives import hashes
from defusedxml import ElementTree as SafeET


BASE_FARE = 10
FARE_PER_KM = 2
DAILY_CAP = 150
PEAK_HOURS = (8, 9, 10, 17, 18, 19)


def calculate_fare(distance_km):
    """Calculate the base fare plus the distance-based fare."""
    if distance_km < 0:
        raise ValueError("Distance cannot be negative.")

    return BASE_FARE + (distance_km * FARE_PER_KM)


def is_peak(time_str):
    """Return True when the supplied time falls within peak hours."""
    try:
        hour, minute = map(int, time_str.split(":"))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            return False
        return hour in PEAK_HOURS
    except (ValueError, AttributeError):
        return False


def apply_discount(fare, is_student=False, is_senior=False):
    """Apply applicable student and senior discounts to a fare."""
    if fare < 0:
        raise ValueError("Fare cannot be negative.")

    discount = 0.0

    if is_student:
        discount += 0.25

    if is_senior:
        discount += 0.25

    discount = min(discount, 0.50)
    return fare * (1 - discount)


def daily_total(fares):
    """Return the total fares charged, limited by the daily cap."""
    if any(fare < 0 for fare in fares):
        raise ValueError("Fares cannot be negative.")

    return min(sum(fares), DAILY_CAP)


def tap_out(balance, fare, categories=None):
    """Deduct a fare and return the updated balance and categories."""
    if categories is None:
        categories = []

    if balance < 0 or fare < 0:
        raise ValueError("Balance and fare cannot be negative.")

    if fare > balance:
        raise ValueError("Insufficient balance.")

    return balance - fare, categories


def ticket_checksum(ticket_data):
    """Generate a SHA-256 checksum for ticket data."""
    digest = hashes.Hash(hashes.SHA256())
    digest.update(ticket_data.encode("utf-8"))
    return digest.finalize().hex()


def load_stops(xml_data):
    """Safely parse XML data and return the names of transit stops."""
    root = SafeET.fromstring(xml_data)
    return [
        stop.text.strip()
        for stop in root.findall(".//stop")
        if stop.text and stop.text.strip()
    ]


def push_fares_to_gate(host, username, password, local_file):
    """Upload a fare file to a trusted remote host using SFTP."""
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())

    try:
        client.connect(
            hostname=host,
            username=username,
            password=password,
        )

        with client.open_sftp() as sftp:
            sftp.put(local_file, "/incoming/fares.csv")
    finally:
        client.close()


def cheapest_route(*distances):
    """Return the shortest route distance from the supplied options."""
    if not distances:
        raise ValueError("At least one route distance is required.")

    if any(distance < 0 for distance in distances):
        raise ValueError("Route distances cannot be negative.")

    return min(distances)


def main():
    """Run example calculations for the fare calculator."""
    print("Fare for exactly 2 km:", calculate_fare(2))
    print("Fare for exactly 32 km:", calculate_fare(32))
    print("Is 20:45 peak?", is_peak("20:45"))

    discounted_fare = apply_discount(
        calculate_fare(10),
        is_student=True,
        is_senior=True,
    )
    print("Student + senior card, 10 km:", discounted_fare)

    print("Daily total (cap 150):", daily_total([60, 70, 50]))

    try:
        balance, _ = tap_out(25, calculate_fare(30))
        print("Balance after trip:", balance)
    except ValueError as error:
        print("Trip rejected:", error)

    print("Cheapest route:", cheapest_route(12, 5, 21))
    print("Ticket checksum:", ticket_checksum("ticket-123"))

    xml_data = """
    <stops>
        <stop>Central</stop>
        <stop>Market</stop>
    </stops>
    """
    print("Stops:", load_stops(xml_data))


if __name__ == "__main__":
    main()
