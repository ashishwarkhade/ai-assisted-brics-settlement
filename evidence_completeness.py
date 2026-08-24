"""
BRICS Evidence Completeness Gate

Phase 9.8

Purpose:
    Determine whether the evidence required for deterministic
    settlement decisioning is complete.

IMPORTANT:

    This module does NOT:
        - determine regulatory legality
        - infer missing evidence
        - recommend a settlement route
        - override regulatory evidence
        - make a payment decision

    It only answers:

        "Is the evidence complete enough for the
         deterministic decision engine to proceed?"

    The gate is fail-closed.

    UNKNOWN evidence means INCOMPLETE evidence.
"""


# ============================================================
# REQUIRED EVIDENCE STATES
# ============================================================

VALID_INFRASTRUCTURE_STATES = (
    "AVAILABLE",
    "UNAVAILABLE",
    "UNKNOWN",
)

VALID_REGULATORY_STATES = (
    "PERMITTED",
    "PROHIBITED",
    "CONDITIONAL",
    "UNKNOWN",
)

VALID_LINKAGE_STATES = (
    "ESTABLISHED",
    "NOT_ESTABLISHED",
    "CONDITIONAL",
    "UNKNOWN",
)

VALID_CROSS_BORDER_STATES = (
    "SUPPORTED",
    "NOT_SUPPORTED",
    "CONDITIONAL",
    "UNKNOWN",
)


# ============================================================
# COMPLETENESS RESULT
# ============================================================

COMPLETE = "COMPLETE"
INCOMPLETE = "INCOMPLETE"


# ============================================================
# VALIDATE EVIDENCE STRUCTURE
# ============================================================

def validate_jurisdiction_evidence(
    evidence,
):
    """
    Validate the minimum jurisdiction evidence structure.

    This is structural validation only.

    It does not verify whether the evidence is factually true.
    """

    required_fields = (
        "jurisdiction",
        "infrastructure",
        "regulatory",
        "linkage",
    )

    for field in required_fields:

        if field not in evidence:

            raise ValueError(
                f"Missing jurisdiction evidence field: {field}"
            )

    infrastructure = evidence["infrastructure"]
    regulatory = evidence["regulatory"]
    linkage = evidence["linkage"]

    infrastructure_required = (
        "name",
        "status",
        "source",
        "source_type",
        "confidence",
    )

    regulatory_required = (
        "asset",
        "activity",
        "status",
        "source",
        "confidence",
    )

    linkage_required = (
        "asset",
        "infrastructure",
        "status",
        "source",
        "confidence",
    )

    for field in infrastructure_required:

        if field not in infrastructure:

            raise ValueError(
                "Missing infrastructure evidence field: "
                f"{field}"
            )

    for field in regulatory_required:

        if field not in regulatory:

            raise ValueError(
                "Missing regulatory evidence field: "
                f"{field}"
            )

    for field in linkage_required:

        if field not in linkage:

            raise ValueError(
                "Missing linkage evidence field: "
                f"{field}"
            )

    if infrastructure["status"] not in VALID_INFRASTRUCTURE_STATES:

        raise ValueError(
            "Invalid infrastructure status: "
            f"{infrastructure['status']}"
        )

    if regulatory["status"] not in VALID_REGULATORY_STATES:

        raise ValueError(
            "Invalid regulatory status: "
            f"{regulatory['status']}"
        )

    if linkage["status"] not in VALID_LINKAGE_STATES:

        raise ValueError(
            "Invalid linkage status: "
            f"{linkage['status']}"
        )

    for name, item in (
        ("infrastructure", infrastructure),
        ("regulatory", regulatory),
        ("linkage", linkage),
    ):

        confidence = item["confidence"]

        if not isinstance(
            confidence,
            (int, float),
        ):

            raise ValueError(
                f"{name} confidence must be numeric"
            )

        if not 0.0 <= confidence <= 1.0:

            raise ValueError(
                f"{name} confidence must be "
                "between 0.0 and 1.0"
            )

    return True


# ============================================================
# CHECK INDIVIDUAL EVIDENCE COMPONENTS
# ============================================================

def check_infrastructure(
    infrastructure,
):
    """
    Infrastructure must be explicitly AVAILABLE.

    UNKNOWN is incomplete.
    """

    return (
        infrastructure["status"] == "AVAILABLE"
    )


def check_regulatory(
    regulatory,
):
    """
    Regulatory evidence must be explicitly established.

    PERMITTED or CONDITIONAL are considered
    sufficiently established for the next
    deterministic decision stage.

    UNKNOWN is incomplete.

    PROHIBITED is complete evidence, but it
    should subsequently cause the decision engine
    to reject the route.
    """

    return (
        regulatory["status"]
        in (
            "PERMITTED",
            "PROHIBITED",
            "CONDITIONAL",
        )
    )


def check_linkage(
    linkage,
):
    """
    Asset/infrastructure linkage must be explicitly
    established, not merely assumed.

    UNKNOWN is incomplete.
    """

    return (
        linkage["status"]
        in (
            "ESTABLISHED",
            "NOT_ESTABLISHED",
            "CONDITIONAL",
        )
    )


# ============================================================
# BUILD COMPLETENESS RESULT
# ============================================================

def build_evidence_completeness(
    evidence,
):
    """
    Deterministically evaluate evidence completeness.

    No inference is performed.

    The result is COMPLETE only when all required
    evidence categories are explicitly established.
    """

    validate_jurisdiction_evidence(
        evidence
    )

    infrastructure = evidence["infrastructure"]
    regulatory = evidence["regulatory"]
    linkage = evidence["linkage"]

    infrastructure_complete = check_infrastructure(
        infrastructure
    )

    regulatory_complete = check_regulatory(
        regulatory
    )

    linkage_complete = check_linkage(
        linkage
    )

    checks = {
        "infrastructure":
            infrastructure_complete,

        "regulatory":
            regulatory_complete,

        "asset_infrastructure_linkage":
            linkage_complete,
    }

    missing = [
        name
        for name, complete in checks.items()
        if not complete
    ]

    if missing:

        status = INCOMPLETE

        reason = (
            "REQUIRED_EVIDENCE_INCOMPLETE"
        )

    else:

        status = COMPLETE

        reason = (
            "REQUIRED_EVIDENCE_COMPLETE"
        )

    return {
        "jurisdiction":
            evidence["jurisdiction"],

        "status":
            status,

        "reason":
            reason,

        "checks":
            checks,

        "missing":
            missing,

        "settlement_recommendation":
            "NOT_PERFORMED",
    }


# ============================================================
# DISPLAY
# ============================================================

def print_completeness_result(
    evidence,
    result,
):
    """
    Display the deterministic completeness result.
    """

    print(
        "=== PHASE 9.8 EVIDENCE COMPLETENESS GATE ==="
    )

    print()

    print(
        f"Jurisdiction: "
        f"{evidence['jurisdiction']}"
    )

    print()

    print(
        "Evidence checks:"
    )

    for name, complete in result["checks"].items():

        if complete:

            state = "COMPLETE"

        else:

            state = "INCOMPLETE"

        print(
            f"  {name}: {state}"
        )

    print()

    print(
        f"Completeness status: "
        f"{result['status']}"
    )

    print(
        f"Reason: "
        f"{result['reason']}"
    )

    print()

    if result["missing"]:

        print(
            "Missing evidence:"
        )

        for item in result["missing"]:

            print(
                f"  - {item}"
            )

    else:

        print(
            "Missing evidence: NONE"
        )

    print()

    print(
        "Settlement recommendation: "
        "NOT_PERFORMED"
    )


# ============================================================
# CONTROLLED TEST
# ============================================================

def build_example_incomplete():
    """
    Current project state.

    India has UPI availability evidence,
    but ETH regulatory status and ETH/UPI
    linkage remain UNKNOWN.
    """

    return {
        "jurisdiction": "India",

        "infrastructure": {
            "name": "UPI",
            "status": "AVAILABLE",
            "source": "NPCI",
            "source_type": "PAYMENT_OPERATOR",
            "confidence": 1.0,
        },

        "regulatory": {
            "asset": "ETH",
            "activity": "CROSS_BORDER_PAYMENT",
            "status": "UNKNOWN",
            "source": "NOT_YET_VALIDATED",
            "confidence": 0.0,
        },

        "linkage": {
            "asset": "ETH",
            "infrastructure": "UPI",
            "status": "UNKNOWN",
            "source": "NOT_YET_VALIDATED",
            "confidence": 0.0,
        },
    }


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    evidence = build_example_incomplete()

    result = build_evidence_completeness(
        evidence
    )

    print_completeness_result(
        evidence,
        result,
    )

    print()

    print(
        "Decision authority:",
        "NOT_PERFORMED",
    )

    print(
        "Gate authority:",
        "DETERMINISTIC",
    )

    print()

    print("Status: READY")
