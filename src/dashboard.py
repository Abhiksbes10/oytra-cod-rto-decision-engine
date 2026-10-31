
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_engine import decide_order

DATA_FILE = BASE_DIR / "data" / "orders_sample.csv"

st.set_page_config(page_title="Oytra RTO Dashboard", layout="wide")
st.title("Oytra — COD & RTO Decision Dashboard")

df = pd.read_csv(DATA_FILE)
df["order_datetime"] = pd.to_datetime(df["order_datetime"], errors="coerce")

results = df.apply(
    lambda order: decide_order(order),
    axis=1
)

df["decision"] = results.apply(lambda result: result["decision"])

labels = {
    "SHIP_AS_IS": "Ship as-is",
    "SHIP_AFTER_CONFIRMATION": "Ship after confirmation",
    "NUDGE_TO_PREPAID": "Nudge to prepaid",
    "HOLD_OR_CANCEL": "Hold / cancel"
}

counts = df["decision"].value_counts()

st.subheader("Order decision summary")

columns = st.columns(4)

for column, decision in zip(columns, labels):
    column.metric(labels[decision], int(counts.get(decision, 0)))

st.subheader("Decision distribution")

chart_data = pd.DataFrame({
    "Decision": [labels[key] for key in labels],
    "Orders": [int(counts.get(key, 0)) for key in labels]
})

st.bar_chart(chart_data.set_index("Decision"))

st.subheader("Recent order decisions")

display_columns = [
    "order_id",
    "customer_name",
    "state",
    "order_value",
    "decision"
]

st.dataframe(
    df[display_columns].tail(20),
    use_container_width=True
)

st.caption(
    "This is a historical decision simulation across the supplied dataset, "
    "not verified real-time savings or actual yesterday's performance."
)
