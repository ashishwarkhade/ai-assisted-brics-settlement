
import json


# ============================================================
# CONFIGURATION
# ============================================================

AUDIT_FILE = "audit/settlement_audit.json"


# ============================================================
# AI AUTHORITY
# ============================================================

AI_AUTHORITY = "EXPLANATION_ONLY"


# ============================================================
# LOAD SETTLEMENT AUDIT
# ============================================================

def load_settlement_report():

    with open(
        AUDIT_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# ============================================================
# BUILD CONFIDENCE FROM AUDIT
# ============================================================

def calculate_confidence(report):

    economic = report.get(
        "economic",
        {}
    )

    provenance = report.get(
        "provenance",
        {}
    )

    route_decisions = report.get(
        "route_decisions",
        []
    )

    economic_confidence = economic.get(
        "confidence",
        0.0,
    )

    network_confidence = 1.0

    compliance_confidence = 0.0

    geopolitical_confidence = 0.0

    risk_confidence = 0.0

    # --------------------------------------------------------
    # Compliance evidence
    # --------------------------------------------------------

    for decision in route_decisions:

        evidence = decision.get(
            "evidence"
        )

        if not evidence:
            continue

        confidence = evidence.get(
            "confidence",
            0.0,
        )

        source_type = evidence.get(
            "source_type"
        )

        if source_type == "REFERENCE":

            compliance_confidence = max(
                compliance_confidence,
                confidence,
            )

    # --------------------------------------------------------
    # Risk
    # --------------------------------------------------------

    if provenance.get(
        "route_risk"
    ) == "REAL":

        risk_confidence = 1.0

    elif provenance.get(
        "route_risk"
    ) == "REFERENCE":

        risk_confidence = 0.5

    else:

        risk_confidence = 0.0

    # --------------------------------------------------------
    # Geopolitical
    # --------------------------------------------------------

    if provenance.get(
        "geopolitical"
    ) == "REAL":

        geopolitical_confidence = 1.0

    elif provenance.get(
        "geopolitical"
    ) == "REFERENCE":

        geopolitical_confidence = 0.5

    else:

        geopolitical_confidence = 0.0

    # --------------------------------------------------------
    # Overall confidence
    #
    # Conservative approach:
    # weakest critical input controls confidence.
    # --------------------------------------------------------

    overall_confidence = min(
        economic_confidence,
        network_confidence,
        compliance_confidence,
        geopolitical_confidence,
        risk_confidence,
    )

    return {
        "overall_confidence":
            overall_confidence,

        "economic_confidence":
            economic_confidence,

        "network_confidence":
            network_confidence,

        "compliance_confidence":
            compliance_confidence,

        "geopolitical_confidence":
            geopolitical_confidence,

        "risk_confidence":
            risk_confidence,
    }


# ============================================================
# ROUTE EXPLANATION
# ============================================================

def explain_route_decision(
    decision
):

    route = decision.get(
        "route",
        "UNKNOWN",
    )

    asset = decision.get(
        "asset",
        "UNKNOWN",
    )

    network = decision.get(
        "network",
        "UNKNOWN",
    )

    status = decision.get(
        "status",
        "UNKNOWN",
    )

    reason = decision.get(
        "reason"
    )

    print()

    print(
        f"{route} "
        f"({asset} / {network})"
    )

    print(
        "-" * 60
    )

    print(
        f"Decision status: {status}"
    )

    if reason:

        print(
            f"Decision reason: {reason}"
        )

    evidence = decision.get(
        "evidence"
    )

    if evidence:

        print()

        print(
            "Supporting evidence:"
        )

        print(
            f"  Value: "
            f"{evidence.get('value')}"
        )

        print(
            f"  Source: "
            f"{evidence.get('source')}"
        )

        print(
            f"  Type: "
            f"{evidence.get('source_type')}"
        )

        print(
            f"  Confidence: "
            f"{evidence.get('confidence')}"
        )


# ============================================================
# TELEGRAPH INTELLIGENCE
# ============================================================

def explain_telegraph_intelligence(
    report
):

    telegraph = report.get(
        "telegraph_intelligence"
    )

    provenance = report.get(
        "provenance",
        {}
    )

    print()

    print(
        "TELEGRAPH INTELLIGENCE"
    )

    print(
        "-" * 60
    )

    if not telegraph:

        print(
            "Status: NOT_AVAILABLE"
        )

        return

    print(
        f"Status: "
        f"{provenance.get('telegraph', 'AVAILABLE')}"
    )

    print(
        f"Request ID: "
        f"{telegraph.get('request_id')}"
    )

    print(
        f"Generated at: "
        f"{telegraph.get('generated_at')}"
    )

    routes = telegraph.get(
        "routes",
        {}
    )

    print(
        f"Routes: "
        f"{list(routes.keys())}"
    )

    for route_id, route in routes.items():

        asset = route.get(
            "asset",
            "UNKNOWN"
        )

        network = route.get(
            "network",
            "UNKNOWN"
        )

        evidence = route.get(
            "evidence",
            []
        )

        print(
            f"  {route_id} | "
            f"{asset} / {network} | "
            f"evidence={len(evidence)}"
        )

    print()

    print(
        "Role: PROVIDER-DERIVED "
        "INTELLIGENCE ONLY"
    )

    print(
        "Telegraph does not make the "
        "settlement decision."
    )

    print(
        "Telegraph does not override "
        "deterministic eligibility."
    )

    print(
        "Telegraph does not override "
        "deterministic ranking."
    )

    print(
        "Telegraph does not create a "
        "settlement recommendation."
    )


# ============================================================
# AI-ASSISTED INTERPRETATION
# ============================================================

def explain_settlement_report(
    report
):

    print()

    print(
        "=== AI-ASSISTED "
        "SETTLEMENT INTERPRETATION ==="
    )

    print()

    print(
        f"AI authority: "
        f"{AI_AUTHORITY}"
    )

    # --------------------------------------------------------
    # Economic condition
    # --------------------------------------------------------

    economic = report.get(
        "economic",
        {}
    )

    economic_gate = report.get(
        "economic_gate",
        {}
    )

    print()

    print(
        "1. ECONOMIC CONDITION"
    )

    print(
        "-" * 60
    )

    print(
        f"Economic gate: "
        f"{economic_gate.get('status')}"
    )

    print(
        f"Transaction value: "
        f"${economic.get('transaction_value_usd', 0):.2f}"
    )

    print(
        f"Observed network cost: "
        f"${economic.get('network_cost_usd', 0):.6f}"
    )

    print(
        f"Economic data source: "
        f"{economic.get('source')}"
    )

    print(
        f"Economic confidence: "
        f"{economic.get('confidence')}"
    )

    # --------------------------------------------------------
    # Regulatory condition
    # --------------------------------------------------------

    regulatory_gate = report.get(
        "regulatory_gate",
        {}
    )

    print()

    print(
        "2. REGULATORY / POLICY CONDITION"
    )

    print(
        "-" * 60
    )

    print(
        f"Jurisdiction: "
        f"{regulatory_gate.get('jurisdiction')}"
    )

    print(
        f"Asset: "
        f"{regulatory_gate.get('asset')}"
    )

    print(
        f"Activity: "
        f"{regulatory_gate.get('activity')}"
    )

    print(
        f"Status: "
        f"{regulatory_gate.get('status')}"
    )

    print(
        f"Regulatory state: "
        f"{regulatory_gate.get('regulatory_state')}"
    )

    # --------------------------------------------------------
    # Route decisions
    # --------------------------------------------------------

    print()

    print(
        "3. DETERMINISTIC ROUTE DECISIONS"
    )

    print(
        "-" * 60
    )

    route_decisions = report.get(
        "route_decisions",
        []
    )

    if not route_decisions:

        print(
            "No route decisions are available."
        )

    else:

        for decision in route_decisions:

            explain_route_decision(
                decision
            )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    print()

    print(
        "4. DETERMINISTIC RECOMMENDATION"
    )

    print(
        "-" * 60
    )

    recommendation = report.get(
        "recommendation"
    )

    recommendation_reason = report.get(
        "recommendation_reason"
    )

    if recommendation:

        print(
            f"Recommendation: "
            f"{recommendation}"
        )

    else:

        print(
            "Recommendation: "
            "NO_RECOMMENDATION"
        )

    if recommendation_reason:

        print(
            f"Reason: "
            f"{recommendation_reason}"
        )

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    confidence = calculate_confidence(
        report
    )

    overall = confidence[
        "overall_confidence"
    ]

    print()

    print(
        "5. CONFIDENCE INTERPRETATION"
    )

    print(
        "-" * 60
    )

    print(
        f"Overall confidence: "
        f"{overall:.2f}"
    )

    print(
        f"Economic confidence: "
        f"{confidence['economic_confidence']:.2f}"
    )

    print(
        f"Network confidence: "
        f"{confidence['network_confidence']:.2f}"
    )

    print(
        f"Compliance confidence: "
        f"{confidence['compliance_confidence']:.2f}"
    )

    print(
        f"Geopolitical confidence: "
        f"{confidence['geopolitical_confidence']:.2f}"
    )

    print(
        f"Risk confidence: "
        f"{confidence['risk_confidence']:.2f}"
    )

    if overall >= 0.90:

        automation = "READY"

    else:

        automation = (
            "NOT_READY_FOR_AUTOMATED_RECOMMENDATION"
        )

    print(
        f"Automation readiness: "
        f"{automation}"
    )

    # --------------------------------------------------------
    # Missing information
    # --------------------------------------------------------

    print()

    print(
        "6. MISSING / INCOMPLETE INFORMATION"
    )

    print(
        "-" * 60
    )

    provenance = report.get(
        "provenance",
        {}
    )

    missing_items = []

    if provenance.get(
        "compliance"
    ) != "REAL":

        missing_items.append(
            "jurisdiction-specific "
            "compliance validation"
        )

    if provenance.get(
        "geopolitical"
    ) != "REAL":

        missing_items.append(
            "validated geopolitical "
            "settlement status"
        )

    if provenance.get(
        "route_risk"
    ) != "REAL":

        missing_items.append(
            "validated route risk data"
        )

    if not missing_items:

        print(
            "No major missing information detected."
        )

    else:

        for item in missing_items:

            print(
                f"- {item}"
            )

    # --------------------------------------------------------
    # Telegraph
    # --------------------------------------------------------

    print()

    print(
        "7. TELEGRAPH INTELLIGENCE"
    )

    print(
        "-" * 60
    )

    explain_telegraph_intelligence(
        report
    )

    # --------------------------------------------------------
    # AI interpretation
    # --------------------------------------------------------

    print()

    print(
        "8. AI INTERPRETATION"
    )

    print(
        "-" * 60
    )

    telegraph_available = (
        report.get(
            "telegraph_intelligence"
        )
        is not None
    )

    if recommendation is None:

        print(
            "The deterministic settlement "
            "engine did not recommend a route."
        )

        print(
            "The primary limitation is incomplete "
            "policy, geopolitical, and risk information."
        )

        if telegraph_available:

            print(
                "Telegraph intelligence is available "
                "but does not change the deterministic result."
            )

        print(
            "The AI assistant explains the "
            "deterministic result and does not "
            "create an alternative recommendation."
        )

    else:

        print(
            "The deterministic engine produced "
            "a settlement recommendation."
        )

        if telegraph_available:

            print(
                "Telegraph intelligence is presented "
                "as provider-derived context only."
            )

        print(
            "The AI assistant provides an "
            "interpretation of that decision."
        )

    print()

    print(
        "AI role: EXPLAIN — NOT OVERRIDE"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    report = load_settlement_report()

    explain_settlement_report(
        report
    )

    print()

    print(
        "Status: READY"
    )
