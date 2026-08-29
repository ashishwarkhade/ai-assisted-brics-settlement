import json


# ============================================================
# CONFIGURATION
# ============================================================

AUDIT_FILE = "audit/settlement_audit.json"


# ============================================================
# LOAD AUDIT
# ============================================================

def load_settlement_audit():

    with open(
        AUDIT_FILE,
        "r",
        encoding="utf-8",
    ) as file:

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
# EXTRACT POLICY CONFIDENCE
# ============================================================

def extract_policy_confidence(
    route_decisions,
    evidence_name,
):

    confidence = 0.0

    for decision in route_decisions:

        evidence = decision.get(
            "evidence",
            {}
        )

        if not evidence:
            continue

        source_type = evidence.get(
            "source_type"
        )

        if source_type != "REFERENCE":
            continue

        value = evidence.get(
            "value"
        )

        # ----------------------------------------------------
        # Compliance evidence
        # ----------------------------------------------------

        if evidence_name == "compliance":

            if value is not None:

                confidence = max(
                    confidence,
                    evidence.get(
                        "confidence",
                        0.0
                    )
                )

        # ----------------------------------------------------
        # Geopolitical evidence
        # ----------------------------------------------------

        elif evidence_name == "geopolitical":

            if value is not None:

                confidence = max(
                    confidence,
                    evidence.get(
                        "confidence",
                        0.0
                    )
                )

    return confidence


# ============================================================
# PROVENANCE CONFIDENCE
# ============================================================

def provenance_confidence(
    provenance,
    field,
):

    value = provenance.get(field)

    if value == "REAL":
        return 1.0

    if value == "REFERENCE":
        return 0.5

    if value == "TEST":
        return 0.0

    return 0.0


# ============================================================
# TELEGRAPH PROVENANCE CONFIDENCE
# ============================================================

def telegraph_provenance_confidence(
    provenance,
):

    value = provenance.get(
        "telegraph"
    )

    if value == "AVAILABLE":
        return 1.0

    return 0.0


# ============================================================
# BUILD DECISION CONFIDENCE
# ============================================================

def build_decision_confidence(audit):

    economic = audit.get(
        "economic",
        {}
    )

    provenance = audit.get(
        "provenance",
        {}
    )

    route_decisions = audit.get(
        "route_decisions",
        []
    )

    # ========================================================
    # ECONOMIC
    # ========================================================

    economic_confidence = economic.get(
        "confidence",
        0.0
    )

    # ========================================================
    # NETWORK
    # ========================================================

    network_confidence = 1.0

    # ========================================================
    # COMPLIANCE
    # ========================================================

    compliance_confidence = (
        extract_policy_confidence(
            route_decisions,
            "compliance"
        )
    )

    # ========================================================
    # GEOPOLITICAL
    # ========================================================

    geopolitical_confidence = (
        provenance_confidence(
            provenance,
            "geopolitical"
        )
    )

    # ========================================================
    # RISK
    # ========================================================

    risk_confidence = (
        provenance_confidence(
            provenance,
            "route_risk"
        )
    )

    # ========================================================
    # TELEGRAPH
    #
    # Telegraph is an intelligence provider only.
    #
    # AVAILABLE means Telegraph supplied intelligence.
    #
    # It does NOT mean that regulatory, geopolitical,
    # compliance, or risk information has been validated.
    #
    # Therefore Telegraph confidence is reported separately
    # and does not participate in overall confidence.
    # ========================================================

    telegraph_confidence = (
        telegraph_provenance_confidence(
            provenance
        )
    )

    # ========================================================
    # OVERALL CONFIDENCE
    #
    # Conservative rule:
    # critical policy dimensions limit confidence.
    #
    # This prevents strong economic data from hiding
    # weak policy intelligence.
    #
    # IMPORTANT:
    # Telegraph is intentionally NOT included here.
    #
    # Telegraph availability represents provider-derived
    # intelligence availability, not settlement validation.
    # ========================================================

    overall_confidence = min(
        economic_confidence,
        network_confidence,
        compliance_confidence,
        geopolitical_confidence,
        risk_confidence,
    )

    # ========================================================
    # AUTOMATION READINESS
    #
    # Automated recommendation requires strong confidence
    # across all critical settlement dimensions.
    #
    # Telegraph availability alone can never make the
    # system automation-ready.
    # ========================================================

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

    # ========================================================
    # DECISION QUALITY
    # ========================================================

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

    # ========================================================
    # OVERALL STATUS
    # ========================================================

    if overall_confidence >= 0.90:

        overall_status = "HIGH"

    elif overall_confidence >= 0.70:

        overall_status = "MEDIUM"

    elif overall_confidence > 0.0:

        overall_status = "LOW"

    else:

        overall_status = "INCOMPLETE"

    # ========================================================
    # RESULT
    # ========================================================

    return {

        "overall_confidence":
            overall_confidence,

        "overall_status":
            overall_status,

        "automation_readiness":
            automation_readiness,

        "economic": {

            "status":
                economic.get(
                    "status"
                ),

            "confidence":
                economic_confidence,

            "classification":
                classify_confidence(
                    economic_confidence
                ),
        },

        "network": {

            "status":
                provenance.get(
                    "route_network_data"
                ),

            "confidence":
                network_confidence,

            "classification":
                classify_confidence(
                    network_confidence
                ),
        },

        "compliance": {

            "status":
                provenance.get(
                    "compliance"
                ),

            "confidence":
                compliance_confidence,

            "classification":
                classify_confidence(
                    compliance_confidence
                ),
        },

        "geopolitical": {

            "status":
                provenance.get(
                    "geopolitical"
                ),

            "confidence":
                geopolitical_confidence,

            "classification":
                classify_confidence(
                    geopolitical_confidence
                ),
        },

        "risk": {

            "status":
                provenance.get(
                    "route_risk"
                ),

            "confidence":
                risk_confidence,

            "classification":
                classify_confidence(
                    risk_confidence
                ),
        },

        "telegraph": {

            "status":
                provenance.get(
                    "telegraph"
                ),

            "confidence":
                telegraph_confidence,

            "classification":
                classify_confidence(
                    telegraph_confidence
                ),
        },

        # ----------------------------------------------------
        # Telegraph control metadata
        #
        # Telegraph is provider-derived intelligence only.
        # It has no settlement decision authority.
        # ----------------------------------------------------

        "telegraph_control": {

            "role":
                "PROVIDER_DERIVED_INTELLIGENCE_ONLY",

            "decision_authority":
                "NONE",

            "affects_eligibility":
                False,

            "affects_ranking":
                False,

            "affects_recommendation":
                False,
        },

        "decision_quality":
            decision_quality,
    }


# ============================================================
# DISPLAY
# ============================================================

def print_decision_confidence(
    confidence
):

    print(
        "=== DECISION CONFIDENCE ==="
    )

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

    # --------------------------------------------------------
    # Economic
    # --------------------------------------------------------

    economic = confidence["economic"]

    print("Economic data")
    print("-" * 55)

    print(
        f"Status: "
        f"{economic['status']}"
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

    # --------------------------------------------------------
    # Network
    # --------------------------------------------------------

    network = confidence["network"]

    print("Network data")
    print("-" * 55)

    print(
        f"Status: "
        f"{network['status']}"
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

    # --------------------------------------------------------
    # Compliance
    # --------------------------------------------------------

    compliance = confidence["compliance"]

    print("Compliance data")
    print("-" * 55)

    print(
        f"Status: "
        f"{compliance['status']}"
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

    # --------------------------------------------------------
    # Geopolitical
    # --------------------------------------------------------

    geopolitical = confidence["geopolitical"]

    print("Geopolitical data")
    print("-" * 55)

    print(
        f"Status: "
        f"{geopolitical['status']}"
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

    # --------------------------------------------------------
    # Risk
    # --------------------------------------------------------

    risk = confidence["risk"]

    print("Risk data")
    print("-" * 55)

    print(
        f"Status: "
        f"{risk['status']}"
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

    # --------------------------------------------------------
    # Telegraph intelligence
    # --------------------------------------------------------

    telegraph = confidence["telegraph"]

    print("Telegraph intelligence")
    print("-" * 55)

    print(
        f"Status: "
        f"{telegraph['status']}"
    )

    print(
        f"Confidence: "
        f"{telegraph['confidence']}"
    )

    print(
        f"Classification: "
        f"{telegraph['classification']}"
    )

    print()

    # --------------------------------------------------------
    # Telegraph control
    # --------------------------------------------------------

    telegraph_control = confidence[
        "telegraph_control"
    ]

    print("Telegraph control")
    print("-" * 55)

    print(
        f"Role: "
        f"{telegraph_control['role']}"
    )

    print(
        f"Decision authority: "
        f"{telegraph_control['decision_authority']}"
    )

    print(
        f"Affects eligibility: "
        f"{telegraph_control['affects_eligibility']}"
    )

    print(
        f"Affects ranking: "
        f"{telegraph_control['affects_ranking']}"
    )

    print(
        f"Affects recommendation: "
        f"{telegraph_control['affects_recommendation']}"
    )

    print()

    # --------------------------------------------------------
    # Automation readiness
    # --------------------------------------------------------

    print("Automation readiness")
    print("-" * 55)

    print(
        confidence[
            "automation_readiness"
        ]
    )

    print()

    # --------------------------------------------------------
    # Decision quality
    # --------------------------------------------------------

    print("Decision quality")
    print("-" * 55)

    print(
        confidence[
            "decision_quality"
        ]
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