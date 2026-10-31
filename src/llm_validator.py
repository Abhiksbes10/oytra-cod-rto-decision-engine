
import json
import os

from openai import OpenAI


def validate_order_text(customer_name, address):
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "status": "NOT_CONFIGURED",
            "reason": "OpenAI API key is not configured."
        }

    client = OpenAI()

    prompt = f"""
    Review this COD order for obvious data-quality issues.

    Customer name: {customer_name}
    Delivery address: {address}

    Check for:
    - Fake or test names
    - Gibberish or incomplete addresses
    - Unclear delivery directions

    Do not reject an order based only on a local-language
    or Hinglish address.

    Return JSON with:
    {{
      "suspicious": true or false,
      "reason": "short explanation"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You validate COD order text. Be conservative."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    except Exception as error:
        return {
            "status": "ERROR",
            "reason": str(error)
        }
