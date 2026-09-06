# 2-Minute Live Demo

## AI-Assisted BRICS Cross-Border Settlement

This demo shows one complete user-to-recommendation pass for a **$1,000 India → Brazil import payment**.

---

## What the Demo Proves

- A business request becomes a structured Payment Intent.
- Real economic intelligence is obtained from Base RPC + CoinGecko.
- A live Telegraph Miner is accessed through x402.
- Telegraph intelligence is normalized into the settlement decision context.
- Telegraph does **not** make the settlement decision.
- Deterministic regulatory/compliance gates retain authority.
- Unknown regulatory evidence is not fabricated into approval.
- The resulting decision is auditable.

---

# 1. Start the Live Telegraph Miner

Open **Terminal 1**:

```bash
cd ~/AI-Lab/projects/Telegraph-MCP
npx tsx telegraph_mining_agent.ts

```markdown
### Live output

```text

=== TELEGRAPH TEST MINING AGENT ===

Node: http://13.237.89.59:7044
Subnet: 402

Creating x402 payment-aware client...
[telegraph-mcp] EVM payment enabled (network: eip155:84532, from: 0xBD5308b712442a44b0866E7B5B10911e9ad003C7)

Mining trade context...
Raw trade-context response saved to: ./trade_context_response.json
Mining agent status: SUCCESS
Telegraph authority: INTELLIGENCE_ONLY
Settlement authority: DETERMINISTIC_ENGINE
Settlement recommendation: NOT_PERFORMED
Telegraph handoff: VALID
Keys: ['fear_greed', 'funding', 'liquidations', 'positioning', 'prices', 'ts']
Response timestamp: 1788676934016


=== USER / BUSINESS REQUEST ===
Amount: $1,000
Source jurisdiction: India
Destination jurisdiction: Brazil
Counterparty: Brazilian supplier
Purpose: import_payment

"We start with a real business request: a $1,000 import payment from India to a Brazilian supplier. The system converts that request into a structured Payment Intent."


=== CANDIDATE SETTLEMENT PATH ===
Source jurisdiction: India
Destination jurisdiction: Brazil
Infrastructure: UPI
Asset: ETH
Regulatory evidence state: UNKNOWN
Asset linkage state: UNKNOWN
Cross-border capability state: UNKNOWN

"The system discovers a candidate settlement path while keeping regulatory evidence, asset linkage and cross-border capability separate."

=== REAL ECONOMIC INPUT ===
User transaction value: $1000.00
Observed blockchain transaction value: $127.59
Network cost: $0.000859
Source: Base RPC + CoinGecko
Confidence: 1.0

"The economic layer uses real external data from Base RPC and CoinGecko rather than hard-coded demonstration values."

=== ECONOMIC GATE ===
Status: PASSED

"The economic gate passes."

=== REGULATORY GATE ===
Jurisdiction: India
Asset: ETH
Activity: CROSS_BORDER_PAYMENT
Status: UNKNOWN
Regulatory state: UNKNOWN

"The regulatory evidence required for this transaction is currently unknown. The system deliberately preserves that uncertainty instead of inventing regulatory approval."



=== TELEGRAPH INTELLIGENCE ===
Request ID: phase-10.5-telegraph
Routes: ['bitcoin', 'solana']
Settlement decision: NOT MADE BY TELEGRAPH

"Telegraph provides external market intelligence through a live x402-paid Miner. It supplies intelligence such as sentiment, funding, liquidations, positioning and prices."
"Telegraph does not make the settlement decision."


=== SETTLEMENT DECISION ===

Route decisions:
Bitcoin | ELIGIBLE_DATA_INCOMPLETE
  Reason: REGULATORY_STATUS_UNKNOWN
  Evidence source: UNAVAILABLE
  Evidence type: UNKNOWN
  Evidence confidence: 0.0
Base | ELIGIBLE_DATA_INCOMPLETE
  Reason: REGULATORY_STATUS_UNKNOWN
  Evidence source: UNAVAILABLE
  Evidence type: UNKNOWN
  Evidence confidence: 0.0

"The deterministic engine evaluates the candidate routes. Because the regulatory state is unknown, neither route is promoted to a settlement recommendation."
"This is intentional. Market intelligence cannot override a required regulatory gate."

=== DATA PROVENANCE ===
Economic input: REAL
Economic source: Base RPC + CoinGecko
Route network data: REAL
Route risk: TEST
Compliance: REFERENCE
Geopolitical: REFERENCE
Regulatory evidence: UNKNOWN
Settlement path evidence: DISCOVERY

"The system keeps provenance visible. Real economic and network inputs are distinguished from reference and test data."

=== AUDIT ===
Audit file: audit/settlement_audit.json
Audit version: 9.9
Status: WRITTEN

"The decision context is written to an audit artifact, making the outcome explainable and auditable."

Closing Statement

"The key idea is separation of intelligence from authority: real-time intelligence can enrich the decision, AI can explain the result, but deterministic controls retain authority over settlement."

User / Business
      |
      v
Payment Intent
      |
      v
Settlement Path Discovery
      |
      +--------------------+
      |                    |
      v                    v
Real Economic Data    Regulatory Evidence
Base RPC + CoinGecko       |
      |                    |
      +---------+----------+
                |
                v
       Deterministic Gates
                ^
                |
       Live Telegraph Miner
              via x402
                |
                v
       Market Intelligence
   sentiment / funding /
   liquidations / positioning /
   prices
                |
                v
           DecisionInput
                |
                v
      Deterministic Engine
           /          \
          v            v
      Decision        Audit


Telegraph
    |
    +--> INTELLIGENCE_ONLY

AI
    |
    +--> EXPLANATION_ONLY

Deterministic Settlement Engine
    |
    +--> SETTLEMENT AUTHORITY


Live Telegraph Miner
        |
        | x402-paid /trade-context
        v
trade_context_response.json
        |
        v
/tmp/telegraph_trade_context.txt
        |
        v
Telegraph Intelligence Adapter
        |
        v
Normalized Intelligence
        |
        v
DecisionInput
        |
        v
Deterministic Settlement Engine
        |
        v
Settlement Decision + Audit


Why the Demo Does Not Produce a Route Recommendation

The demonstration intentionally produces:
Bitcoin | ELIGIBLE_DATA_INCOMPLETE
Base    | ELIGIBLE_DATA_INCOMPLETE

because:REGULATORY_STATUS_UNKNOWN


This demonstrates that:

Real market intelligence can enter the decision context.
Economic validation can pass.
Regulatory evidence can remain unknown.
The deterministic engine preserves that uncertainty.
External intelligence cannot manufacture regulatory approval.
The system refuses to present an unsupported settlement route as approved.

Verification

Current implementation checkpoint:
Commit:
138e7fb feat: complete end-to-end settlement decision pass

Branch:
main

Remote:
origin/main

Working tree:
clean

Tests:
66 passed in 0.04s
