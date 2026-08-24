# ============================================================
# BRICS EVIDENCE ACQUISITION
# Phase 9.A.4
# ============================================================


EVIDENCE_VERSION = "9.A.4"


# ============================================================
# VALID SOURCE TYPES
# ============================================================

VALID_SOURCE_TYPES = {
    "OFFICIAL",
    "REGULATORY",
    "INTERNATIONAL",
    "SECONDARY",
    "UNKNOWN",
}


# ============================================================
# VALID EVIDENCE QUALITY STATES
# ============================================================

VALID_EVIDENCE_QUALITY = {
    "COMPLETE",
    "PARTIAL",
    "MISSING",
}


# ============================================================
# VALID FRESHNESS STATES
# ============================================================

VALID_FRESHNESS_STATES = {
    "CURRENT",
    "DATED",
    "UNKNOWN",
}


# ============================================================
# SOURCE CLASSIFICATION
# ============================================================

def classify_source(source_type):

    if not source_type:
        return "UNKNOWN"

    source_type = source_type.upper()

    if source_type in VALID_SOURCE_TYPES:
        return source_type

    return "UNKNOWN"


# ============================================================
# EVIDENCE QUALITY
# ============================================================

def classify_evidence_quality(
    evidence_text,
    jurisdiction,
    source_url,
):
    """
    Determine whether the evidence record contains
    the minimum metadata required for downstream
    processing.

    This does NOT determine whether the evidence
    supports a regulatory conclusion.
    """

    if not evidence_text:
        return "MISSING"

    if not jurisdiction:
        return "PARTIAL"

    if not source_url:
        return "PARTIAL"

    return "COMPLETE"


# ============================================================
# SOURCE FRESHNESS
# ============================================================

def classify_freshness(document_date):
    """
    Classify whether a document has a known date.

    This function deliberately does NOT determine
    whether the document is legally current.

    CURRENT means:
        A date is available and the source can be
        treated as having known timing.

    DATED means:
        The document is explicitly identified as dated
        but is not being treated as current.

    UNKNOWN means:
        No document date is available.
    """

    if not document_date:
        return "UNKNOWN"

    return "CURRENT"


# ============================================================
# BUILD EVIDENCE RECORD
# ============================================================

def build_evidence_record(
    source_id,
    jurisdiction,
    source_type,
    source_url,
    evidence_text,
    document_date=None,
):
    """
    Build a raw evidence record.

    This module records and classifies evidence.

    It does NOT determine:

        PERMITTED
        PROHIBITED
        CONDITIONAL
        UNKNOWN

    Source classification, evidence quality,
    and freshness do not imply regulatory permission.
    """

    source_classification = classify_source(
        source_type
    )

    evidence_quality = classify_evidence_quality(
        evidence_text,
        jurisdiction,
        source_url,
    )

    freshness = classify_freshness(
        document_date
    )

    return {
        "evidence_version": EVIDENCE_VERSION,

        "source_id": source_id,

        "jurisdiction": jurisdiction,

        "source_type": source_classification,

        "source_url": source_url,

        "document_date": document_date,

        "freshness": freshness,

        "evidence_text": evidence_text,

        "evidence_quality": evidence_quality,

        "validation_status": "UNVALIDATED",
    }


# ============================================================
# DISPLAY EVIDENCE RECORD
# ============================================================

def print_evidence_record(record):

    print("=== BRICS EVIDENCE RECORD ===")

    print()

    print(
        f"Evidence version: "
        f"{record['evidence_version']}"
    )

    print()

    print("Source")
    print("-" * 55)

    print(
        f"Source ID: "
        f"{record['source_id']}"
    )

    print(
        f"Jurisdiction: "
        f"{record['jurisdiction']}"
    )

    print(
        f"Source type: "
        f"{record['source_type']}"
    )

    print(
        f"Source URL: "
        f"{record['source_url']}"
    )

    print(
        f"Document date: "
        f"{record['document_date']}"
    )

    print(
        f"Freshness: "
        f"{record['freshness']}"
    )

    print()

    print("Evidence")
    print("-" * 55)

    print(
        record["evidence_text"]
    )

    print()

    print("Evidence quality:")

    print(
        f"  {record['evidence_quality']}"
    )

    print()

    print(
        f"Validation status: "
        f"{record['validation_status']}"
    )


# ============================================================
# CLASSIFICATION TEST
# ============================================================

def run_classification_test():

    print(
        "=== BRICS EVIDENCE SOURCE "
        "CLASSIFICATION ==="
    )

    print()

    test_sources = [
        "OFFICIAL",
        "REGULATORY",
        "INTERNATIONAL",
        "SECONDARY",
        "unknown_source",
        None,
    ]

    for source in test_sources:

        result = classify_source(
            source
        )

        print(
            f"Input: {source} "
            f"-> Classification: {result}"
        )


# ============================================================
# EVIDENCE QUALITY TEST
# ============================================================

def run_quality_test():

    print()

    print(
        "=== BRICS EVIDENCE QUALITY "
        "CLASSIFICATION ==="
    )

    print()

    tests = [
        {
            "name": "Complete evidence",
            "jurisdiction": "India",
            "source_url": "https://example.org/source",
            "evidence_text": (
                "Sample regulatory evidence."
            ),
        },
        {
            "name": "Partial evidence",
            "jurisdiction": "India",
            "source_url": None,
            "evidence_text": (
                "Sample regulatory evidence."
            ),
        },
        {
            "name": "Missing evidence",
            "jurisdiction": "India",
            "source_url": "https://example.org/source",
            "evidence_text": None,
        },
    ]

    for test in tests:

        result = classify_evidence_quality(
            test["evidence_text"],
            test["jurisdiction"],
            test["source_url"],
        )

        print(
            f"{test['name']} "
            f"-> {result}"
        )


# ============================================================
# FRESHNESS TEST
# ============================================================

def run_freshness_test():

    print()

    print(
        "=== BRICS SOURCE FRESHNESS "
        "CLASSIFICATION ==="
    )

    print()

    tests = [
        "2026-08-24",
        "2025-01-15",
        None,
    ]

    for document_date in tests:

        result = classify_freshness(
            document_date
        )

        print(
            f"Document date: {document_date} "
            f"-> Freshness: {result}"
        )


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    run_classification_test()

    run_quality_test()

    run_freshness_test()

    evidence = build_evidence_record(

        source_id="TEST-IN-001",

        jurisdiction="India",

        source_type="OFFICIAL",

        source_url="NOT_YET_CONNECTED",

        document_date=None,

        evidence_text=(
            "Sample regulatory evidence. "
            "Meaning has not yet been validated."
        ),
    )

    print()

    print_evidence_record(
        evidence
    )

    print()

    print("Status: READY")