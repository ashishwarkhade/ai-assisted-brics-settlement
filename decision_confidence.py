import json


# ============================================================
# CONFIGURATION
# ============================================================

AUDIT_FILE = "audit/settlement_audit.json"


# ============================================================
# LOAD AUDIT
# ============================================================

def load_settlement_audit():

    with open(AUDIT_FILE, "r") as file:
        return json.load(file)


# ============================================================
# CONFIDENCE CLASSIFICATION
# ============================================================

def classify_confidence(confidence):

    if confidence >= 0.90:
        return "HIGH"

    if confidence >= 0.70:
        return "MEDIUM"

    if confidence > 0.0:
        return "LOW"

    return "UNKNOWN"


# ============================================================
# BUILD DECISION CONFIDENCE
# ============================================================

def build_decision_confidence(audit):

    economic = audit["economic"]

    provenance = audit["provenance"]

    economic_confidence = economic.get(
        "confidence",
        0.0,
    )

    # --------------------------------------------------------
    # Provenance confidence
    # --------------------------------------------------------

    network_confidence = 1.0

    compliance_confidence = 0.0

    geopolitical_confidence = 0.0

    risk_confidence = 0.0

    # --------------------------------------------------------
    # Inspect route decisions
    # --------------------------------------------------------

    route_decisions = audit.get(
        "route_decisions",
        [],
    )

    for decision in route_decisions:

        evidence = decision.get(
            "evidence"
        )

        if not evidence:
            continue

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

    # --------------------------------------------------------
    # Existing provenance tells us risk quality
    # --------------------------------------------------------

    if provenance.get("route_risk") == "REAL":

        risk_confidence = 1.0

    elif provenance.get("route_risk") == "REFERENCE":

        risk_confidence = 0.5

    else:

        risk_confidence = 0.0

    # --------------------------------------------------------
    # Geopolitical provenance
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
    # weakest critical data determines confidence.
    # --------------------------------------------------------

    overall_confidence = min(
        economic_confidence,
        network_confidence,
        compliance_confidence,
        geopolitical_confidence,
        risk_confidence,
    )

    # --------------------------------------------------------
    # Decision quality
    # --------------------------------------------------------

    if overall_confidence >= 0.90:

        decision_quality = "SUFFICIENT_FOR_AUTOMATED_RECOMMENDATION"

    elif overall_confidence >= 0.70:

        decision_quality = (
            "REQUIRES_ADDITIONAL_VALIDATION"
        )

    else:

        decision_quality = (
            "INSUFFICIENT_FOR_AUTOMATED_RECOMMENDATION"
        )

    # --------------------------------------------------------
    # Overall classification
    # --------------------------------------------------------

    if overall_confidence >= 0.90:

        overall_status = "HIGH"

    elif overall_confidence >= 0.70:

        overall_status = "MEDIUM"

    elif overall_confidence > 0.0:

        overall_status = "LOW"

    else:

        overall_status = "INCOMPLETE"

    return {
        "overall_confidence": overall_confidence,
        "overall_status": overall_status,

        "economic": {
            "status": economic.get("status"),
            "confidence": economic_confidence,
            "classification":
                classify_confidence(
                    economic_confidence
                ),
        },

        "network": {
            "status": provenance.get(
                "route_network_data"
            ),
            "confidence": network_confidence,
            "classification":
                classify_confidence(
                    network_confidence
                ),
        },

        "compliance": {
            "status": provenance.get(
                "compliance"
            ),
            "confidence": compliance_confidence,
            "classification":
                classify_confidence(
                    compliance_confidence
                ),
        },

        "geopolitical": {
            "status": provenance.get(
                "geopolitical"
            ),
            "confidence": geopolitical_confidence,
            "classification":
                classify_confidence(
                    geopolitical_confidence
                ),
        },

        "risk": {
            "status": provenance.get(
                "route_risk"
            ),
            "confidence": risk_confidence,
            "classification":
                classify_confidence(
                    risk_confidence
                ),
        },

        "decision_quality": decision_quality,
    }


# ============================================================
# DISPLAY
# ============================================================

def print_decision_confidence(confidence):

    print("=== DECISION CONFIDENCE ===")

    print()

    print(
        f"Overall status: "
        f"{confidence['overall_status']}"
    )

    print(
        f"Overall confidence: "
        f"{confidence['overall_confidence']:.2f}"
    )

    print()

    print("Economic data")
    print("-" * 55)

    economic = confidence["economic"]

    print(
        f"Status: {economic['status']}"
    )

    print(
        f"Confidence: "
        f"{economic['confidence']}"
    )

    print(
        f"Classification: "
        f"{economic['classification']}"
    )

    print()

    print("Network data")
    print("-" * 55)

    network = confidence["network"]

    print(
        f"Status: {network['status']}"
    )

    print(
        f"Confidence: "
        f"{network['confidence']}"
    )

    print(
        f"Classification: "
        f"{network['classification']}"
    )

    print()

    print("Compliance data")
    print("-" * 55)

    compliance = confidence["compliance"]

    print(
        f"Status: {compliance['status']}"
    )

    print(
        f"Confidence: "
        f"{compliance['confidence']}"
    )

    print(
        f"Classification: "
        f"{compliance['classification']}"
    )

    print()

    print("Geopolitical data")
    print("-" * 55)

    geopolitical = confidence["geopolitical"]

    print(
        f"Status: {geopolitical['status']}"
    )

    print(
        f"Confidence: "
        f"{geopolitical['confidence']}"
    )

    print(
        f"Classification: "
        f"{geopolitical['classification']}"
    )

    print()

    print("Risk data")
    print("-" * 55)

    risk = confidence["risk"]

    print(
        f"Status: {risk['status']}"
    )

    print(
        f"Confidence: "
        f"{risk['confidence']}"
    )

    print(
        f"Classification: "
        f"{risk['classification']}"
    )

    print()

    print("Decision quality")
    print("-" * 55)

    print(
        confidence["decision_quality"]
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    audit = load_settlement_audit()

    confidence = build_decision_confidence(
        audit
    )

    print_decision_confidence(
        confidence
    )

    print()
    print("Status: READY")
