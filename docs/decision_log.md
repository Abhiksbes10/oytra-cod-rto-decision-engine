# Decision Log

| Rule | Condition | Action |
|---|---|---|
| R1 | Risk score <= 30 | Ship as-is |
| R2 | Risk score 31–55 | WhatsApp confirmation |
| R3 | Risk score 56–75 | Prepaid nudge |
| R4 | Risk score > 75 and prior orders > 0 | Hold/cancel |
| R5 | Risk score > 75 and no prior orders | WhatsApp confirmation |

## Risk Inputs
- Previous RTO count
- State
- Courier
- Acquisition source
- Order value

## Important
Risk scores are heuristic scores, not calibrated RTO probabilities. Thresholds and weights are configurable in config.json.