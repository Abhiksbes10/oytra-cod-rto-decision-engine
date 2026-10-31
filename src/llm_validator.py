import os


def validate_order_text(customer_name, address):
    """
    Optional LLM validation.
    No API key means the rule-based system continues without LLM validation.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {
            "status": "NOT_CONFIGURED",
            "name_quality": "NOT_CHECKED",
            "address_quality": "NOT_CHECKED",
            "interpretation": "LLM validation unavailable"
        }

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You validate ecommerce customer names and delivery "
                        "addresses. Interpret Hinglish address instructions. "
                        "Do not invent missing details. Return JSON with keys: "
                        "name_quality, address_quality, interpretation, "
                        "needs_manual_review."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Customer name: {customer_name}\n"
                        f"Delivery address: {address}"
                    )
                }
            ]
        )

        import json
        result = json.loads(response.choices[0].message.content)

        return {
            "status": "SUCCESS",
            **result
        }

    except Exception as error:
        return {
            "status": "ERROR",
            "name_quality": "NOT_CHECKED",
            "address_quality": "NOT_CHECKED",
            "interpretation": str(error)
        }