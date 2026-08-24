"""
BRICS Deterministic Regulatory Evidence Validator

Phase 9.6

Purpose:
    Provide the deterministic validation gate between
    AI/discovered regulatory evidence and the settlement
    decision layer.

IMPORTANT:

    This validator does NOT:
        - search for evidence
        - interpret legal prose
        - infer regulatory permission
        - make settlement recommendations
        - override the regulatory evidence schema

    It validates the evidence record and determines whether
    the evidence is sufficient to establish a controlled
    regulatory state.

Architecture:

    AI Evidence Discovery
            |
            v
    AI Regulatory Extractor
            |
            v
    Regulatory Evidence
            |
            v
    THIS VALIDATOR
            |
       +----+----+
       |         |
     VALID    INSUFFICIENT
       |         |
       v         v
    State      UNKNOWN
       |
       v
Settlement Decision
"""


from brics_regulatory_evidence import (
    validate_regulatory_evidence,
    determine_regulatory_state,
)


# ============================================================
# VALIDATOR STATUS
# ============================================================

VALIDATOR_STATUS = (
    "VALID",
    "INSUFFICIENT",
    "INVALID",
)


# ============================================================
# VALIDATE EVIDENCE
# ============================================================

def validate_evidence(
    evidence,
):
    """
    Deterministically validate one regulatory evidence record.

    Returns a structured validation result.

    The underlying schema validator remains authoritative.
    """

    try:

        validate_regulatory_evidence(
            evidence
        )

    except (
        ValueError,
        TypeError,
    ) as error:

        return {
            "status": "INVALID",

            "valid": False,

            "reason":
                "REGULATORY_EVIDENCE_SCHEMA_INVALID",

            "error":
                str(error),

            "regulatory_state":
                "UNKNOWN",
        }


    # --------------------------------------------------------
    # Determine explicit regulatory state
    # --------------------------------------------------------

    regulatory_state = (
        determine_regulatory_state(
            evidence
        )
    )


    # --------------------------------------------------------
    # UNKNOWN evidence
    # --------------------------------------------------------

    if regulatory_state == "UNKNOWN":

        return {
            "status": "INSUFFICIENT",

            "valid": True,

            "reason":
                "REGULATORY_EVIDENCE_INSUFFICIENT",

            "error": None,

            "regulatory_state":
                "UNKNOWN",
        }


    # --------------------------------------------------------
    # Explicit controlled state
    # --------------------------------------------------------

    return {
        "status": "VALID",

        "valid": True,

        "reason":
            "REGULATORY_EVIDENCE_VALIDATED",

        "error": None,

        "regulatory_state":
            regulatory_state,
    }


# ============================================================
# BUILD VALIDATED RESULT
# ============================================================

def build_validated_evidence(
    evidence,
):
    """
    Return the original evidence together with the
    deterministic validation result.

    No fields inside the original evidence record are changed.
    """

    validation = validate_evidence(
        evidence
    )

    return {
        "evidence":
            evidence,

        "validation":
            validation,
    }


# ============================================================
# DISPLAY
# ============================================================

def print_validation_result(
    result,
):

    evidence = result["evidence"]
    validation = result["validation"]

    print(
        "=== PHASE 9.6 DETERMINISTIC "
        "REGULATORY VALIDATOR ==="
    )

    print()

    print(
        f"Jurisdiction: "
        f"{evidence['jurisdiction']}"
    )

    print(
        f"Asset: "
        f"{evidence['asset']}"
    )

    print(
        f"Activity: "
        f"{evidence['activity']}"
    )

    print(
        f"Evidence status: "
        f"{evidence['status']}"
    )

    print(
        f"Validator status: "
        f"{validation['status']}"
    )

    print(
        f"Regulatory state: "
        f"{validation['regulatory_state']}"
    )

    print(
        f"Reason: "
        f"{validation['reason']}"
    )

    if validation["error"]:

        print(
            f"Error: "
            f"{validation['error']}"
        )


# ============================================================
# CONTROLLED UNKNOWN TEST
# ============================================================

def build_example_unknown():
    """
    Controlled test using the existing Phase 9.4
    UNKNOWN evidence example.
    """

    from brics_regulatory_evidence import (
        build_example_unknown as build_evidence,
    )

    return build_evidence()


# ============================================================
# CONTROLLED VALIDATED TEST
# ============================================================

def build_example_conditional():
    """
    Structural test using an explicitly typed CONDITIONAL
    regulatory state.

    This is NOT a real-world regulatory claim.
    """

    from brics_regulatory_evidence import (
        build_regulatory_evidence,
    )

    return build_regulatory_evidence(

        jurisdiction="India",

        asset="ETH",

        activity="CROSS_BORDER_PAYMENT",

        status="CONDITIONAL",

        source="EXAMPLE_SOURCE",

        source_type="REFERENCE",

        confidence=0.8,

        evidence_text=(
            "Example evidence supplied only for "
            "deterministic validator testing."
        ),
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print(
        "=== PHASE 9.6 DETERMINISTIC "
        "EVIDENCE VALIDATOR ==="
    )

    print()

    # --------------------------------------------------------
    # UNKNOWN TEST
    # --------------------------------------------------------

    unknown_evidence = (
        build_example_unknown()
    )

    unknown_result = (
        build_validated_evidence(
            unknown_evidence
        )
    )

    print(
        "=== UNKNOWN EVIDENCE TEST ==="
    )

    print_validation_result(
        unknown_result
    )

    print()

    # --------------------------------------------------------
    # CONDITIONAL TEST
    # --------------------------------------------------------

    conditional_evidence = (
        build_example_conditional()
    )

    conditional_result = (
        build_validated_evidence(
            conditional_evidence
        )
    )

    print(
        "=== CONDITIONAL EVIDENCE TEST ==="
    )

    print_validation_result(
        conditional_result
    )

    print()

    print(
        "AI authority:",
        "EXTRACTION_ONLY",
    )

    print(
        "Validator authority:",
        "DETERMINISTIC",
    )

    print(
        "Settlement recommendation:",
        "NOT_PERFORMED",
    )

    print()

    print(
        "Status:",
        "READY",
    )