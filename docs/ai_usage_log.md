# AI Usage Log

## AI Assistance
AI assistance was used for:
- Python project structure
- Decision-engine implementation
- Test-case generation
- Documentation drafting
- Reviewing business assumptions

## Examples of AI Limitations and Corrections

### 1. Risk Scores
AI-generated scores could be mistaken for RTO probabilities.

Correction: Scores are explicitly described as heuristic scores.

### 2. Financial Impact
Estimated savings could be mistaken for actual savings.

Correction: Dashboard metrics are labelled as estimates based on configurable assumptions.

### 3. Address Interpretation
An LLM could misunderstand Hinglish directions or invent missing details.

Correction: Uncertain results require human review.

## Human Responsibility
Business assumptions, risk weights, thresholds, and final decisions require human validation before production use.