import sys
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.decision_engine import decide_order
from src.whatsapp_simulator import simulate_whatsapp
from src.risk_model import load_config


st.set_page_config(
    page_title="Oytra COD RTO Decision Engine",
    page_icon="📦",
    layout="wide"
)

st.title("Oytra COD RTO Decision Engine")
st.caption("Prototype dashboard | Historical sample-data simulation")

DATA_FILE = BASE_DIR / "data" / "orders_sample.csv"

if not DATA_FILE.exists():
    st.error("Dataset not found: data/orders_sample.csv")
    st.stop()

df = pd.read_csv(DATA_FILE)
config = load_config()

required_columns = [
    "order_id",
    "order_value",
    "customer_prior_orders",
    "customer_prior_rto",
    "state",
    "courier",
    "utm_source"
]

missing = [column for column in required_columns if column not in df.columns]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

decisions = df.apply(
    lambda row: decide_order(row.to_dict()),
    axis=1
)

df["decision"] = decisions.apply(lambda result: result["decision"])
df["risk_score"] = decisions.apply(lambda result: result["risk_score"])
df["risk_level"] = decisions.apply(lambda result: result["risk_level"])

counts = df["decision"].value_counts()

ship_count = int(counts.get("SHIP_AS_IS", 0))
confirm_count = int(counts.get("SHIP_AFTER_CONFIRMATION", 0))
prepaid_count = int(counts.get("NUDGE_TO_PREPAID", 0))
hold_count = int(counts.get("HOLD_OR_CANCEL", 0))

col1, col2, col3, col4 = st.columns(4)

col1.metric("Ship as-is", ship_count)
col2.metric("Confirm first", confirm_count)
col3.metric("Prepaid nudge", prepaid_count)
col4.metric("Hold / cancel", hold_count)

st.divider()
st.subheader("Estimated financial impact")

financials = config["financials"]
simulation = config["simulation"]

rto_loss = (
    financials["forward_shipping"]
    + financials["return_shipping"]
    + financials["packaging_handling"]
    + financials["returned_product_cost"]
    * financials["returned_product_cost_percent"] / 100
)

avoided_rto_estimate = (
    confirm_count
    * simulation["assumed_rto_reduction_after_confirmation_percent"] / 100
    * rto_loss
)

genuine_cancel_rate = (
    simulation["assumed_genuine_order_rate_among_cancelled_percent"] / 100
)

estimated_cancelled_genuine = hold_count * genuine_cancel_rate
gross_margin = (
    financials["product_price"]
    * financials["gross_margin_percent"] / 100
)

estimated_lost_margin = estimated_cancelled_genuine * gross_margin
net_impact = avoided_rto_estimate - estimated_lost_margin

a, b, c = st.columns(3)

a.metric("Estimated RTO cost avoided", f"₹{avoided_rto_estimate:,.0f}")
b.metric("Estimated genuine-order margin lost", f"₹{estimated_lost_margin:,.0f}")
c.metric("Estimated net impact", f"₹{net_impact:,.0f}")

st.caption(
    "These are illustrative estimates based on configurable assumptions "
    "and historical sample data. They are not actual realized savings."
)

st.divider()
st.subheader("Decision distribution")

summary = (
    df["decision"]
    .value_counts()
    .rename_axis("Decision")
    .reset_index(name="Orders")
)

st.bar_chart(summary.set_index("Decision"))

st.subheader("Order-level decision log")

display_columns = [
    column for column in [
        "order_id",
        "order_value",
        "state",
        "courier",
        "utm_source",
        "risk_score",
        "risk_level",
        "decision"
    ]
    if column in df.columns
]

st.dataframe(
    df[display_columns],
    width="stretch",
    hide_index=True
)

st.divider()
st.subheader("Simulate WhatsApp response")

selected_index = st.number_input(
    "Dataset row number",
    min_value=0,
    max_value=len(df) - 1,
    value=0,
    step=1
)

selected_order = df.iloc[int(selected_index)].to_dict()
selected_decision = decide_order(selected_order)

response = st.selectbox(
    "Customer response",
    ["YES", "NO", "NO_REPLY"]
)

if st.button("Run WhatsApp simulation"):
    result = simulate_whatsapp(
        selected_order,
        selected_decision,
        response=response
    )
    st.json(result)