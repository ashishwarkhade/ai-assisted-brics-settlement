# System Architecture

## 1. Purpose

The system is an AI-assisted cross-border settlement architecture for BRICS payment scenarios.

Its purpose is to combine payment intent with multiple sources of settlement intelligence and then apply a deterministic decision boundary to determine whether a settlement route is eligible for recommendation.

The architecture separates intelligence gathering from the final settlement decision.

---

## 2. High-Level Architecture

```text
User / Business
       |
       v
Payment Intent
       |
       v
Intelligence Layer
       |
       +-- Transaction / Blockchain Intelligence
       +-- Route Intelligence
       +-- Financial / Market Intelligence
       +-- Regulatory Evidence
       +-- Telegraph MCP Intelligence
       |
       v
Normalized Intelligence
       |
       v
DecisionInput
       |
       v
Deterministic DecisionEngine
       |
       +-- Validate Input
       +-- Evaluate Routes
       +-- Rank Eligible Routes
       +-- Recommend / Refuse
       |
       v
Settlement Decision
       |
       v
Audit
```

---

## 3. Payment Intent

Payment intent represents the requested transaction independently from the eventual settlement decision.

It establishes the requirements and constraints that the settlement process must satisfy.

The architectural distinction is:

```text
PaymentIntent != SettlementDecision
```

The intent describes what the user or business wants to accomplish.

The decision engine determines whether an eligible settlement route can satisfy that intent using the available evidence.

---

## 4. Intelligence Layer

The intelligence layer gathers information required to evaluate potential settlement routes.

The project contains intelligence from several sources, including:

- Transaction intelligence
- Blockchain and network information
- Route intelligence
- Financial and market information
- Regulatory evidence
- Telegraph MCP intelligence

These sources are not themselves the settlement decision.

Their output is normalized and supplied to the decision boundary as structured decision input.

---

## 5. Telegraph MCP

Telegraph MCP acts as an intelligence provider and tool infrastructure layer.

The integration path is:

```text
Telegraph MCP
      |
      v
Telegraph Intelligence
      |
      v
DecisionInput
      |
      v
DecisionEngine
```

Telegraph intelligence is deliberately kept separate from the deterministic settlement decision.

The integration must not allow Telegraph intelligence to directly become a settlement decision, recommendation, or route ranking result.

Relevant integration components include:

```text
telegraph_intelligence_adapter.py
telegraph_decision_integration.py
telegraph_trade_context_provider.py
```

---

## 6. Intelligence Normalization

Different intelligence providers can expose information in different formats.

The architecture therefore places normalization between external intelligence and the decision boundary.

```text
External Sources
       |
       v
Provider-specific Intelligence
       |
       v
Normalized Intelligence
       |
       v
DecisionInput
```

This allows external intelligence providers to evolve without making the deterministic decision engine provider-specific.

---

## 7. DecisionInput

`DecisionInput` establishes the boundary between intelligence and deterministic decision-making.

It carries the information required by the decision engine while preserving the separation between transaction information, intelligence, regulatory evidence, Telegraph intelligence, and the settlement decision.

Telegraph intelligence can coexist with the core transaction and regulatory information without replacing it.

---

## 8. Deterministic Decision Engine

The central decision boundary is implemented by `DecisionEngine`.

Its main stages are:

```text
validate_input()
       |
       v
evaluate_routes()
       |
       v
rank_routes()
       |
       v
recommend()
```

The complete workflow is exposed through `decide()`.

The engine does not ask an external intelligence provider to make the final settlement decision.

Instead, it evaluates structured inputs against deterministic route and policy conditions.

---

## 9. Route Eligibility

A route must first pass the eligibility boundary before it can be ranked.

The engine can exclude routes when required conditions are not satisfied.

Examples include:

- Policy rejection
- Regulatory ineligibility
- Insufficient evidence
- Unavailable route cost
- Other required decision data being unknown

Only routes that satisfy the eligibility boundary proceed to deterministic ranking.

This prevents an unavailable or insufficiently evidenced route from becoming a recommendation merely because it appears attractive on another metric.

---

## 10. Deterministic Ranking

After eligibility evaluation, eligible routes can be ranked deterministically.

The ranking stage operates on the routes that survived evaluation rather than on every discovered route.

This creates the following boundary:

```text
All Candidate Routes
        |
        v
Eligibility Evaluation
        |
        +---- Rejected / Unknown
        |
        v
Eligible Routes
        |
        v
Deterministic Ranking
        |
        v
Recommendation
```

---

## 11. Recommendation and Refusal

The engine can produce a recommendation when an eligible route exists.

It can also produce no recommendation when the available evidence or policy conditions do not justify one.

This is an intentional property of the architecture.

In particular:

```text
Unknown evidence
      !=
Permission to recommend
```

The system therefore distinguishes between a route being technically observable and a route being sufficiently supported for settlement recommendation.

---

## 12. Regulatory Evidence

Regulatory information is represented separately from the final settlement decision.

The regulatory layer can explicitly represent uncertainty.

Where regulatory evidence is unknown or insufficient for the required decision, the engine can avoid producing a settlement recommendation.

This prevents missing regulatory information from being silently interpreted as approval.

---

## 13. Auditability

The settlement workflow retains decision-related evidence through the audit layer.

The conceptual flow is:

```text
Payment Intent
      |
      v
Evidence
      |
      v
DecisionInput
      |
      v
DecisionEngine
      |
      v
Settlement Decision
      |
      v
Audit
```

The objective is to make the resulting decision traceable to the information and constraints used by the decision process.

---

## 14. Architectural Separation

The architecture deliberately separates four responsibilities:

### Intelligence

Find and provide relevant information.

### Normalization

Convert provider-specific information into structured decision input.

### Decision

Apply deterministic eligibility, ranking, and recommendation rules.

### Audit

Retain the information necessary to understand the resulting settlement decision.

This separation reduces the risk of allowing an intelligence provider to become the decision authority.

---

## 15. Current Implementation Boundary

The current implementation includes:

```text
payment_intent.py
decision_input.py
decision_engine.py
settlement_decision.py
policy_intelligence.py
brics_regulatory_evidence.py
telegraph_intelligence_adapter.py
telegraph_decision_integration.py
audit/
```

The deterministic decision-engine architecture was established in:

```text
c866342
refactor: establish deterministic settlement decision engine
```

The architecture README was subsequently added in:

```text
6c6a1b2
docs: add project architecture README
```

---

## 16. Validation Baseline

The current automated test baseline is:

```text
46 passed in 0.03s
```

The decision-engine tests cover, among other areas:

- Input validation
- Eligible route ranking
- Deterministic cost ordering
- Rejected-route exclusion
- Unknown-cost exclusion
- Recommendation behavior
- No-recommendation behavior
- Regulatory uncertainty
- Telegraph separation from route ranking

---

## 17. Core Principle

The system can be summarized as:

```text
AI / External Tools / Live Data
              |
              v
        Intelligence
              |
              v
       DecisionInput
              |
              v
    Deterministic DecisionEngine
              |
              v
      Settlement Decision
              |
              v
             Audit
```

> **Intelligence informs the decision; the deterministic decision engine makes the decision.**
