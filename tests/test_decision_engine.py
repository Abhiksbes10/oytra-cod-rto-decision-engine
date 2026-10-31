from src.decision_engine import decide_order, calculate_prepaid_discount
from src.whatsapp_simulator import simulate_whatsapp


def sample_order(**overrides):
    order = {
        "order_id": "TEST001",
        "order_value": 649,
        "customer_prior_orders": 3,
        "customer_prior_rto": 0,
        "state": "Maharashtra",
        "courier": "Delhivery",
        "utm_source": "direct"
    }
    order.update(overrides)
    return order


def test_low_risk_order_ships():
    result = decide_order(sample_order())
    assert result["decision"] == "SHIP_AS_IS"


def test_medium_risk_order_requires_confirmation():
    order = sample_order(customer_prior_rto=1)
    result = decide_order(order)
    assert result["decision"] == "SHIP_AFTER_CONFIRMATION"


def test_high_risk_order_gets_prepaid_nudge():
    order = sample_order(
        customer_prior_rto=1,
        state="Bihar"
    )
    result = decide_order(order)
    assert result["decision"] == "NUDGE_TO_PREPAID"


def test_critical_risk_existing_customer_is_held():
    order = sample_order(
        customer_prior_rto=2,
        state="Bihar",
        courier="Xpressbees",
        utm_source="meta_ads",
        order_value=2000
    )
    result = decide_order(order)
    assert result["decision"] == "HOLD_OR_CANCEL"


def test_new_customer_critical_order_requires_confirmation():
    order = sample_order(
        customer_prior_orders=0,
        customer_prior_rto=2,
        state="Bihar",
        courier="Xpressbees",
        utm_source="meta_ads",
        order_value=2000
    )
    result = decide_order(order)
    assert result["decision"] == "SHIP_AFTER_CONFIRMATION"


def test_whatsapp_yes_confirms():
    order = sample_order(customer_prior_rto=1)
    decision = decide_order(order)
    result = simulate_whatsapp(order, decision, response="YES")
    assert result["outcome"] == "CONFIRMED"


def test_whatsapp_no_cancels():
    order = sample_order(customer_prior_rto=1)
    decision = decide_order(order)
    result = simulate_whatsapp(order, decision, response="NO")
    assert result["outcome"] == "CANCELLED"


def test_whatsapp_no_reply():
    order = sample_order(customer_prior_rto=1)
    decision = decide_order(order)
    result = simulate_whatsapp(order, decision, response="NO_REPLY")
    assert result["outcome"] == "NO_RESPONSE"


def test_prepaid_discount_is_zero_for_non_nudge():
    order = sample_order()
    decision = decide_order(order)
    assert calculate_prepaid_discount(order, decision) == 0


def test_prepaid_nudge_has_discount():
    order = sample_order(
        customer_prior_rto=1,
        state="Bihar"
    )
    decision = decide_order(order)
    assert calculate_prepaid_discount(order, decision) > 0