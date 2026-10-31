
def simulate_whatsapp_response(response, language="English"):
    messages = {
        "English": "Please confirm your COD order. Reply YES to confirm or NO to cancel.",
        "Hindi": "कृपया अपना COD ऑर्डर कन्फर्म करें। YES या NO में जवाब दें।",
        "Hinglish": "Please apna COD order confirm karein. YES ya NO reply karein."
    }

    response = str(response).strip().lower()

    if response in ("yes", "y"):
        status = "CONFIRMED"
        next_action = "SHIP_ORDER"

    elif response in ("no", "n"):
        status = "CANCELLED_BY_CUSTOMER"
        next_action = "CANCEL_ORDER"

    elif response in ("", "no_reply", "timeout"):
        status = "NO_RESPONSE"
        next_action = "MANUAL_REVIEW"

    else:
        status = "UNCLEAR_RESPONSE"
        next_action = "MANUAL_REVIEW"

    return {
        "message": messages.get(language, messages["English"]),
        "response": response or "no_reply",
        "status": status,
        "next_action": next_action
    }


def calculate_prepaid_offer(order_value, discount_percent):
    discount = round(order_value * discount_percent / 100, 2)

    return {
        "original_amount": round(order_value, 2),
        "discount_percent": discount_percent,
        "discount_amount": discount,
        "prepaid_amount": round(order_value - discount, 2)
    }
