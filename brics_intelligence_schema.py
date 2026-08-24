"""
BRICS Settlement Intelligence Schema

Phase 9.1

Purpose:
    Define the structured intelligence model used by the
    AI-assisted BRICS settlement path discovery system.

Important:
    This module does NOT determine whether a settlement route
    is permitted.

    It only defines structured evidence.

Architecture:

    Intelligence Discovery
            |
            v
    Structured Intelligence
            |
            v
    Deterministic Validation
            |
            v
    Settlement Decision Engine
"""


# ============================================================
# ENUM VALUES
# ============================================================

JURISDICTION_STATUS = (
    "KNOWN",
    "UNKNOWN",
)


INFRASTRUCTURE_TYPES = (
    "PAYMENT_SYSTEM",
    "FINANCIAL_MESSAGING",
    "BANKING_NETWORK",
    "SETTLEMENT_PLATFORM",
    "UNKNOWN",
)


INFRASTRUCTURE_STATUS = (
    "AVAILABLE",
    "LIMITED",
    "UNKNOWN",
)


ASSET_TYPES = (
    "CRYPTO_ASSET",
    "STABLECOIN",
    "FIAT",
    "CBDC",
    "TOKENIZED_DEPOSIT",
    "UNKNOWN",
)


REGULATORY_STATUS = (
    "PERMITTED",
    "PROHIBITED",
    "CONDITIONAL",
    "REQUIRES_REVIEW",
    "UNKNOWN",
)


LINKAGE_STATUS = (
    "SUPPORTED",
    "NOT_SUPPORTED",
    "CONDITIONAL",
    "UNKNOWN",
)


CROSS_BORDER_STATUS = (
    "SUPPORTED",
    "NOT_SUPPORTED",
    "CONDITIONAL",
    "UNKNOWN",
)


SETTLEMENT_STATUS = (
    "AVAILABLE",
    "BLOCKED",
    "CONDITIONAL",
    "INCOMPLETE",
    "UNKNOWN",
)


SOURCE_TYPES = (
    "OFFICIAL",
    "REGULATOR",
    "CENTRAL_BANK",
    "PAYMENT_OPERATOR",
    "INTERNATIONAL_ORGANIZATION",
    "REFERENCE",
    "SECONDARY",
    "UNKNOWN",
)


# ============================================================
# VALIDATION HELPERS
# ============================================================

def is_valid_enum(value, allowed_values):
    """
    Return True when value belongs to an allowed enum.
    """

    return value in allowed_values


def require_enum(value, allowed_values, field_name):
    """
    Validate an enum field.

    Raises:
        ValueError
    """

    if value not in allowed_values:

        raise ValueError(
            f"Invalid {field_name}: {value}"
        )

    return value


# ============================================================
# EVIDENCE
# ============================================================

def build_evidence(
    value,
    source,
    source_type,
    confidence,
):
    """
    Build a normalized evidence record.
    """

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
        "value": value,
        "source": source,
        "source_type": source_type,
        "confidence": confidence,
    }


# ============================================================
# PAYMENT INFRASTRUCTURE
# ============================================================

def build_payment_infrastructure(
    name,
    jurisdiction,
    infrastructure_type,
    status,
    evidence,
):
    """
    Build structured payment infrastructure intelligence.

    Example:

        UPI
        India
        PAYMENT_SYSTEM
        AVAILABLE

    This does NOT imply crypto settlement support.
    """

    require_enum(
        infrastructure_type,
        INFRASTRUCTURE_TYPES,
        "infrastructure_type",
    )

    require_enum(
        status,
        INFRASTRUCTURE_STATUS,
        "status",
    )

    return {
        "name": name,
        "jurisdiction": jurisdiction,
        "type": infrastructure_type,
        "status": status,
        "evidence": evidence,
    }


# ============================================================
# ASSET
# ============================================================

def build_asset(
    symbol,
    asset_type,
):
    """
    Build normalized asset information.
    """

    require_enum(
        asset_type,
        ASSET_TYPES,
        "asset_type",
    )

    return {
        "symbol": symbol,
        "type": asset_type,
    }


# ============================================================
# REGULATORY INTELLIGENCE
# ============================================================

def build_regulatory_status(
    jurisdiction,
    asset,
    activity,
    status,
    evidence,
):
    """
    Build jurisdiction-specific regulatory intelligence.

    This describes regulatory evidence.

    It does NOT itself create a settlement recommendation.
    """

    require_enum(
        status,
        REGULATORY_STATUS,
        "regulatory_status",
    )

    return {
        "jurisdiction": jurisdiction,
        "asset": asset,
        "activity": activity,
        "status": status,
        "evidence": evidence,
    }


# ============================================================
# INFRASTRUCTURE / ASSET LINKAGE
# ============================================================

def build_asset_linkage(
    infrastructure,
    asset,
    status,
    evidence,
):
    """
    Describe whether evidence exists connecting an
    infrastructure rail to an asset.

    Example:

        UPI -> ETH

    A payment system being available does NOT automatically
    create this relationship.
    """

    require_enum(
        status,
        LINKAGE_STATUS,
        "linkage_status",
    )

    return {
        "infrastructure": infrastructure,
        "asset": asset,
        "status": status,
        "evidence": evidence,
    }


# ============================================================
# CROSS-BORDER CAPABILITY
# ============================================================

def build_cross_border_capability(
    source_jurisdiction,
    destination_jurisdiction,
    infrastructure,
    asset,
    status,
    evidence,
):
    """
    Describe evidence concerning a cross-border settlement path.
    """

    require_enum(
        status,
        CROSS_BORDER_STATUS,
        "cross_border_status",
    )

    return {
        "source_jurisdiction": source_jurisdiction,
        "destination_jurisdiction":
            destination_jurisdiction,
        "infrastructure": infrastructure,
        "asset": asset,
        "status": status,
        "evidence": evidence,
    }


# ============================================================
# SETTLEMENT PATH
# ============================================================

def build_settlement_path(
    source_jurisdiction,
    destination_jurisdiction,
    infrastructure,
    asset,
    regulatory_status,
    linkage_status,
    cross_border_status,
):
    """
    Build a complete settlement-path intelligence record.

    This function does NOT decide whether the path should
    be recommended.

    It only records the current state of the evidence.
    """

    require_enum(
        regulatory_status,
        REGULATORY_STATUS,
        "regulatory_status",
    )

    require_enum(
        linkage_status,
        LINKAGE_STATUS,
        "linkage_status",
    )

    require_enum(
        cross_border_status,
        CROSS_BORDER_STATUS,
        "cross_border_status",
    )

    return {
        "source_jurisdiction":
            source_jurisdiction,

        "destination_jurisdiction":
            destination_jurisdiction,

        "infrastructure":
            infrastructure,

        "asset":
            asset,

        "regulatory_status":
            regulatory_status,

        "linkage_status":
            linkage_status,

        "cross_border_status":
            cross_border_status,
    }


# ============================================================
# INTELLIGENCE RECORD
# ============================================================

def build_intelligence_record(
    jurisdiction,
    infrastructure,
    asset,
    regulatory,
    linkage,
    cross_border,
    settlement_path,
):
    """
    Build the top-level BRICS intelligence record.
    """

    if not jurisdiction:

        raise ValueError(
            "jurisdiction is required"
        )

    return {
        "jurisdiction": jurisdiction,
        "infrastructure": infrastructure,
        "asset": asset,
        "regulatory": regulatory,
        "linkage": linkage,
        "cross_border": cross_border,
        "settlement_path": settlement_path,
    }


# ============================================================
# EXAMPLE
# ============================================================

def example_upi_eth_record():
    """
    Example only.

    IMPORTANT:
        UNKNOWN is intentional.

    The existence of UPI does not establish that ETH
    can be settled through UPI.
    """

    evidence = build_evidence(
        value="UPI payment infrastructure exists",
        source="EXAMPLE_SOURCE",
        source_type="REFERENCE",
        confidence=0.5,
    )

    infrastructure = build_payment_infrastructure(
        name="UPI",
        jurisdiction="India",
        infrastructure_type="PAYMENT_SYSTEM",
        status="AVAILABLE",
        evidence=evidence,
    )

    asset = build_asset(
        symbol="ETH",
        asset_type="CRYPTO_ASSET",
    )

    regulatory = build_regulatory_status(
        jurisdiction="India",
        asset="ETH",
        activity="CROSS_BORDER_SETTLEMENT",
        status="UNKNOWN",
        evidence=evidence,
    )

    linkage = build_asset_linkage(
        infrastructure="UPI",
        asset="ETH",
        status="UNKNOWN",
        evidence=evidence,
    )

    cross_border = build_cross_border_capability(
        source_jurisdiction="India",
        destination_jurisdiction="UNKNOWN",
        infrastructure="UPI",
        asset="ETH",
        status="UNKNOWN",
        evidence=evidence,
    )

    settlement_path = build_settlement_path(
        source_jurisdiction="India",
        destination_jurisdiction="UNKNOWN",
        infrastructure="UPI",
        asset="ETH",
        regulatory_status="UNKNOWN",
        linkage_status="UNKNOWN",
        cross_border_status="UNKNOWN",
    )

    return build_intelligence_record(
        jurisdiction="India",
        infrastructure=infrastructure,
        asset=asset,
        regulatory=regulatory,
        linkage=linkage,
        cross_border=cross_border,
        settlement_path=settlement_path,
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=== BRICS INTELLIGENCE SCHEMA ===")
    print()

    record = example_upi_eth_record()

    print("Example: India / UPI / ETH")
    print()

    print(
        "Infrastructure:",
        record["infrastructure"]["status"],
    )

    print(
        "Regulatory status:",
        record["regulatory"]["status"],
    )

    print(
        "UPI / ETH linkage:",
        record["linkage"]["status"],
    )

    print(
        "Cross-border status:",
        record["cross_border"]["status"],
    )

    print()

    print(
        "Settlement path:",
        record["settlement_path"],
    )

    print()
    print("Status: READY")
