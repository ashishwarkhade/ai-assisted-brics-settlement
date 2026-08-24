"""
BRICS Regulatory Evidence

Phase 9.4

Purpose:
    Represent regulatory evidence using controlled,
    typed states.

Important:

    AI may extract information into this structure.

    AI does NOT determine the final settlement decision.

    The deterministic validation layer is responsible
    for interpreting these states.
"""


# ============================================================
# CONTROLLED ENUMS
# ============================================================

REGULATORY_STATUS = (
    "PERMITTED",
    "PROHIBITED",
    "CONDITIONAL",
    "UNKNOWN",
)


ACTIVITY_TYPES = (
    "DOMESTIC_PAYMENT",
    "CROSS_BORDER_PAYMENT",
    "SETTLEMENT",
    "CUSTODY",
    "EXCHANGE",
    "TRANSFER",
    "UNKNOWN",
)


SOURCE_TYPES = (
    "CENTRAL_BANK",
    "FINANCIAL_REGULATOR",
    "GOVERNMENT",
    "LAW",
    "REGULATION",
    "OFFICIAL_GUIDANCE",
    "INTERNATIONAL_ORGANIZATION",
    "REFERENCE",
    "UNKNOWN",
)


# ============================================================
# ENUM VALIDATION
# ============================================================

def require_enum(
    value,
    allowed_values,
    field_name,
):

    if value not in allowed_values:

        raise ValueError(
            f"Invalid {field_name}: {value}"
        )

    return value


# ============================================================
# EVIDENCE RECORD
# ============================================================

def build_regulatory_evidence(
    jurisdiction,
    asset,
    activity,
    status,
    source,
    source_type,
    confidence,
    evidence_text,
):
    """
    Build a structured regulatory evidence record.

    This function records evidence only.

    It does not create a settlement recommendation.
    """

    require_enum(
        status,
        REGULATORY_STATUS,
        "status",
    )

    require_enum(
        activity,
        ACTIVITY_TYPES,
        "activity",
    )

    require_enum(
        source_type,
        SOURCE_TYPES,
        "source_type",
    )

    if not 0.0 <= confidence <= 1.0:

        raise ValueError(
            "confidence must be between 0.0 and 1.0"
        )

    return {

        "jurisdiction":
            jurisdiction,

        "asset":
            asset,

        "activity":
            activity,

        "status":
            status,

        "source":
            source,

        "source_type":
            source_type,

        "confidence":
            confidence,

        "evidence_text":
            evidence_text,
    }


# ============================================================
# VALIDATE REGULATORY EVIDENCE
# ============================================================

def validate_regulatory_evidence(
    evidence,
):
    """
    Deterministically validate the structure of an
    evidence record.

    This does NOT verify whether the source itself is true.

    It verifies that the record conforms to our schema.
    """

    required_fields = (
        "jurisdiction",
        "asset",
        "activity",
        "status",
        "source",
        "source_type",
        "confidence",
        "evidence_text",
    )

    for field in required_fields:

        if field not in evidence:

            raise ValueError(
                f"Missing evidence field: {field}"
            )

    require_enum(
        evidence["status"],
        REGULATORY_STATUS,
        "status",
    )

    require_enum(
        evidence["activity"],
        ACTIVITY_TYPES,
        "activity",
    )

    require_enum(
        evidence["source_type"],
        SOURCE_TYPES,
        "source_type",
    )

    confidence = evidence["confidence"]

    if not isinstance(
        confidence,
        (int, float),
    ):

        raise ValueError(
            "confidence must be numeric"
        )

    if not 0.0 <= confidence <= 1.0:

        raise ValueError(
            "confidence must be between 0.0 and 1.0"
        )

    return True


# ============================================================
# DETERMINE REGULATORY STATE
# ============================================================

def determine_regulatory_state(
    evidence,
):
    """
    Deterministic interpretation of the typed status.

    IMPORTANT:

        This function does not infer status from prose.

        It only accepts the explicitly typed status.
    """

    validate_regulatory_evidence(
        evidence
    )

    status = evidence["status"]

    if status == "PERMITTED":

        return "PERMITTED"

    if status == "PROHIBITED":

        return "PROHIBITED"

    if status == "CONDITIONAL":

        return "CONDITIONAL"

    return "UNKNOWN"


# ============================================================
# DISPLAY
# ============================================================

def print_regulatory_evidence(
    evidence,
):

    print(
        "=== BRICS REGULATORY EVIDENCE ==="
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
        f"Status: "
        f"{evidence['status']}"
    )

    print(
        f"Source: "
        f"{evidence['source']}"
    )

    print(
        f"Source type: "
        f"{evidence['source_type']}"
    )

    print(
        f"Confidence: "
        f"{evidence['confidence']}"
    )

    print()

    print(
        "Evidence text:"
    )

    print(
        evidence["evidence_text"]
    )


# ============================================================
# CONTROLLED TEST
# ============================================================

def build_example_unknown():

    """
    Example deliberately uses UNKNOWN.

    We are NOT making a regulatory claim about ETH.
    """

    return build_regulatory_evidence(

        jurisdiction="India",

        asset="ETH",

        activity="CROSS_BORDER_PAYMENT",

        status="UNKNOWN",

        source="NOT_YET_VALIDATED",

        source_type="UNKNOWN",

        confidence=0.0,

        evidence_text=(
            "No jurisdiction-specific validated "
            "evidence has yet been entered."
        ),
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    evidence = build_example_unknown()

    print_regulatory_evidence(
        evidence
    )

    print()

    validate_regulatory_evidence(
        evidence
    )

    print()

    print(
        "Deterministic regulatory state:",
        determine_regulatory_state(
            evidence
        ),
    )

    print()

    print("Status: READY")
