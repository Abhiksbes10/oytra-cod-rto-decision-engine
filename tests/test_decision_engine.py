
import sys
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

from decision_engine import decide_order
from whatsapp_simulator import (
    simulate_whatsapp_response,
    calculate_prepaid_offer,
)


def test_decision_engine_returns_valid_decision():
    order = {
        "customer_prior_rto": 0,
        "customer_prior_orders": 2,
        "state": "Maharashtra",
        "courier": "Delhivery",
        "utm_source": "direct",
        "order_value": 649,
    }

    result = decide_order(order)

    assert result["decision"] in {
        "SHIP_AS_IS",
        "SHIP_AFTER_CONFIRMATION",
        "NUDGE_TO_PREPAID",
        "HOLD_OR_CANCEL",
    }


def test_whatsapp_yes_response():
    result = simulate_whatsapp_response("yes")

    assert result["status"] == "CONFIRMED"
    assert result["next_action"] == "SHIP_ORDER"


def test_whatsapp_no_response():
    result = simulate_whatsapp_response("no")

    assert result["status"] == "CANCELLED_BY_CUSTOMER"


def test_whatsapp_no_reply():
    result = simulate_whatsapp_response("timeout")

    assert result["status"] == "NO_RESPONSE"
    assert result["next_action"] == "MANUAL_REVIEW"


def test_prepaid_discount_calculation():
    result = calculate_prepaid_offer(649, 10)

    assert result["discount_amount"] == 64.9
    assert result["prepaid_amount"] == 584.1
