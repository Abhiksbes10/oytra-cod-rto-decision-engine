import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_risk(order):
    config = load_config()
    weights = config["risk_weights"]

    score = 0
    reasons = []

    prior_rto = int(order.get("customer_prior_rto", 0) or 0)

    if prior_rto >= 2:
        score += weights["prior_rto_2_plus"]
        reasons.append("Two or more previous RTOs")
    elif prior_rto == 1:
        score += weights["prior_rto_1"]
        reasons.append("One previous RTO")

    state = str(order.get("state", "")).strip().lower()
    points = weights["state"].get(state, 0)

    if points:
        score += points
        reasons.append(f"State risk factor: {state}")

    courier = str(order.get("courier", "")).strip().lower()
    points = weights["courier"].get(courier, 0)

    if points:
        score += points
        reasons.append(f"Courier risk factor: {courier}")

    source = str(order.get("utm_source", "")).strip().lower()
    points = weights["source"].get(source, 0)

    if points:
        score += points
        reasons.append(f"Acquisition source risk factor: {source}")

    try:
        order_value = float(order.get("order_value", 0) or 0)
    except (TypeError, ValueError):
        order_value = 0

    if order_value > weights["high_order_value_min"]:
        score += weights["high_order_value_points"]
        reasons.append("High-value order")

    score = min(score, 100)

    thresholds = config["risk_thresholds"]

    if score <= thresholds["low_max"]:
        level = "LOW"
    elif score <= thresholds["medium_max"]:
        level = "MEDIUM"
    elif score <= thresholds["high_max"]:
        level = "HIGH"
    else:
        level = "CRITICAL"

    return {
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons
    }