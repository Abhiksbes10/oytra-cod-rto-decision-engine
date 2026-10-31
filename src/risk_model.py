
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def calculate_risk(order):
    score = 0
    reasons = []

    # Previous customer RTO history
    prior_rto = int(order.get("customer_prior_rto", 0) or 0)

    if prior_rto >= 2:
        score += 40
        reasons.append("Customer has 2 or more previous RTOs")
    elif prior_rto == 1:
        score += 15
        reasons.append("Customer has 1 previous RTO")

    # Delivery location
    state = str(order.get("state", "")).strip().lower()

    state_risk = {
        "bihar": 25,
        "uttar pradesh": 20,
        "madhya pradesh": 15,
        "assam": 12
    }

    if state in state_risk:
        score += state_risk[state]
        reasons.append(f"Historically higher RTO location: {state}")

    # Courier
    courier = str(order.get("courier", "")).strip().lower()

    courier_risk = {
        "xpressbees": 8,
        "ecom express": 6
    }

    if courier in courier_risk:
        score += courier_risk[courier]
        reasons.append(f"Higher historical RTO courier: {courier}")

    # Acquisition source
    source = str(order.get("utm_source", "")).strip().lower()

    if source == "meta_ads":
        score += 6
        reasons.append("Meta Ads orders have higher historical RTO")

    # Order value
    try:
        order_value = float(order.get("order_value", 0) or 0)
    except (TypeError, ValueError):
        order_value = 0

    if order_value > 1500:
        score += 8
        reasons.append("Order value exceeds ₹1,500")

    # Keep score within 0–100
    score = min(score, 100)

    config = load_config()
    thresholds = config["risk_thresholds"]

    if score <= thresholds["low_max"]:
        risk_level = "LOW"
    elif score <= thresholds["medium_max"]:
        risk_level = "MEDIUM"
    elif score <= thresholds["high_max"]:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons
    }
