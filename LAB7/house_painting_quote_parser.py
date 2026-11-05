
def clean_colour_name(name):
    """
    Converts a colour name into a lowercase code.
    Handles invalid and empty inputs safely.
    """
    if not isinstance(name, str):
        return ""

    return '_'.join(name.strip().lower().split())


def room_area(text):
    """
    Converts LENGTHxWIDTH into square feet.
    Returns 0 for invalid dimensions.
    """
    if not isinstance(text, str):
        return 0

    parts = text.lower().strip().split('x')

    if len(parts) != 2:
        return 0

    try:
        length = int(parts[0].strip())
        width = int(parts[1].strip())

        if length < 0 or width < 0:
            return 0

        return length * width

    except ValueError:
        return 0


def total_wall_area(text):
    """
    Adds valid wall areas separated by semicolons.
    Ignores invalid entries safely.
    """
    if not isinstance(text, str):
        return 0

    total = 0

    for area in text.split(';'):
        area = area.strip()

        try:
            value = int(area)

            if value >= 0:
                total += value

        except ValueError:
            continue

    return total


def main():
    print("==== Running clean_colour_name ====")
    value = input("Enter a paint colour name (e.g. Ocean Blue): ")
    print("Colour code:", clean_colour_name(value))

    print("\n==== Running room_area ====")
    value = input("Enter room size as LENGTHxWIDTH in feet (e.g. 12x10): ")
    print("Room area (sq ft):", room_area(value))

    print("\n==== Running total_wall_area ====")
    value = input("Enter wall areas separated by ; (e.g. 120;95;110): ")
    print("Total wall area (sq ft):", total_wall_area(value))


if __name__ == "__main__":
    main()
