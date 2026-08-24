"""
BRICS Asset / Infrastructure Linkage

Phase 9.8

Purpose:
    Determine whether validated evidence establishes a linkage
    between a digital asset and payment infrastructure within
    a specific jurisdiction.

IMPORTANT:

    Infrastructure availability does NOT imply asset linkage.

    Asset regulation does NOT imply infrastructure linkage.

    Cross-border capability does NOT imply settlement eligibility.

    This module records and validates linkage evidence only.

    It does NOT make a settlement recommendation.
"""


# ============================================================
# CONTROLLED LINKAGE STATES
# ============================================================

LINKAGE_STATUS = (
    "SUPPORTED",
    "NOT_SUPPORTED",
    "CONDITIONAL",
    "UNKNOWN",
)


SOURCE_TYPES = (
    "CENTRAL_BANK",
    "FINANCIAL_REGULATOR",
    "GOVERNMENT",
    "PAYMENT_OPERATOR",
    "LAW",
    "REGULATION",
    "OFFICIAL_GUIDANCE",
    "INTERNATIONAL_ORGANIZATION",
    "REFERENCE",
    "UNKNOWN",
)


# ============================================================
# BUILD LINKAGE EVIDENCE
# ============================================================

def build_linkage_evidence(
    jurisdiction,
    asset,
    infrastructure,
    status,
    source,
    source_type,
    confidence,
    evidence_text,
):
    """
    Build a structured asset/infrastructure linkage record.

    This function records evidence only.

    It does not determine settlement eligibility.
    """

    if status not in LINKAGE_STATUS:

        raise ValueError(
            f"Invalid linkage status: {status}"
        )

    if source_type not in SOURCE_TYPES:

        raise ValueError(
            f"Invalid source type: {source_type}"
        )

    if not 0.0 <= confidence <= 1.0:

        raise ValueError(
            "confidence must be between 0.0 and 1.0"
        )

    if not isinstance(
        evidence_text,
        str,
    ):

        raise ValueError(
            "evidence_text must be a string"
        )

    if not evidence_text.strip():

        raise ValueError(
            "evidence_text cannot be empty"
        )

    return {

        "jurisdiction":
            jurisdiction,

        "asset":
            asset,

        "infrastructure":
            infrastructure,

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
# VALIDATE LINKAGE EVIDENCE
# ============================================================

def validate_linkage_evidence(
    evidence,
):
    """
    Deterministically validate the linkage evidence schema.

    This does NOT verify whether the external source is true.

    It only validates the structure and controlled values.
    """

    required_fields = (
        "jurisdiction",
        "asset",
        "infrastructure",
        "status",
        "source",
        "source_type",
        "confidence",
        "evidence_text",
    )

    for field in required_fields:

        if field not in evidence:

            raise ValueError(
                f"Missing linkage field: {field}"
            )

    if evidence["status"] not in LINKAGE_STATUS:

        raise ValueError(
            f"Invalid linkage status: "
            f"{evidence['status']}"
        )

    if evidence["source_type"] not in SOURCE_TYPES:

        raise ValueError(
            f"Invalid source type: "
            f"{evidence['source_type']}"
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

    if not isinstance(
        evidence["evidence_text"],
        str,
    ):

        raise ValueError(
            "evidence_text must be a string"
        )

    if not evidence["evidence_text"].strip():

        raise ValueError(
            "evidence_text cannot be empty"
        )

    return True


# ============================================================
# DETERMINE LINKAGE STATE
# ============================================================

def determine_linkage_state(
    evidence,
):
    """
    Deterministically interpret the explicit linkage status.

    No inference is performed.
    """

    validate_linkage_evidence(
        evidence
    )

    return evidence["status"]


# ============================================================
# CONTROLLED UNKNOWN EXAMPLE
# ============================================================

def build_example_unknown():
    """
    Conservative test case.

    We have evidence that UPI exists in India,
    but no validated evidence in our current registry
    establishing ETH ↔ UPI linkage.

    Therefore the linkage remains UNKNOWN.
    """

    return build_linkage_evidence(

        jurisdiction="India",

        asset="ETH",

        infrastructure="UPI",

        status="UNKNOWN",

        source="NOT_YET_VALIDATED",

        source_type="UNKNOWN",

        confidence=0.0,

        evidence_text=(
            "No validated jurisdiction-specific evidence "
            "has yet been entered establishing a direct "
            "ETH to UPI settlement linkage."
        ),
    )


# ============================================================
# DISPLAY
# ============================================================

def print_linkage_evidence(
    evidence,
):

    print(
        "=== BRICS ASSET / INFRASTRUCTURE LINKAGE ==="
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
        f"Infrastructure: "
        f"{evidence['infrastructure']}"
    )

    print(
        f"Linkage status: "
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
        "Evidence:"
    )

    print(
        evidence["evidence_text"]
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    evidence = build_example_unknown()

    print_linkage_evidence(
        evidence
    )

    print()

    validate_linkage_evidence(
        evidence
    )

    print()

    print(
        "Deterministic linkage state:",
        determine_linkage_state(
            evidence
        ),
    )

    print()

    print(
        "Settlement recommendation:",
        "NOT_PERFORMED",
    )

    print()

    print("Status: READY")
