import random
from src.risk_model import load_config
from src.decision_engine import calculate_prepaid_discount


def simulate_whatsapp(order, decision, response=None, seed=None):
    config = load_config()
    settings = config["simulation"]

    rng = random.Random(seed)

    language = "Hinglish"
    if response is None:
        response = rng.choices(
            ["YES", "NO", "NO_REPLY"],
            weights=[
                settings["confirmation_response_probability"] * 0.7,
                settings["confirmation_response_probability"] * 0.3,
                1 - settings["confirmation_response_probability"]
            ],
            k=1
        )[0]

    discount = calculate_prepaid_discount(order, decision)

    if decision["decision"] == "SHIP_AS_IS":
        outcome = "SHIP"
    elif decision["decision"] == "HOLD_OR_CANCEL":
        outcome = "HOLD"
    elif decision["decision"] == "NUDGE_TO_PREPAID":
        converted = rng.random() < settings["prepaid_conversion_probability"]
        outcome = "PREPAID" if converted else "COD"
    elif response == "YES":
        outcome = "CONFIRMED"
    elif response == "NO":
        outcome = "CANCELLED"
    else:
        outcome = "NO_RESPONSE"

    return {
        "language": language,
        "response": response,
        "confirmation_window_hours": settings["confirmation_window_hours"],
        "prepaid_discount": discount,
        "outcome": outcome
    }