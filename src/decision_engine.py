from src.risk_model import calculate_risk, load_config


def decide_order(order):
    risk = calculate_risk(order)
    config = load_config()

    score = risk["risk_score"]
    prior_orders = int(order.get("customer_prior_orders", 0) or 0)
    thresholds = config["risk_thresholds"]

    if score <= thresholds["low_max"]:
        decision = "SHIP_AS_IS"

    elif score <= thresholds["medium_max"]:
        decision = "SHIP_AFTER_CONFIRMATION"

    elif score <= thresholds["high_max"]:
        decision = "NUDGE_TO_PREPAID"

    elif prior_orders == 0:
        decision = "SHIP_AFTER_CONFIRMATION"

    else:
        decision = "HOLD_OR_CANCEL"

    return {
        "decision": decision,
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "reasons": risk["reasons"]
    }


def calculate_prepaid_discount(order, decision):
    config = load_config()
    discounts = config["prepaid_discount"]

    if decision["decision"] != "NUDGE_TO_PREPAID":
        return 0

    if decision["risk_level"] == "CRITICAL":
        discount_percent = discounts["high_risk"]
    else:
        discount_percent = discounts["medium_risk"]

    order_value = float(order.get("order_value", 0) or 0)
    return round(order_value * discount_percent / 100, 2)