# Oytra COD RTO Decision Engine

A Python-based prototype that analyzes historical COD orders, evaluates RTO risk, recommends order actions, simulates WhatsApp confirmation, and displays decision summaries through a Streamlit dashboard.

## Features

- Historical order data analysis
- Data quality checks
- Configurable risk scoring
- Four COD decision outcomes
- Optional LLM-assisted customer-name and address validation
- WhatsApp confirmation simulator
- Prepaid discount calculator
- Streamlit founder dashboard
- Automated tests

## Project Structure

```text
oytra-rto-assignment/
├── config.json
├── data/
│   └── orders_sample.csv
├── docs/
│   └── business_memo.md
├── src/
│   ├── main.py
│   ├── risk_model.py
│   ├── llm_validator.py
│   ├── decision_engine.py
│   ├── whatsapp_simulator.py
│   └── dashboard.py
├── tests/
│   └── test_decision_engine.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.12+
- pip

## Setup

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Place `orders_sample.csv` inside the `data/` folder.

## Run Dashboard

```powershell
python -m streamlit run src/dashboard.py
```

## Run Tests

```powershell
python -m pytest tests/ -v
```

## Configuration

Edit `config.json` to adjust risk thresholds, financial assumptions, and prepaid discount settings without modifying Python code.

## LLM Configuration

The LLM validation module requires an OpenAI API key configured through the `OPENAI_API_KEY` environment variable. It is optional and is not required to run the historical dashboard or automated tests.

## Current Prototype Limitations

- Risk scores use manually configured weights and are not calibrated probabilities.
- Dashboard results represent historical simulation, not real-time business operations.
- WhatsApp interactions are simulated; no live WhatsApp integration exists.
- LLM validation requires API credentials and has not been presented as a production integration.
- Financial savings and conversion improvements require controlled pilot measurement.

## Testing

Five automated tests currently pass, covering decision output, WhatsApp responses, and prepaid discount calculations.