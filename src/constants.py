MEASUREMENTS = {
    "cup": "cup",
    "cups": "cup",
    "tbsp": "tablespoon",
    "tablespoon": "tablespoon",
    "tsp": "teaspoon",
    "teaspoons": "teaspoon",
    "pounds": "pound",
    "pound": "pound",
    "kg": "kilogram",
    "grams": "gram",
    "g": "gram",
    "large": "large",
    "small": "small",
    "medium": "medium",
    "oz": "ounce",
    "ounces": "ounce",
    "liters": "liter",
    "liter": "liter",
    "ml": "milliliter",
    "quart": "quart",
    "quarts": "quart",
    "pinch": "pinch",
    "dash": "dash",
}

def parse_ingredient(line):
    parts = line.strip().split(' ', 1)  # Split into quantity and description
    quantity = parts[0].strip() if len(parts) > 1 else None
    description = parts[1].strip() if len(parts) > 1 else parts[0].strip()
    measurement = None

    # Check for measurement units in the description
    for measurement_unit in MEASUREMENTS:
        if description.lower().startswith(measurement_unit):
            measurement = measurement_unit
            description = description[len(measurement_unit):].strip()
            break

    return quantity, measurement, description