# Submission Demo

## 1. What the System Demonstrates

The system demonstrates an AI-assisted cross-border settlement architecture in which payment intent and multiple sources of settlement intelligence are passed through a structured decision boundary.

The final settlement decision is made by a deterministic `DecisionEngine`.

The core principle is:

> Intelligence informs the decision; the deterministic decision engine makes the decision.

---

## 2. End-to-End Flow

```text
Payment Intent
      |
      v
Real Economic Intelligence
      |
      v
Regulatory Evidence
      |
      v
Telegraph MCP Intelligence
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

---

## 3. Demo Execution

The demo executes the settlement workflow using real economic intelligence, regulatory evidence, Telegraph MCP intelligence, deterministic route evaluation, and audit generation.

The observed execution includes:

- Real economic input from Base RPC + CoinGecko
- Economic gate: `PASSED`
- Regulatory gate: `PERMITTED`
- Telegraph MCP intelligence
- Deterministic `DecisionEngine` evaluation
- Route-level evidence checks
- Audit generation

---

## 4. Deterministic Decision Result

The demonstrated execution produced:

```text
Bitcoin | ELIGIBLE_DATA_INCOMPLETE
Base | ELIGIBLE_DATA_INCOMPLETE

## 6. Telegraph Intelligence vs Decision Routes

Telegraph MCP and the deterministic route input serve different architectural roles.

Telegraph provides external intelligence about available settlement context. Its returned route information is preserved as Telegraph intelligence inside `DecisionInput`.

The deterministic decision engine receives its authoritative candidate route set separately through `normalized_routes.py`, which currently obtains route intelligence from `route_intelligence.py`.

Therefore, Telegraph-discovered routes are not automatically substituted into the deterministic decision set.

The demonstrated execution may therefore show:

```text
Telegraph intelligence:
['bitcoin', 'solana']

Deterministic decision routes:
Bitcoin
Base

This preserves the principle that an external intelligence provider does not become the authority that defines or makes the settlement decision.