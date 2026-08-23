import json


AUDIT_FILE = "audit/settlement_audit.json"


# ============================================================
# LOAD AUDIT
# ============================================================

def load_settlement_audit():

    with open(AUDIT_FILE, "r") as file:
        return json.load(file)


# ============================================================
# LOAD DECISION CONFIDENCE
# ============================================================

def build_confidence_summary(audit):

    economic = audit.get("economic", {})
    provenance = audit.get("provenance", {})
    route_decisions = audit.get(
        "route_decisions",
        [],
    )

    economic_confidence = economic.get(
        "confidence",
        0.0,
    )

    network_confidence = 1.0

    compliance_confidence = 0.0
    geopolitical_confidence = 0.0
    risk_confidence = 0.0

    for decision in route_decisions:

        evidence = decision.get("evidence")

        if evidence:

            source_type = evidence.get(
                "source_type"
            )

            confidence = evidence.get(
                "confidence",
                0.0,
            )

            if source_type == "REFERENCE":

                compliance_confidence = max(
                    compliance_confidence,
                    confidence,
                )

    if provenance.get("geopolitical") == "REAL":

        geopolitical_confidence = 1.0

    elif provenance.get("geopolitical") == "REFERENCE":

        geopolitical_confidence = 0.5

    if provenance.get("route_risk") == "REAL":

        risk_confidence = 1.0

    elif provenance.get("route_risk") == "REFERENCE":

        risk_confidence = 0.5

    # --------------------------------------------------------
    # Weighted confidence
    #
    # Economic/network data are strong.
    # Policy data remain the limiting factors.
    # --------------------------------------------------------

    overall_confidence = (
        economic_confidence * 0.20
        + network_confidence * 0.20
        + compliance_confidence * 0.25
        + geopolitical_confidence * 0.20
        + risk_confidence * 0.15
    )

    # --------------------------------------------------------
    # Automation readiness
    # --------------------------------------------------------

    if (
        overall_confidence >= 0.90
        and compliance_confidence >= 0.90
        and geopolitical_confidence >= 0.90
        and risk_confidence >= 0.90
    ):

        automation_readiness = "READY"

    else:

        automation_readiness = (
            "NOT_READY_FOR_AUTOMATED_RECOMMENDATION"
        )

    # --------------------------------------------------------
    # Decision quality
    # --------------------------------------------------------

    if automation_readiness == "READY":

        decision_quality = (
            "SUFFICIENT_FOR_AUTOMATED_RECOMMENDATION"
        )

    elif overall_confidence >= 0.70:

        decision_quality = (
            "REQUIRES_ADDITIONAL_VALIDATION"
        )

    else:

        decision_quality = (
            "INSUFFICIENT_FOR_AUTOMATED_RECOMMENDATION"
        )

    return {
        "overall_confidence":
            round(overall_confidence, 2),

        "automation_readiness":
            automation_readiness,

        "decision_quality":
            decision_quality,

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
# BUILD REPORT
# ============================================================

def build_settlement_report(audit):

    confidence = build_confidence_summary(
        audit
    )

    recommendation = audit.get(
        "recommendation"
    )

    report = {

        "report_version": "8.12",

        "economic": audit.get(
            "economic"
        ),

        "economic_gate": audit.get(
            "economic_gate"
        ),

        "route_decisions": audit.get(
            "route_decisions",
            []
        ),

        "route_ranking": audit.get(
            "route_ranking",
            []
        ),

        "recommendation": recommendation,

        "recommendation_reason":
            audit.get(
                "recommendation_reason"
            ),

        "confidence": confidence,

        "provenance": audit.get(
            "provenance",
            {}
        ),
    }

    return report


# ============================================================
# HUMAN-READABLE REPORT
# ============================================================

def print_settlement_report(report):

    print("=== SETTLEMENT DECISION REPORT ===")

    print()
    print(
        f"Report version: "
        f"{report['report_version']}"
    )

    # --------------------------------------------------------
    # Economic input
    # --------------------------------------------------------

    economic = report["economic"]

    print()
    print("ECONOMIC INPUT")
    print("-" * 60)

    print(
        f"Transaction value: "
        f"${economic['transaction_value_usd']:.2f}"
    )

    print(
        f"Network cost: "
        f"${economic['network_cost_usd']:.6f}"
    )

    print(
        f"Status: "
        f"{economic['status']}"
    )

    print(
        f"Source: "
        f"{economic['source']}"
    )

    print(
        f"Confidence: "
        f"{economic['confidence']}"
    )

    # --------------------------------------------------------
    # Economic gate
    # --------------------------------------------------------

    gate = report["economic_gate"]

    print()
    print("ECONOMIC GATE")
    print("-" * 60)

    print(
        f"Status: "
        f"{gate['status']}"
    )

    if gate.get("reason"):

        print(
            f"Reason: "
            f"{gate['reason']}"
        )

    # --------------------------------------------------------
    # Route decisions
    # --------------------------------------------------------

    print()
    print("ROUTE DECISIONS")
    print("=" * 60)

    for decision in report["route_decisions"]:

        print(
            f"{decision['route']} | "
            f"{decision['asset']} / "
            f"{decision['network']}"
        )

        print(
            f"  Status: "
            f"{decision['status']}"
        )

        if decision.get("reason"):

            print(
                f"  Reason: "
                f"{decision['reason']}"
            )

        evidence = decision.get(
            "evidence"
        )

        if evidence:

            print(
                f"  Evidence: "
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

        print()

    # --------------------------------------------------------
    # Route ranking
    # --------------------------------------------------------

    print("ROUTE RANKING")
    print("=" * 60)

    ranking = report.get(
        "route_ranking",
        []
    )

    if not ranking:

        print(
            "No route has sufficient "
            "policy and economic data."
        )

    else:

        for index, route in enumerate(
            ranking,
            start=1
        ):

            print(
                f"{index}. "
                f"{route}"
            )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    print()
    print("FINAL RECOMMENDATION")
    print("=" * 60)

    if report["recommendation"]:

        print(
            report["recommendation"]
        )

    else:

        print("NO_RECOMMENDATION")

    if report.get(
        "recommendation_reason"
    ):

        print(
            f"Reason: "
            f"{report['recommendation_reason']}"
        )

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    confidence = report["confidence"]

    print()
    print("DECISION CONFIDENCE")
    print("=" * 60)

    print(
        f"Overall confidence: "
        f"{confidence['overall_confidence']:.2f}"
    )

    print(
        f"Automation readiness: "
        f"{confidence['automation_readiness']}"
    )

    print(
        f"Decision quality: "
        f"{confidence['decision_quality']}"
    )

    # --------------------------------------------------------
    # Provenance
    # --------------------------------------------------------

    provenance = report["provenance"]

    print()
    print("DATA PROVENANCE")
    print("=" * 60)

    print(
        f"Economic input: "
        f"{provenance.get('economic_input')}"
    )

    print(
        f"Economic source: "
        f"{provenance.get('economic_source')}"
    )

    print(
        f"Route network data: "
        f"{provenance.get('route_network_data')}"
    )

    print(
        f"Route risk: "
        f"{provenance.get('route_risk')}"
    )

    print(
        f"Compliance: "
        f"{provenance.get('compliance')}"
    )

    print(
        f"Geopolitical: "
        f"{provenance.get('geopolitical')}"
    )


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(report):

    output_file = (
        "audit/settlement_report_8_12.json"
    )

    with open(
        output_file,
        "w"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
        )

    return output_file


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    audit = load_settlement_audit()

    report = build_settlement_report(
        audit
    )

    print_settlement_report(
        report
    )

    output_file = save_report(
        report
    )

    print()
    print("Status: READY")
    print(
        f"Report file: "
        f"{output_file}"
    )