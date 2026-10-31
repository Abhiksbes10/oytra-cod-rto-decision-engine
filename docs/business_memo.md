# Oytra — COD RTO Reduction Strategy

**Prepared for:** Oytra  
**Project:** COD Risk Decision Engine  
**Dataset:** 2,018 historical orders

## 1. Executive Summary

The objective is to reduce Return to Origin (RTO) losses without unnecessarily cancelling genuine customer orders.

The historical dataset contains 2,018 orders, with 573 RTO orders among 2,017 completed orders, representing an RTO rate of approximately 28.4%.

I recommend a risk-based COD decision system with four outcomes:

1. Ship as-is.
2. Ship after WhatsApp confirmation.
3. Nudge the customer towards prepaid payment.
4. Hold or cancel only when multiple strong risk signals justify intervention.

The system should protect revenue while reducing avoidable logistics losses.

## 2. Important Data Findings

### Finding 1: Previous RTO history is a strong risk signal

| Previous RTOs | Orders | RTO rate |
|---|---:|---:|
| 0 | 1,872 | 27.19% |
| 1 | 111 | 34.23% |
| 2 | 34 | 76.47% |

Customers with two previous RTOs have a substantially higher historical RTO rate. However, this group contains only 34 orders, so further validation is required before using it for automatic cancellation.

### Finding 2: Delivery geography has substantial variation

| State | RTO rate |
|---|---:|
| Bihar | 53.42% |
| Uttar Pradesh | 44.67% |
| Madhya Pradesh | 38.46% |
| Maharashtra | 17.95% |

This suggests that delivery location should influence risk scoring. State-level patterns should not become blanket delivery restrictions.

### Finding 3: Acquisition channels have different RTO outcomes

| Acquisition source | RTO rate |
|---|---:|
| Meta Ads | 31.32% |
| Instagram Organic | 29.36% |
| Google Ads | 28.05% |
| Influencer | 26.64% |
| WhatsApp Broadcast | 26.47% |
| Direct | 22.66% |

Meta Ads has the highest observed RTO rate, while Direct has the lowest. However, Meta Ads also contributes 779 orders, so automatically rejecting this channel could harm acquisition.

### Additional finding: Order value matters

Orders above ₹1,500 have a 38.87% RTO rate, compared with 20.19% for orders between ₹1,000 and ₹1,500.

## 3. Financial Analysis

| Metric | Amount |
|---|---:|
| Average product selling price | ₹649 |
| Gross margin | 62% |
| Gross profit per delivered order | ₹402.38 |
| Forward shipping | ₹65 |
| Return shipping | ₹65 |
| Packaging and handling | ₹25 |
| Returned product loss | ₹14.40 |
| Total estimated loss per RTO | ₹169.40 |

The shipping-only break-even RTO probability is approximately 70.37%.

This means a high-risk order should not automatically be cancelled just because its RTO probability is elevated.

The ₹300+ customer acquisition cost also matters when evaluating the longer-term customer relationship. However, acquisition cost is already incurred when an order arrives, so it should not simply be added to the marginal shipping calculation.

## 4. Recommended Decision Policy

| Risk category | Recommended action |
|---|---|
| Low | Ship as-is |
| Medium | WhatsApp confirmation |
| High | Encourage prepaid payment |
| Critical | Hold for manual review or cancellation |

Additional rules:

- Do not reject customers based only on their state or acquisition channel.
- Use previous RTO history as one risk signal.
- Validate incomplete addresses and suspicious customer details.
- Provide manual review for uncertain cases.
- Keep risk thresholds configurable.

## 5. Historical Simulation

The current decision engine was run against all 2,018 historical orders.

| Decision | Orders |
|---|---:|
| Ship as-is | 1,822 |
| Ship after confirmation | 185 |
| Nudge to prepaid | 10 |
| Hold / cancel | 1 |

These are model-generated historical decision counts, not verified avoided RTOs or actual financial savings.

The next validation step is to compare each decision against historical delivery outcomes and measure false positives and false negatives.

## 6. Operations vs Marketing

Operations wants to reduce avoidable shipping and return costs.

Marketing wants to protect genuine customers acquired through paid channels.

The proposed system balances these interests by applying interventions before cancellation.

WhatsApp confirmation and prepaid nudges create opportunities to retain genuine customers while identifying potentially risky orders.

Automatic cancellation should remain a last resort.

## 7. Failure Modes and Detection

| Failure mode | Detection or mitigation |
|---|---|
| Genuine order flagged as risky | Measure false-positive rate and provide manual review |
| Fake or incomplete address | Address validation and LLM-assisted review |
| Hinglish address incorrectly flagged | Preserve local-language delivery information |
| Historical data imbalance | Monitor sample sizes and validate on new orders |
| Incorrect phone number | Phone-number validation |
| Courier performance changes | Monitor courier-specific RTO rates |
| Customer does not respond | Use a defined confirmation timeout and manual review |

LLM output should be treated as a validation signal, not an automatic cancellation decision.

## 8. Two-Week Implementation Plan

**Week 1**
- Clean and normalize historical order data.
- Validate risk rules against historical outcomes.
- Improve customer, address and phone validation.
- Implement WhatsApp confirmation workflow.
- Test prepaid discount economics.

**Week 2**
- Integrate the decision engine with Shopify order events.
- Build the founder dashboard using actual order outcomes.
- Run a controlled pilot with a subset of COD orders.
- Measure RTO rate, conversion, cancellation rate and net financial impact.
- Review results with Operations and Marketing before expanding.

## 9. Final Recommendation

Implement a configurable, risk-based COD decision engine with WhatsApp confirmation and prepaid nudges.

Avoid blanket customer or location restrictions.

The system should optimize for net business value: reducing avoidable RTO losses while preserving genuine customer orders and acquisition opportunities.

**Important limitation:** The current implementation is a prototype using manually configured risk weights. Its scores are not calibrated RTO probabilities, and its simulated decisions must be validated before production deployment.