import json
from datetime import datetime, timezone

from brics_regulatory_evidence import (
    build_regulatory_evidence,
    determine_regulatory_state,
)

from settlement_path_discovery import build_candidate_path
from normalized_routes import get_normalized_routes
from policy_intelligence import build_policy_intelligence
from economic_intelligence import build_economic_intelligence
from decision_explanation import build_decision_explanation
from telegraph_decision_integration import build_telegraph_decision_input
from decision_engine import DecisionEngine
from payment_intent import validate_payment_intent


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

    for field in (
        "source",
        "source_type",
        "confidence",
    ):
        if field in evidence:
            record[field] = evidence[field]

    if "value" in evidence:
        record["value"] = evidence["value"]

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
    payment_intent,
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
    settlement_path=None,
):
    """
    Build the complete settlement audit record.

    The audit records:

        - payment intent
        - economic intelligence
        - regulatory evidence
        - regulatory state
        - candidate settlement path
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

        if "evidence" in decision:

            item["evidence"] = (
                build_evidence_audit_record(
                    decision["evidence"]
                )
            )

        if "explanation" in decision:

            item["explanation"] = (
                decision["explanation"]
            )

        route_decisions.append(item)

    route_ranking = []

    for route in ranked_routes:

        route_ranking.append({
            "route": route["route"],
            "asset": route["asset"],
            "network": route["network"],
            "cost_usd": route["cost"]["value"],
        })

    audit = {
        "audit_version": "9.9",

        "payment_intent":
            payment_intent,

        "generated_at_utc":
            datetime.now(timezone.utc).isoformat(),

        # ----------------------------------------------------
        # Economic intelligence
        # ----------------------------------------------------

        "economic": {
            "user_transaction_value_usd":
                economic["user_transaction_value_usd"],

            "observed_transaction_value_usd":
                economic["observed_transaction_value_usd"],

            "network_cost_usd":
                economic["network_cost_usd"],

            "status":
                economic["status"],

            "source":
                economic["source"],

            "confidence":
                economic["confidence"],

            "user_transaction_amount":
                economic["user_transaction_amount"],

            "user_transaction_currency":
                economic["user_transaction_currency"],

            "observed_transaction_value_eth":
                economic["observed_transaction_value_eth"],

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
        # Candidate settlement path
        # ----------------------------------------------------

        "settlement_path":
            settlement_path,

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

            "settlement_path":
                "DISCOVERY",
        },
    }

    return audit


# ============================================================
# RUN SETTLEMENT
# ============================================================

def run_settlement(payment_intent):
    """
    Run the deterministic settlement pipeline using a
    caller-supplied PaymentIntent.

    User/Business input owns PaymentIntent construction.

    This function owns settlement evaluation.

    It does not:
        - choose a settlement route
        - override the DecisionEngine
        - create regulatory approval
        - allow Telegraph to make a settlement decision

    Settlement path discovery supplies candidate-path
    intelligence only. UNKNOWN evidence remains UNKNOWN
    until independently validated evidence is available.
    """

    payment_intent = validate_payment_intent(
        payment_intent
    )

    if payment_intent["metadata"]["status"] != "VALIDATED":

        raise ValueError(
            "PaymentIntent validation failed"
        )

    source_jurisdiction = (
        payment_intent["corridor"]["source_jurisdiction"]
    )

    destination_jurisdiction = (
        payment_intent["corridor"]["destination_jurisdiction"]
    )

    if not source_jurisdiction:
        raise ValueError(
            "PaymentIntent source jurisdiction is required"
        )

    if not destination_jurisdiction:
        raise ValueError(
            "PaymentIntent destination jurisdiction is required"
        )

    # ============================================================
    # CANDIDATE SETTLEMENT PATH
    # ============================================================

    # Discovery does not recommend a route.
    # It records the corridor and leaves unsupported evidence
    # explicitly UNKNOWN.
    settlement_path = build_candidate_path(
        source=source_jurisdiction,
        destination=destination_jurisdiction,
        asset="ETH",
    )

    print()
    print("=== CANDIDATE SETTLEMENT PATH ===")

    print(
        f"Source jurisdiction: "
        f"{settlement_path['source_jurisdiction']}"
    )

    print(
        f"Destination jurisdiction: "
        f"{settlement_path['destination_jurisdiction']}"
    )

    print(
        f"Infrastructure: "
        f"{settlement_path['infrastructure']}"
    )

    print(
        f"Asset: "
        f"{settlement_path['asset']}"
    )

    print(
        f"Regulatory evidence state: "
        f"{settlement_path['regulatory_status']}"
    )

    print(
        f"Asset linkage state: "
        f"{settlement_path['linkage_status']}"
    )

    print(
        f"Cross-border capability state: "
        f"{settlement_path['cross_border_status']}"
    )

    # ============================================================
    # REAL ECONOMIC INPUT
    # ============================================================

    economic = build_economic_intelligence(
        payment_intent
    )

    transaction_value_usd = (
        economic["user_transaction_value_usd"]
    )

    network_cost_usd = (
        economic["network_cost_usd"]
    )

    print()
    print("=== REAL ECONOMIC INPUT ===")

    print(
        f"User transaction value: "
        f"${transaction_value_usd:.2f}"
    )

    print(
        f"Observed blockchain transaction value: "
        f"${economic['observed_transaction_value_usd']:.2f}"
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

    # IMPORTANT:
    #
    # The candidate path has no validated regulatory evidence.
    # Therefore UNKNOWN is represented explicitly.
    #
    # This does not infer permission or prohibition.
    # The deterministic DecisionEngine remains authoritative.

    regulatory_evidence = build_regulatory_evidence(
        jurisdiction=source_jurisdiction,
        asset=settlement_path["asset"],
        activity="CROSS_BORDER_PAYMENT",
        status=settlement_path["regulatory_status"],
        source="UNAVAILABLE",
        source_type="UNKNOWN",
        confidence=0.0,
        evidence_text=(
            "No jurisdiction-specific validated regulatory "
            "evidence has been supplied for this corridor."
        ),
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
                        "user_transaction_value_usd"
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
                "user_transaction_value_usd"
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

    print(
        "Settlement path evidence: "
        "DISCOVERY"
    )

    # ============================================================
    # BUILD AUDIT RECORD
    # ============================================================

    audit = build_settlement_audit(
        payment_intent=payment_intent,

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

        settlement_path=
            settlement_path,
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

    return {
        "payment_intent":
            payment_intent,

        "economic":
            economic,

        "economic_status":
            economic_status,

        "economic_reason":
            economic_reason,

        "settlement_path":
            settlement_path,

        "regulatory_evidence":
            regulatory_evidence,

        "regulatory_state":
            regulatory_state,

        "telegraph_intelligence":
            telegraph_intelligence,

        "decisions":
            decisions,

        "ranked_routes":
            ranked_routes,

        "recommendation":
            recommendation,

        "recommendation_reason":
            recommendation_reason,

        "audit":
            audit,
    }


# ============================================================
# CONTROLLED USER / BUSINESS DEMO
# ============================================================

if __name__ == "__main__":

    from user_business_input import (
        build_user_business_input,
        validate_user_business_input,
    )

    user_business_input = build_user_business_input(
        amount=1000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="Brazilian supplier",
        source_jurisdiction="India",
        destination_jurisdiction="Brazil",
        constraints={
            "purpose": "import_payment",
        },
    )

    payment_intent = (
        validate_user_business_input(
            user_business_input
        )
    )

    print()
    print("=== USER / BUSINESS REQUEST ===")

    print(
        "Amount: "
        "$1,000"
    )

    print(
        "Source jurisdiction: "
        "India"
    )

    print(
        "Destination jurisdiction: "
        "Brazil"
    )

    print(
        "Counterparty: "
        "Brazilian supplier"
    )

    print(
        "Purpose: "
        "import_payment"
    )

    run_settlement(payment_intent)

    print()
