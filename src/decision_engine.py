from src.risk_model import calculate_risk, load_config


def decide_order(order):
    risk = calculate_risk(order)
    config = load_config()

    score = risk["risk_score"]
    thresholds = config["risk_thresholds"]

    if score <= thresholds["low_max"]:
        decision = "SHIP_AS_IS"
    elif score <= thresholds["medium_max"]:
        decision = "SHIP_AFTER_CONFIRMATION"
    elif score <= thresholds["high_max"]:
        decision = "NUDGE_TO_PREPAID"
    else:
        prior_orders = int(order.get("customer_prior_orders", 0) or 0)
        decision = (
            "SHIP_AFTER_CONFIRMATION"
            if prior_orders == 0
            else "HOLD_OR_CANCEL"
        )

    return {
        "decision": decision,
        "risk_score": score,
        "risk_level": risk["risk_level"],
        "reasons": risk["reasons"]
    }


def calculate_prepaid_discount(order, decision):
    config = load_config()
    discounts = config["prepaid_discount"]

    if decision["decision"] != "NUDGE_TO_PREPAID":
        return 0

    level = decision.get("risk_level", "MEDIUM")
    percent = (
        discounts["high_risk"]
        if level in ("HIGH", "CRITICAL")
        else discounts["medium_risk"]
    )

    value = float(order.get("order_value", 0) or 0)
    return round(value * percent / 100, 2)
