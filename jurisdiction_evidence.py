"""
BRICS Jurisdiction Evidence

Phase 9.8.1

Purpose:
    Combine independently validated evidence associated with
    a jurisdiction into one structured intelligence record.

IMPORTANT:

    This module does NOT make a settlement recommendation.

    It does NOT infer:

        - regulatory permission
        - asset support
        - infrastructure linkage
        - cross-border settlement capability

    Each evidence dimension remains independent.

Architecture:

    Jurisdiction
        |
        +-- Infrastructure Evidence
        |
        +-- Regulatory Evidence
        |
        +-- Asset / Infrastructure Linkage
        |
        v
    Jurisdiction Intelligence

    Decision authority remains with the deterministic
    settlement decision engine.
"""


# ============================================================
# CONTROLLED STATES
# ============================================================

INFRASTRUCTURE_STATUS = (
    "AVAILABLE",
    "UNAVAILABLE",
    "UNKNOWN",
)


REGULATORY_STATUS = (
    "PERMITTED",
    "PROHIBITED",
    "CONDITIONAL",
    "UNKNOWN",
)


LINKAGE_STATUS = (
    "SUPPORTED",
    "NOT_SUPPORTED",
    "CONDITIONAL",
    "UNKNOWN",
)


# ============================================================
# BUILD JURISDICTION EVIDENCE
# ============================================================

def build_jurisdiction_evidence(
    jurisdiction,
    infrastructure,
    infrastructure_status,
    infrastructure_source,
    infrastructure_source_type,
    infrastructure_confidence,
    infrastructure_evidence_text,
    regulatory_evidence,
    linkage_evidence,
):
    """
    Build a structured jurisdiction evidence record.

    Each evidence dimension is preserved independently.

    No settlement decision is made here.
    """

    # --------------------------------------------------------
    # Infrastructure validation
    # --------------------------------------------------------

    if infrastructure_status not in INFRASTRUCTURE_STATUS:

        raise ValueError(
            f"Invalid infrastructure status: "
            f"{infrastructure_status}"
        )

    if not 0.0 <= infrastructure_confidence <= 1.0:

        raise ValueError(
            "infrastructure confidence must be "
            "between 0.0 and 1.0"
        )

    if not isinstance(
        infrastructure_evidence_text,
        str,
    ):

        raise ValueError(
            "infrastructure evidence text "
            "must be a string"
        )

    if not infrastructure_evidence_text.strip():

        raise ValueError(
            "infrastructure evidence text "
            "cannot be empty"
        )

    # --------------------------------------------------------
    # Regulatory evidence validation
    # --------------------------------------------------------

    if not isinstance(
        regulatory_evidence,
        dict,
    ):

        raise ValueError(
            "regulatory_evidence must be a dictionary"
        )

    required_regulatory_fields = (
        "jurisdiction",
        "asset",
        "activity",
        "status",
        "source",
        "source_type",
        "confidence",
        "evidence_text",
    )

    for field in required_regulatory_fields:

        if field not in regulatory_evidence:

            raise ValueError(
                f"Missing regulatory evidence field: "
                f"{field}"
            )

    if regulatory_evidence["status"] not in REGULATORY_STATUS:

        raise ValueError(
            "Invalid regulatory evidence status: "
            f"{regulatory_evidence['status']}"
        )

    # --------------------------------------------------------
    # Linkage evidence validation
    # --------------------------------------------------------

    if not isinstance(
        linkage_evidence,
        dict,
    ):

        raise ValueError(
            "linkage_evidence must be a dictionary"
        )

    required_linkage_fields = (
        "jurisdiction",
        "asset",
        "infrastructure",
        "status",
        "source",
        "source_type",
        "confidence",
        "evidence_text",
    )

    for field in required_linkage_fields:

        if field not in linkage_evidence:

            raise ValueError(
                f"Missing linkage evidence field: "
                f"{field}"
            )

    if linkage_evidence["status"] not in LINKAGE_STATUS:

        raise ValueError(
            "Invalid linkage evidence status: "
            f"{linkage_evidence['status']}"
        )

    # --------------------------------------------------------
    # Jurisdiction consistency
    # --------------------------------------------------------

    if regulatory_evidence["jurisdiction"] != jurisdiction:

        raise ValueError(
            "Regulatory evidence jurisdiction does not "
            "match jurisdiction record"
        )

    if linkage_evidence["jurisdiction"] != jurisdiction:

        raise ValueError(
            "Linkage evidence jurisdiction does not "
            "match jurisdiction record"
        )

    # --------------------------------------------------------
    # Infrastructure consistency
    # --------------------------------------------------------

    if linkage_evidence["infrastructure"] != infrastructure:

        raise ValueError(
            "Linkage infrastructure does not match "
            "jurisdiction infrastructure"
        )

    # --------------------------------------------------------
    # Build structured record
    # --------------------------------------------------------

    return {

        "jurisdiction":
            jurisdiction,

        "infrastructure": {

            "name":
                infrastructure,

            "status":
                infrastructure_status,

            "source":
                infrastructure_source,

            "source_type":
                infrastructure_source_type,

            "confidence":
                infrastructure_confidence,

            "evidence_text":
                infrastructure_evidence_text,
        },

        "regulatory":
            regulatory_evidence,

        "linkage":
            linkage_evidence,
    }


# ============================================================
# VALIDATE JURISDICTION EVIDENCE
# ============================================================

def validate_jurisdiction_evidence(
    evidence,
):
    """
    Deterministically validate the combined evidence record.

    This function validates structure only.

    It does not determine whether the underlying claims
    are legally or operationally true.
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
                f"Missing jurisdiction evidence field: "
                f"{field}"
            )

    infrastructure = evidence["infrastructure"]

    if infrastructure["status"] not in INFRASTRUCTURE_STATUS:

        raise ValueError(
            "Invalid infrastructure status"
        )

    regulatory = evidence["regulatory"]

    if regulatory["status"] not in REGULATORY_STATUS:

        raise ValueError(
            "Invalid regulatory status"
        )

    linkage = evidence["linkage"]

    if linkage["status"] not in LINKAGE_STATUS:

        raise ValueError(
            "Invalid linkage status"
        )

    return True


# ============================================================
# DETERMINE EVIDENCE COMPLETENESS
# ============================================================

def determine_evidence_completeness(
    evidence,
):
    """
    Determine whether all three intelligence dimensions
    contain sufficient non-UNKNOWN states.

    This is NOT a settlement eligibility decision.

    It only describes evidence completeness.
    """

    validate_jurisdiction_evidence(
        evidence
    )

    infrastructure_status = (
        evidence["infrastructure"]["status"]
    )

    regulatory_status = (
        evidence["regulatory"]["status"]
    )

    linkage_status = (
        evidence["linkage"]["status"]
    )

    if infrastructure_status == "UNKNOWN":

        return "INCOMPLETE"

    if regulatory_status == "UNKNOWN":

        return "INCOMPLETE"

    if linkage_status == "UNKNOWN":

        return "INCOMPLETE"

    return "COMPLETE"


# ============================================================
# CONTROLLED INDIA EXAMPLE
# ============================================================

def build_india_example():
    """
    Controlled India example.

    Evidence currently establishes:

        UPI:
            AVAILABLE

        ETH regulatory status for the specific
        CROSS_BORDER_PAYMENT activity:
            UNKNOWN

        ETH ↔ UPI linkage:
            UNKNOWN

    Therefore the combined evidence remains INCOMPLETE.
    """

    regulatory_evidence = {

        "jurisdiction":
            "India",

        "asset":
            "ETH",

        "activity":
            "CROSS_BORDER_PAYMENT",

        "status":
            "UNKNOWN",

        "source":
            "NOT_YET_VALIDATED",

        "source_type":
            "UNKNOWN",

        "confidence":
            0.0,

        "evidence_text":
            (
                "No validated jurisdiction-specific "
                "regulatory evidence has yet been entered "
                "for ETH cross-border payment activity."
            ),
    }

    linkage_evidence = {

        "jurisdiction":
            "India",

        "asset":
            "ETH",

        "infrastructure":
            "UPI",

        "status":
            "UNKNOWN",

        "source":
            "NOT_YET_VALIDATED",

        "source_type":
            "UNKNOWN",

        "confidence":
            0.0,

        "evidence_text":
            (
                "No validated evidence currently "
                "establishes a direct ETH to UPI "
                "settlement linkage."
            ),
    }

    return build_jurisdiction_evidence(

        jurisdiction="India",

        infrastructure="UPI",

        infrastructure_status="AVAILABLE",

        infrastructure_source="NPCI",

        infrastructure_source_type="PAYMENT_OPERATOR",

        infrastructure_confidence=1.0,

        infrastructure_evidence_text=(
            "NPCI identifies UPI as an instant payment "
            "system operated by NPCI and used for "
            "transfers between participating bank accounts."
        ),

        regulatory_evidence=
            regulatory_evidence,

        linkage_evidence=
            linkage_evidence,
    )


# ============================================================
# DISPLAY
# ============================================================

def print_jurisdiction_evidence(
    evidence,
):

    print(
        "=== BRICS JURISDICTION EVIDENCE ==="
    )

    print()

    print(
        f"Jurisdiction: "
        f"{evidence['jurisdiction']}"
    )

    print()

    # --------------------------------------------------------
    # Infrastructure
    # --------------------------------------------------------

    infrastructure = evidence[
        "infrastructure"
    ]

    print(
        "Infrastructure:"
    )

    print(
        f"  Name: "
        f"{infrastructure['name']}"
    )

    print(
        f"  Status: "
        f"{infrastructure['status']}"
    )

    print(
        f"  Source: "
        f"{infrastructure['source']}"
    )

    print(
        f"  Source type: "
        f"{infrastructure['source_type']}"
    )

    print(
        f"  Confidence: "
        f"{infrastructure['confidence']}"
    )

    # --------------------------------------------------------
    # Regulatory
    # --------------------------------------------------------

    regulatory = evidence[
        "regulatory"
    ]

    print()

    print(
        "Regulatory:"
    )

    print(
        f"  Asset: "
        f"{regulatory['asset']}"
    )

    print(
        f"  Activity: "
        f"{regulatory['activity']}"
    )

    print(
        f"  Status: "
        f"{regulatory['status']}"
    )

    print(
        f"  Source: "
        f"{regulatory['source']}"
    )

    print(
        f"  Confidence: "
        f"{regulatory['confidence']}"
    )

    # --------------------------------------------------------
    # Linkage
    # --------------------------------------------------------

    linkage = evidence[
        "linkage"
    ]

    print()

    print(
        "Asset / Infrastructure Linkage:"
    )

    print(
        f"  Asset: "
        f"{linkage['asset']}"
    )

    print(
        f"  Infrastructure: "
        f"{linkage['infrastructure']}"
    )

    print(
        f"  Status: "
        f"{linkage['status']}"
    )

    print(
        f"  Source: "
        f"{linkage['source']}"
    )

    print(
        f"  Confidence: "
        f"{linkage['confidence']}"
    )

    # --------------------------------------------------------
    # Completeness
    # --------------------------------------------------------

    completeness = (
        determine_evidence_completeness(
            evidence
        )
    )

    print()

    print(
        "Evidence completeness:",
        completeness,
    )

    print(
        "Settlement recommendation:",
        "NOT_PERFORMED",
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    evidence = build_india_example()

    print_jurisdiction_evidence(
        evidence
    )

    print()

    validate_jurisdiction_evidence(
        evidence
    )

    print()

    print(
        "Validation status:",
        "VALID",
    )

    print()

    print(
        "Status: READY"
    )
