# Oytra COD RTO Decision Engine
## Founder Business Memo

### Executive Summary

The sample contains 2,018 COD orders. Of the 2,017 orders with a completed delivery outcome, 573 were RTO, representing approximately 28.4%.

The proposed decision engine uses historical order attributes to assign a heuristic risk score and recommend one of four actions:

- Ship as-is
- Ship after WhatsApp confirmation
- Nudge to prepaid
- Hold or cancel

The objective is to reduce avoidable RTO costs without unnecessarily rejecting genuine customers.

### 1. Key Findings

**Finding 1 — Previous RTO history is a useful risk signal.**

| Previous RTOs | Orders | RTO rate |
|---|---:|---:|
| 0 | 1,872 | 27.19% |
| 1 | 111 | 34.23% |
| 2 | 34 | 76.47% |

Customers with two previous RTOs had a substantially higher observed RTO rate. The proposed model therefore assigns a higher risk weight to repeat RTO history.

**Finding 2 — RTO rates vary by state.**

| State | Observed RTO rate |
|---|---:|
| Bihar | 53.42% |
| Uttar Pradesh | 44.67% |
| Madhya Pradesh | 38.46% |
| Assam | 34.92% |
| Maharashtra | 17.95% |

State is used as a risk signal, not as a reason to automatically reject an order. The model should be monitored for unfair geographic outcomes.

**Finding 3 — Courier and acquisition source performance varies.**

Courier RTO rates:

| Courier | RTO rate |
|---|---:|
| Xpressbees | 31.23% |
| Ecom Express | 30.16% |
| BlueDart | 28.88% |
| Shadowfax | 28.44% |
| Delhivery | 25.92% |

Acquisition source RTO rates:

| Source | RTO rate |
|---|---:|
| Meta Ads | 31.32% |
| Instagram Organic | 29.36% |
| Google Ads | 28.05% |
| Influencer | 26.64% |
| WhatsApp Broadcast | 26.47% |
| Direct | 22.66% |

These are historical correlations. They do not prove that a courier or marketing channel causes an RTO.

### 2. Financial Impact

Given business assumptions:

- Product price: ₹649
- Gross margin: 62%
- Forward shipping: ₹65
- Return shipping: ₹65
- Packaging and handling: ₹25
- Returned-product loss assumption: 8% of ₹180 = ₹14.40

Estimated RTO cost:

₹65 + ₹65 + ₹25 + ₹14.40 = **₹169.40 per RTO**

Estimated prepaid RTO cost at a 4% RTO rate:

₹169.40 × 4% = **₹6.78 per prepaid order**

These are estimates based on the supplied assumptions, not verified accounting figures.

### 3. Decision Rules

| Risk score | Action |
|---|---|
| 0–30 | Ship as-is |
| 31–55 | WhatsApp confirmation |
| 56–75 | Prepaid nudge |
| 76–100 | Hold/cancel, except new customers receive confirmation |

The thresholds and weights are configurable in `config.json`.

The model uses previous RTO history, state, courier, acquisition source, and order value. It does not use an LLM to calculate risk.

### 4. Operations vs Marketing Trade-off

Operations should reduce avoidable delivery and return costs. Marketing should protect genuine customer conversion and avoid unnecessary cancellation.

A strict cancellation policy may reduce RTOs but also reject genuine orders. The safer approach is to confirm uncertain orders and reserve cancellation for the highest-risk cases.

### 5. Failure Modes and Detection

| Failure mode | Detection / mitigation |
|---|---|
| Incorrect or incomplete address | Address validation and manual review |
| Hinglish address misunderstood | LLM-assisted interpretation with human review |
| Genuine customer does not respond | Avoid automatic cancellation solely due to no reply |
| Incorrect risk classification | Review decision outcomes and recalibrate weights |
| State-level bias | Monitor false positives and approval rates by state |
| Courier performance changes | Recalculate courier-level RTO rates regularly |
| LLM unavailable | Continue with deterministic rules and flag manual review |

### 6. Two-Week Rollout Plan

**Week 1**
- Validate data quality and clean order fields.
- Run the model in shadow mode without changing fulfillment.
- Review high-risk orders with the operations team.
- Compare model decisions against actual outcomes.

**Week 2**
- Pilot WhatsApp confirmation on a limited eligible segment.
- Track response, cancellation, prepaid conversion, and RTO outcomes.
- Compare genuine-order loss against avoided RTO cost.
- Adjust thresholds based on measured results.

### 7. Limitations

- This is a prototype based on a historical sample, not a production integration.
- Risk scores are heuristic and are not calibrated probabilities.
- WhatsApp responses and prepaid conversion are simulated.
- Financial impact is estimated from configurable assumptions.
- The dashboard summarizes the supplied historical dataset; it does not represent live yesterday's orders.
- No live Shopify, courier, or WhatsApp API is connected.

### Recommendation

Start with shadow-mode evaluation and human review. Only introduce automated fulfillment actions after the model has been tested against real outcomes and false-positive rates.