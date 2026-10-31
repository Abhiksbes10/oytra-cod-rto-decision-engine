import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.decision_engine import decide_order
from src.whatsapp_simulator import simulate_whatsapp


def main():
    data_file = BASE_DIR / "data" / "orders_sample.csv"

    if not data_file.exists():
        print("Dataset not found:", data_file)
        return

    df = pd.read_csv(data_file)

    print("\nOYTRA COD RTO DECISION ENGINE")
    print("=" * 45)

    for _, row in df.head(10).iterrows():
        order = row.to_dict()
        decision = decide_order(order)

        print(f"\nOrder ID: {order.get('order_id')}")
        print(f"Risk score: {decision['risk_score']}")
        print(f"Risk level: {decision['risk_level']}")
        print(f"Decision: {decision['decision']}")
        print(f"Reasons: {decision['reasons']}")

        simulation = simulate_whatsapp(
            order,
            decision,
            seed=42
        )
        print(f"WhatsApp simulation: {simulation['outcome']}")


if __name__ == "__main__":
    main()