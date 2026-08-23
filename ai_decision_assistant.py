import json


# ============================================================
# CONFIGURATION
# ============================================================

REPORT_FILE = "audit/settlement_report_8_12.json"


# ============================================================
# LOAD SETTLEMENT REPORT
# ============================================================

def load_settlement_report():

    with open(REPORT_FILE, "r") as file:
        return json.load(file)


# ============================================================
# BUILD CONFIDENCE FROM REPORT
# ============================================================

def calculate_confidence(report):

    economic = report.get("economic", {})
    provenance = report.get("provenance", {})
    route_decisions = report.get("route_decisions", [])

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

        evidence = decision.get("evidence")

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

    if provenance.get("route_risk") == "REAL":

        risk_confidence = 1.0

    elif provenance.get("route_risk") == "REFERENCE":

        risk_confidence = 0.5

    else:

        risk_confidence = 0.0

    # --------------------------------------------------------
    # Geopolitical
    # --------------------------------------------------------

    if provenance.get("geopolitical") == "REAL":

        geopolitical_confidence = 1.0

    elif provenance.get("geopolitical") == "REFERENCE":

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
        "overall_confidence": overall_confidence,
        "economic_confidence": economic_confidence,
        "network_confidence": network_confidence,
        "compliance_confidence": compliance_confidence,
        "geopolitical_confidence":
            geopolitical_confidence,
        "risk_confidence": risk_confidence,
    }


# ============================================================
# ROUTE EXPLANATION
# ============================================================

def explain_route_decision(decision):

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

    print("-" * 60)

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
# AI-ASSISTED INTERPRETATION
# ============================================================

def explain_settlement_report(report):

    print()
    print(
        "=== AI-ASSISTED "
        "SETTLEMENT INTERPRETATION ==="
    )

    # --------------------------------------------------------
    # Economic condition
    # --------------------------------------------------------

    economic = report.get(
        "economic",
        {}
    )

    print()
    print("1. ECONOMIC CONDITION")
    print("-" * 60)

    print(
        "The transaction passed "
        "the economic gate."
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

    # --------------------------------------------------------
    # Route interpretation
    # --------------------------------------------------------

    print()
    print("2. ROUTE INTERPRETATION")
    print("-" * 60)

    route_decisions = report.get(
        "route_decisions",
        []
    )

    for decision in route_decisions:

        explain_route_decision(
            decision
        )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    print()
    print("3. RECOMMENDATION INTERPRETATION")
    print("-" * 60)

    recommendation = report.get(
        "recommendation"
    )

    recommendation_reason = report.get(
        "recommendation_reason"
    )

    if recommendation:

        print(
            f"Deterministic recommendation: "
            f"{recommendation}"
        )

    else:

        print(
            "Deterministic recommendation: "
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
    print("4. CONFIDENCE INTERPRETATION")
    print("-" * 60)

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
        "5. MISSING / INCOMPLETE INFORMATION"
    )
    print("-" * 60)

    provenance = report.get(
        "provenance",
        {}
    )

    missing_items = []

    if provenance.get("compliance") != "REAL":

        missing_items.append(
            "jurisdiction-specific "
            "compliance validation"
        )

    if provenance.get("geopolitical") != "REAL":

        missing_items.append(
            "validated geopolitical "
            "settlement status"
        )

    if provenance.get("route_risk") != "REAL":

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
    # AI interpretation
    # --------------------------------------------------------

    print()
    print("6. AI INTERPRETATION")
    print("-" * 60)

    if recommendation is None:

        print(
            "The deterministic settlement "
            "engine did not recommend a route."
        )

        print(
            "The primary limitation is incomplete "
            "policy, geopolitical, and risk information."
        )

        print(
            "The AI assistant explains the "
            "deterministic result but does not "
            "create an alternative recommendation."
        )

    else:

        print(
            "The deterministic engine produced "
            "a settlement recommendation."
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
    print("Status: READY")