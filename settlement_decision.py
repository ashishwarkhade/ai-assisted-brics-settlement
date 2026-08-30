import json
from datetime import datetime, timezone

from brics_regulatory_evidence import (
    build_regulatory_evidence,
    determine_regulatory_state,
)

from normalized_routes import get_normalized_routes
from policy_intelligence import build_policy_intelligence
from economic_intelligence import build_economic_intelligence
from decision_explanation import build_decision_explanation
from telegraph_decision_integration import build_telegraph_decision_input
from decision_engine import DecisionEngine
from payment_intent import (
    build_payment_intent,
    validate_payment_intent,
)


# ============================================================
# DECISION POLICY
# ============================================================

MAX_RISK = 50

AUDIT_FILE = "audit/settlement_audit.json"



# ============================================================
# BUILD EVIDENCE AUDIT RECORD
# ============================================================

def build_evidence_audit_record(evidence):
    """
    Convert any supported evidence structure into a safe
    audit representation.

    Phase 8 policy evidence uses:
        value
        source
        source_type
        confidence

    Phase 9 regulatory evidence uses:
        jurisdiction
        asset
        activity
        status
        source
        source_type
        confidence
        evidence_text

    This function deliberately does NOT assume that every
    evidence object contains a 'value' field.
    """

    if not isinstance(evidence, dict):
        return evidence

    record = {}

    # --------------------------------------------------------
    # Common provenance fields
    # --------------------------------------------------------

    for field in (
        "source",
        "source_type",
        "confidence",
    ):

        if field in evidence:

            record[field] = evidence[field]

    # --------------------------------------------------------
    # Phase 8 policy evidence
    # --------------------------------------------------------

    if "value" in evidence:

        record["value"] = evidence["value"]

    # --------------------------------------------------------
    # Phase 9 regulatory evidence
    # --------------------------------------------------------

    for field in (
        "jurisdiction",
        "asset",
        "activity",
        "status",
        "regulatory_status",
        "evidence_text",
    ):

        if field in evidence:

            record[field] = evidence[field]

    return record


# ============================================================
# BUILD SETTLEMENT AUDIT
# ============================================================

def build_settlement_audit(
    economic,
    economic_status,
    economic_reason,
    regulatory_evidence,
    regulatory_state,
    decisions,
    ranked_routes,
    recommendation,
    recommendation_reason,
    telegraph_intelligence=None,
):
    """
    Build the complete settlement audit record.

    The audit records:

        - economic intelligence
        - regulatory evidence
        - regulatory state
        - route decisions
        - route ranking
        - recommendation
        - data provenance

    The audit does NOT create a recommendation.
    It records the deterministic decision already made.
    """

    route_decisions = []

    for decision in decisions:

        route = decision["route"]

        item = {
            "route": route["route"],
            "asset": route["asset"],
            "network": route["network"],
            "status": decision["status"],
            "reason": decision["reason"],
        }

        # ----------------------------------------------------
        # Decision evidence
        # ----------------------------------------------------

        if "evidence" in decision:

            item["evidence"] = (
                build_evidence_audit_record(
                    decision["evidence"]
                )
            )

        # ----------------------------------------------------
        # Decision explanation
        # ----------------------------------------------------

        if "explanation" in decision:

            item["explanation"] = (
                decision["explanation"]
            )

        route_decisions.append(item)

    # --------------------------------------------------------
    # Route ranking
    # --------------------------------------------------------

    route_ranking = []

    for route in ranked_routes:

        route_ranking.append({
            "route": route["route"],
            "asset": route["asset"],
            "network": route["network"],
            "cost_usd": route["cost"]["value"],
        })

    # --------------------------------------------------------
    # Complete audit
    # --------------------------------------------------------

    audit = {
        "audit_version": "9.9",

        "generated_at_utc":
            datetime.now(timezone.utc).isoformat(),

        # ----------------------------------------------------
        # Economic intelligence
        # ----------------------------------------------------

        "economic": {
            "transaction_value_usd":
                economic["transaction_value_usd"],

            "network_cost_usd":
                economic["network_cost_usd"],

            "status":
                economic["status"],

            "source":
                economic["source"],

            "confidence":
                economic["confidence"],
        },

        # ----------------------------------------------------
        # Economic gate
        # ----------------------------------------------------

        "economic_gate": {
            "status":
                economic_status,

            "reason":
                economic_reason,
        },

        # ----------------------------------------------------
        # Regulatory intelligence
        # ----------------------------------------------------

        "regulatory_gate": {
            "jurisdiction":
                regulatory_evidence["jurisdiction"],

            "asset":
                regulatory_evidence["asset"],

            "activity":
                regulatory_evidence["activity"],

            "status":
                regulatory_evidence["status"],

            "regulatory_state":
                regulatory_state,

            "source":
                regulatory_evidence["source"],

            "source_type":
                regulatory_evidence["source_type"],

            "confidence":
                regulatory_evidence["confidence"],

            "evidence_text":
                regulatory_evidence["evidence_text"],
        },

        # ----------------------------------------------------
        # Route decisions
        # ----------------------------------------------------

        "route_decisions":
            route_decisions,

        # ----------------------------------------------------
        # Route ranking
        # ----------------------------------------------------

        "route_ranking":
            route_ranking,

        # ----------------------------------------------------
        # Recommendation
        # ----------------------------------------------------

        "recommendation":
            recommendation,

        "recommendation_reason":
            recommendation_reason,

        # ----------------------------------------------------
        # Telegraph intelligence
        # ----------------------------------------------------

        "telegraph_intelligence":
            telegraph_intelligence,

        # ----------------------------------------------------
        # Provenance
        # ----------------------------------------------------

        "provenance": {
            "economic_input":
                economic["status"],

            "economic_source":
                economic["source"],

            "route_network_data":
                "REAL",

            "route_risk":
                "TEST",

            "compliance":
                "REFERENCE",

            "geopolitical":
                "REFERENCE",

            "regulatory":
                regulatory_evidence["source_type"],

            "telegraph":
                "AVAILABLE"
                if telegraph_intelligence is not None
                else "UNAVAILABLE",
        },
    }

    return audit


# ============================================================
# REAL ECONOMIC INPUT
# ============================================================

economic = build_economic_intelligence()

transaction_value_usd = (
    economic["transaction_value_usd"]
)

network_cost_usd = (
    economic["network_cost_usd"]
)


print("=== REAL ECONOMIC INPUT ===")

print(
    f"Transaction value: "
    f"${transaction_value_usd:.2f}"
)

print(
    f"Network cost: "
    f"${network_cost_usd:.6f}"
)

print(
    f"Source: "
    f"{economic['source']}"
)

print(
    f"Confidence: "
    f"{economic['confidence']}"
)


# ============================================================
# ECONOMIC GATE
# ============================================================

if network_cost_usd > transaction_value_usd:

    economic_status = "REJECTED"

    economic_reason = (
        "NETWORK_COST_EXCEEDS_TRANSACTION_VALUE"
    )

else:

    economic_status = "PASSED"

    economic_reason = None


print()
print("=== ECONOMIC GATE ===")

print(
    f"Status: "
    f"{economic_status}"
)

if economic_reason:

    print(
        f"Reason: "
        f"{economic_reason}"
    )


# ============================================================
# REGULATORY EVIDENCE
# ============================================================

regulatory_evidence = build_regulatory_evidence(
    jurisdiction="India",
    asset="ETH",
    activity="CROSS_BORDER_PAYMENT",
    status="PERMITTED",
    source="TEST",
    source_type="REFERENCE",
    confidence=1.0,
    evidence_text="Test permitted regulatory evidence",
)
regulatory_state = (
    determine_regulatory_state(
        regulatory_evidence
    )
)

print()
print("=== REGULATORY GATE ===")

print(
    f"Jurisdiction: "
    f"{regulatory_evidence['jurisdiction']}"
)

print(
    f"Asset: "
    f"{regulatory_evidence['asset']}"
)

print(
    f"Activity: "
    f"{regulatory_evidence['activity']}"
)

print(
    f"Status: "
    f"{regulatory_evidence['status']}"
)

print(
    f"Regulatory state: "
    f"{regulatory_state}"
)


# ============================================================
# PHASE E.3 — PAYMENT INTENT
# ============================================================

payment_intent = build_payment_intent(
    amount=50000,
    source_currency="USD",
    destination_currency="USD",
    counterparty="counterparty-A",
)

payment_intent = validate_payment_intent(
    payment_intent
)

if payment_intent["metadata"]["status"] != "VALIDATED":

    raise ValueError(
        "PaymentIntent validation failed"
    )



# ============================================================
# PHASE 10.5 — TELEGRAPH DECISION INPUT
# ============================================================

# Telegraph is an intelligence provider only.
# Its normalized output is passed into the provider-independent
# decision-input contract. No settlement decision is made here.

telegraph_intelligence = None

try:

    telegraph_decision_input = (
        build_telegraph_decision_input(
            intelligence={
                "asset": economic["asset"],
                "network": economic["network"],
                "chain_id": economic["chain_id"],
                "status": economic["status"],
                "confidence": economic["confidence"],
                "value_usd": economic[
                    "transaction_value_usd"
                ],
                "network_cost_usd": economic[
                    "network_cost_usd"
                ],
                "market_price_usd": economic[
                    "eth_price_usd"
                ],
            },
                regulatory_evidence=
                  regulatory_evidence,

                payment_intent=
                  payment_intent,
        )
    )

    telegraph_intelligence = (
        telegraph_decision_input.get(
            "telegraph_intelligence"
        )
    )

    print()
    print("=== TELEGRAPH INTELLIGENCE ===")

    if telegraph_intelligence is not None:

        print(
            f"Request ID: "
            f"{telegraph_intelligence['request_id']}"
        )

        print(
            f"Routes: "
            f"{list(telegraph_intelligence['routes'].keys())}"
        )

        print(
            "Settlement decision: "
            "NOT MADE BY TELEGRAPH"
        )

except (FileNotFoundError, ValueError) as exc:

    print()
    print("=== TELEGRAPH INTELLIGENCE ===")

    print(
        "Status: UNAVAILABLE"
    )

    print(
        f"Reason: {exc}"
    )


# ============================================================
# NORMALIZED ROUTE INPUT
# ============================================================

normalized_routes = get_normalized_routes()


# ============================================================
# POLICY INTELLIGENCE
# ============================================================

policies = build_policy_intelligence(
    jurisdiction=
        regulatory_evidence["jurisdiction"],
)

# ============================================================
# PHASE E.4.3 — DECISION ENGINE
# ============================================================

engine = DecisionEngine(
    max_risk=MAX_RISK,
)

decision_input = build_telegraph_decision_input(
    intelligence={
        "asset": economic["asset"],
        "network": economic["network"],
        "chain_id": economic["chain_id"],
        "status": economic["status"],
        "confidence": economic["confidence"],
        "value_usd": economic[
            "transaction_value_usd"
        ],
        "network_cost_usd": economic[
            "network_cost_usd"
        ],
        "market_price_usd": economic[
            "eth_price_usd"
        ],
    },
    regulatory_evidence=
        regulatory_evidence,

    payment_intent=
        payment_intent,
)

result = engine.decide(
    decision_input=
        decision_input,

    normalized_routes=
        normalized_routes,

    policies=
        policies,

    regulatory_state=
        regulatory_state,

    regulatory_evidence=
        regulatory_evidence,
)

decisions = result["decisions"]

ranked_routes = result["ranked_routes"]

recommendation = result["recommendation"]

recommendation_reason = (
    result["recommendation_reason"]
)



# ============================================================
# DECISION EXPLANATIONS
# ============================================================

for decision in decisions:

    decision["explanation"] = (
        build_decision_explanation(
            decision
        )
    )


# ============================================================
# SETTLEMENT DECISION
# ============================================================

print()
print("=== SETTLEMENT DECISION ===")

print()
print("Route decisions:")


for decision in decisions:

    route = decision["route"]

    print(
        f"{route['route']} | "
        f"{decision['status']}"
    )

    if decision["reason"]:

        print(
            f"  Reason: "
            f"{decision['reason']}"
        )

    if "evidence" in decision:

        evidence = decision["evidence"]

        print(
            f"  Evidence source: "
            f"{evidence['source']}"
        )

        print(
            f"  Evidence type: "
            f"{evidence['source_type']}"
        )

        print(
            f"  Evidence confidence: "
            f"{evidence['confidence']}"
        )


# ============================================================
# DATA PROVENANCE
# ============================================================

print()
print("=== DATA PROVENANCE ===")

print(
    f"Economic input: "
    f"{economic['status']}"
)

print(
    f"Economic source: "
    f"{economic['source']}"
)

print(
    "Route network data: "
    "REAL"
)

print(
    "Route risk: "
    "TEST"
)

print(
    "Compliance: "
    "REFERENCE"
)

print(
    "Geopolitical: "
    "REFERENCE"
)

print(
    f"Regulatory evidence: "
    f"{regulatory_evidence['source_type']}"
)


# ============================================================
# BUILD AUDIT RECORD
# ============================================================

audit = build_settlement_audit(
    economic=economic,

    economic_status=
        economic_status,

    economic_reason=
        economic_reason,

    regulatory_evidence=
        regulatory_evidence,

    regulatory_state=
        regulatory_state,

    decisions=
        decisions,

    ranked_routes=
        ranked_routes,

    recommendation=
        recommendation,

    recommendation_reason=
        recommendation_reason,

    telegraph_intelligence=
        telegraph_intelligence,
)


# ============================================================
# WRITE AUDIT FILE
# ============================================================

with open(
    AUDIT_FILE,
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        audit,
        file,
        indent=4,
    )


print()
print("=== AUDIT ===")

print(
    f"Audit file: "
    f"{AUDIT_FILE}"
)

print(
    "Audit version: "
    "9.9"
)

print(
    "Status: "
    "WRITTEN"
)