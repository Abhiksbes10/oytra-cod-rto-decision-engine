
from src.risk_model import calculate_risk


def decide_order(order):
    risk = calculate_risk(order)

    score = risk["risk_score"]
    prior_orders = int(order.get("customer_prior_orders", 0) or 0)

    if score <= 30:
        decision = "SHIP_AS_IS"

    elif score <= 55:
        decision = "SHIP_AFTER_CONFIRMATION"

    elif score <= 75:
        decision = "NUDGE_TO_PREPAID"

    else:
        # Protect first-time customers from automatic cancellation.
        if prior_orders == 0:
            decision = "SHIP_AFTER_CONFIRMATION"
        else:
            decision = "HOLD_OR_CANCEL"

    return {
        "decision": decision,
        "risk_score": score,
        "risk_level": risk["risk_level"],
        "reasons": risk["reasons"]
    }


def calculate_prepaid_discount(order, decision):
    from src.risk_model import load_config

    config = load_config()
    discounts = config["prepaid_discount"]

    if decision["decision"] != "NUDGE_TO_PREPAID":
        return 0

    level = decision.get("risk_level", "MEDIUM")
    percent = discounts["high_risk"] if level in ("HIGH", "CRITICAL") else discounts["medium_risk"]
    value = float(order.get("order_value", 0) or 0)

    return round(value * percent / 100, 2)
