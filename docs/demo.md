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
