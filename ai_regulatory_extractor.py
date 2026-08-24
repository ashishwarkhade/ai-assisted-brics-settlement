"""
AI Regulatory Evidence Extractor

Phase 9.5

Purpose:
    Extract candidate regulatory evidence into the existing
    BRICS regulatory evidence schema.

IMPORTANT:

    AI is an evidence extractor only.

    AI does NOT:
        - recommend a settlement route
        - determine settlement eligibility
        - override deterministic policy
        - invent regulatory evidence
        - convert ambiguous evidence into PERMITTED

    The deterministic regulatory validator remains
    authoritative.

Architecture:

    Regulatory Evidence Discovery
              |
              v
    AI Regulatory Extractor
              |
              v
    Structured Evidence
              |
              v
    Deterministic Validation
              |
              v
    Regulatory State
              |
              v
    Settlement Decision
"""


from brics_regulatory_evidence import (
    build_regulatory_evidence,
    validate_regulatory_evidence,
    determine_regulatory_state,
)


# ============================================================
# EXTRACTION REQUEST
# ============================================================

def build_extraction_request(
    jurisdiction,
    asset,
    activity,
):
    """
    Build the controlled input for regulatory evidence
    extraction.

    This function does not make a regulatory determination.
    """

    return {
        "jurisdiction": jurisdiction,
        "asset": asset,
        "activity": activity,
    }


# ============================================================
# AI EXTRACTION
# ============================================================

def extract_regulatory_evidence(
    jurisdiction,
    asset,
    activity,
    source="NOT_YET_VALIDATED",
    source_type="UNKNOWN",
    evidence_text=None,
    status="UNKNOWN",
    confidence=0.0,
):
    """
    Convert discovered regulatory information into the
    existing BRICS regulatory evidence schema.

    The extractor accepts an explicitly supplied status.

    It does NOT infer regulatory permission from prose.

    If validated evidence has not been supplied, the safe
    state is UNKNOWN.
    """

    if evidence_text is None:

        evidence_text = (
            "No validated jurisdiction-specific "
            "regulatory evidence has been supplied."
        )

    evidence = build_regulatory_evidence(

        jurisdiction=jurisdiction,

        asset=asset,

        activity=activity,

        status=status,

        source=source,

        source_type=source_type,

        confidence=confidence,

        evidence_text=evidence_text,
    )

    return evidence


# ============================================================
# DETERMINISTIC VALIDATION
# ============================================================

def validate_extracted_evidence(
    evidence,
):
    """
    Validate extracted evidence using the authoritative
    deterministic regulatory schema.
    """

    validate_regulatory_evidence(
        evidence
    )

    return True


# ============================================================
# DETERMINE CONTROLLED STATE
# ============================================================

def get_regulatory_state(
    evidence,
):
    """
    Return the deterministic regulatory state.

    No inference is performed.
    """

    validate_extracted_evidence(
        evidence
    )

    return determine_regulatory_state(
        evidence
    )


# ============================================================
# COMPLETE EXTRACTION PIPELINE
# ============================================================

def build_regulatory_extraction(
    jurisdiction,
    asset,
    activity,
    source="NOT_YET_VALIDATED",
    source_type="UNKNOWN",
    evidence_text=None,
    status="UNKNOWN",
    confidence=0.0,
):
    """
    Execute the complete Phase 9.5 extraction pipeline.

    Flow:

        Input
          |
          v
        Extract
          |
          v
        Validate
          |
          v
        Determine controlled state
    """

    evidence = extract_regulatory_evidence(

        jurisdiction=jurisdiction,

        asset=asset,

        activity=activity,

        source=source,

        source_type=source_type,

        evidence_text=evidence_text,

        status=status,

        confidence=confidence,
    )

    validate_extracted_evidence(
        evidence
    )

    regulatory_state = get_regulatory_state(
        evidence
    )

    return {
        "evidence": evidence,

        "regulatory_state":
            regulatory_state,

        "extraction_status":
            "VALIDATED",
    }


# ============================================================
# DISPLAY
# ============================================================

def print_extraction_result(
    result,
):

    evidence = result["evidence"]

    print(
        "=== AI REGULATORY EXTRACTION ==="
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
        f"Regulatory status: "
        f"{evidence['status']}"
    )

    print(
        f"Regulatory state: "
        f"{result['regulatory_state']}"
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

    print()

    print(
        f"Extraction status: "
        f"{result['extraction_status']}"
    )


# ============================================================
# CONTROLLED UNKNOWN TEST
# ============================================================

def build_example_unknown():
    """
    Controlled test using UNKNOWN.

    This deliberately does not make a regulatory claim
    about ETH in India.
    """

    return build_regulatory_extraction(

        jurisdiction="India",

        asset="ETH",

        activity="CROSS_BORDER_PAYMENT",

        source="NOT_YET_VALIDATED",

        source_type="UNKNOWN",

        status="UNKNOWN",

        confidence=0.0,

        evidence_text=(
            "No jurisdiction-specific validated "
            "regulatory evidence has yet been supplied."
        ),
    )


# ============================================================
# CONTROLLED VALIDATED-EVIDENCE TEST
# ============================================================

def build_example_validated():
    """
    Schema test using explicitly supplied evidence.

    IMPORTANT:

        This is a structural test only.

        It is NOT a claim that the referenced regulatory
        status is actually true in the real world.
    """

    return build_regulatory_extraction(

        jurisdiction="India",

        asset="ETH",

        activity="CROSS_BORDER_PAYMENT",

        source="EXAMPLE_SOURCE",

        source_type="REFERENCE",

        status="CONDITIONAL",

        confidence=0.8,

        evidence_text=(
            "Example evidence supplied for schema "
            "validation only."
        ),
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print(
        "=== PHASE 9.5 AI REGULATORY EXTRACTOR ==="
    )

    print()

    result = build_example_unknown()

    print_extraction_result(
        result
    )

    print()

    print(
        "AI authority:",
        "EXTRACTION_ONLY",
    )

    print(
        "Decision authority:",
        "DETERMINISTIC_VALIDATOR",
    )

    print()

    print(
        "Status:",
        "READY",
    )