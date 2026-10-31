
import pandas as pd

from risk_model import calculate_risk


def main():
    data_path = "data/orders_sample.csv"
    df = pd.read_csv(data_path)

    print("\n========== RISK MODEL TEST ==========")

    sample_orders = df.head(10)

    for _, order in sample_orders.iterrows():
        result = calculate_risk(order)

        print(f"\nOrder ID: {order['order_id']}")
        print(f"Customer: {order['customer_name']}")
        print(f"Risk Score: {result['risk_score']}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Reasons: {', '.join(result['reasons']) or 'No major risk signals'}")

    print("\n=====================================")


if __name__ == "__main__":
    main()
