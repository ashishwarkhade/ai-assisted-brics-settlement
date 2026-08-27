"""
Phase B — Intelligence Contract

Defines the provider-independent intelligence model.

Purpose:

    Raw Provider Data
            |
            v
    Intelligence Normalizer
            |
            v
    Normalized Intelligence
            |
            v
    Deterministic Decision Engine

This module does NOT determine whether a settlement route
is permitted or recommended.

It only defines structured evidence.

Each evidence record contains:

    metric
    value
    unit
    source
    timestamp
    status
    confidence
    validation
    measurement_type
"""


# ============================================================
# CONTROLLED VALUES
# ============================================================

INTELLIGENCE_STATUS = (
    "AVAILABLE",
    "UNAVAILABLE",
    "STALE",
    "ERROR",
    "INVALID",
)


VALIDATION_STATUS = (
    "VALID",
    "INVALID",
    "NOT_VALIDATED",
)


CONFIDENCE_LEVELS = (
    "HIGH",
    "MEDIUM",
    "LOW",
)


MEASUREMENT_TYPES = (
    "OBSERVED",
    "ESTIMATED",
    "DERIVED",
)


# ============================================================
# VALIDATION HELPERS
# ============================================================

def require_enum(
    value,
    allowed_values,
    field_name,
):
    """
    Validate that a value belongs to an allowed enum.
    """

    if value not in allowed_values:

        raise ValueError(
            f"Invalid {field_name}: {value}"
        )

    return value


# ============================================================
# INTELLIGENCE EVIDENCE
# ============================================================

def build_intelligence_evidence(
    metric,
    value,
    unit,
    source,
    timestamp,
    status,
    confidence,
    validation,
    measurement_type="OBSERVED",
):
    """
    Build one normalized intelligence evidence record.

    This function describes evidence only.

    It does NOT:

        - rank routes
        - determine eligibility
        - calculate risk
        - make settlement decisions
    """

    require_enum(
        status,
        INTELLIGENCE_STATUS,
        "intelligence status",
    )

    require_enum(
        validation,
        VALIDATION_STATUS,
        "validation status",
    )

    require_enum(
        confidence,
        CONFIDENCE_LEVELS,
        "confidence level",
    )

    require_enum(
        measurement_type,
        MEASUREMENT_TYPES,
        "measurement type",
    )

    if metric is None or metric == "":
        raise ValueError(
            "metric is required"
        )

    if source is None or source == "":
        raise ValueError(
            "source is required"
        )

    if timestamp is None or timestamp == "":
        raise ValueError(
            "timestamp is required"
        )

    return {
        "metric": metric,
        "value": value,
        "unit": unit,
        "source": source,
        "timestamp": timestamp,
        "status": status,
        "confidence": confidence,
        "validation": validation,
        "measurement_type": measurement_type,
    }


# ============================================================
# EVIDENCE USABILITY
# ============================================================

def is_usable(evidence):
    """
    Return True only when evidence is:

        - available
        - valid
        - non-null

    Measurement type does not determine usability.

    Both observed and estimated evidence may be usable.
    The DecisionEngine decides whether a particular
    measurement type is acceptable for a particular policy.
    """

    return (
        evidence["status"] == "AVAILABLE"
        and evidence["validation"] == "VALID"
        and evidence["value"] is not None
    )


def is_missing(evidence):
    """
    Return True when evidence cannot currently be used.
    """

    return not is_usable(evidence)


# ============================================================
# ROUTE INTELLIGENCE CONTRACT
# ============================================================

def build_route_intelligence_contract(
    route_id,
    asset,
    network,
    evidence,
):
    """
    Build provider-independent intelligence for one route.

    Example:

        route_id = "bitcoin"
        asset    = "BTC"
        network  = "Bitcoin"

    The evidence list contains normalized evidence records.
    """

    if route_id is None or route_id == "":
        raise ValueError(
            "route_id is required"
        )

    if asset is None or asset == "":
        raise ValueError(
            "asset is required"
        )

    if network is None or network == "":
        raise ValueError(
            "network is required"
        )

    if not isinstance(evidence, list):
        raise ValueError(
            "evidence must be a list"
        )

    return {
        "route_id": route_id,
        "asset": asset,
        "network": network,
        "evidence": evidence,
    }


# ============================================================
# COMPLETE NORMALIZED INTELLIGENCE
# ============================================================

def build_normalized_intelligence(
    request_id,
    generated_at,
    routes,
):
    """
    Build the complete normalized intelligence object.

    This is the object that the future DecisionEngine
    will consume.
    """

    if request_id is None or request_id == "":
        raise ValueError(
            "request_id is required"
        )

    if generated_at is None or generated_at == "":
        raise ValueError(
            "generated_at is required"
        )

    if not isinstance(routes, dict):
        raise ValueError(
            "routes must be a dictionary"
        )

    return {
        "request_id": request_id,
        "generated_at": generated_at,
        "routes": routes,
    }


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    evidence = build_intelligence_evidence(
        metric="bitcoin_fee_rate",
        value=3,
        unit="sat/vByte",
        source="mempool.space",
        timestamp="2026-08-27T11:30:00+00:00",
        status="AVAILABLE",
        confidence="HIGH",
        validation="VALID",
        measurement_type="OBSERVED",
    )

    estimated_cost = build_intelligence_evidence(
        metric="network_cost",
        value=0.3336228,
        unit="USD",
        source="mempool.space + CoinGecko",
        timestamp="2026-08-27T11:30:00+00:00",
        status="AVAILABLE",
        confidence="HIGH",
        validation="VALID",
        measurement_type="ESTIMATED",
    )

    route = build_route_intelligence_contract(
        route_id="bitcoin",
        asset="BTC",
        network="Bitcoin",
        evidence=[
            evidence,
            estimated_cost,
        ],
    )

    normalized = build_normalized_intelligence(
        request_id="phase-b-demo",
        generated_at="2026-08-27T11:30:00+00:00",
        routes={
            "bitcoin": route,
        },
    )

    print("=== INTELLIGENCE EVIDENCE ===")

    for key, value in evidence.items():
        print(f"{key}: {value}")

    print()

    print("=== ESTIMATED COST EVIDENCE ===")

    for key, value in estimated_cost.items():
        print(f"{key}: {value}")

    print()

    print(
        f"Observed fee usable: "
        f"{is_usable(evidence)}"
    )

    print(
        f"Estimated cost usable: "
        f"{is_usable(estimated_cost)}"
    )

    print()

    print("=== NORMALIZED INTELLIGENCE ===")

    print(
        f"Request ID: "
        f"{normalized['request_id']}"
    )

    print(
        f"Routes: "
        f"{list(normalized['routes'].keys())}"
    )