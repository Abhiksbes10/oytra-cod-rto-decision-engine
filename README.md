# Oytra COD RTO Decision Engine

A Python prototype for classifying Cash on Delivery orders by heuristic RTO risk and recommending fulfillment actions.

## Features

- Configurable heuristic risk scoring
- Four fulfillment recommendations
- Optional LLM-assisted name and address validation
- WhatsApp response simulator
- Prepaid discount calculation
- Streamlit founder dashboard
- Automated tests
- Business memo and decision log

## Project Structure

```text
oytra-rto-assignment/
├── config.json
├── data/
│   └── orders_sample.csv
├── docs/
│   ├── business_memo.md
│   ├── decision_log.md
│   └── ai_usage_log.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── risk_model.py
│   ├── decision_engine.py
│   ├── llm_validator.py
│   ├── whatsapp_simulator.py
│   └── dashboard.py
├── tests/
│   └── test_decision_engine.py
├── requirements.txt
└── README.md