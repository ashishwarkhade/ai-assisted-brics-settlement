# AI-Assisted BRICS Cross-Border Settlement

## Overview

An AI-assisted cross-border settlement system combining payment intent, intelligence, regulatory evidence, and a deterministic settlement decision engine.

## Core Architecture

User / Business -> Payment Intent -> Intelligence Layer -> Normalized Intelligence -> DecisionInput -> Deterministic DecisionEngine -> Settlement Decision -> Audit

## Decision Boundary

The DecisionEngine validates input, evaluates route eligibility, ranks eligible routes, and produces a recommendation or refusal.

## Telegraph MCP

Telegraph MCP is an intelligence provider and tool infrastructure layer. Telegraph intelligence enters DecisionInput but does not directly make the settlement decision.

## Key Principle

Intelligence informs the decision; the deterministic decision engine makes the decision.

## Testing

Current locked test result: 46 passed in 0.03s.

## Project Status

Data collection has stopped. The project is now in architecture and submission preparation.

## Locked Commit

c866342 - refactor: establish deterministic settlement decision engine
