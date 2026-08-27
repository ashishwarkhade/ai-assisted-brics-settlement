"""
Phase B — Intelligence Normalizer

Converts the existing route_intelligence format into the
provider-independent Intelligence Contract.

This module does not make settlement decisions.
"""


from datetime import datetime, timezone

from intelligence_contract import (
    build_intelligence_evidence,
    build_route_intelligence_contract,
    build_normalized_intelligence,
)


# ============================================================
# STATUS MAPPING
# ============================================================

def normalize_status(status):
    """
    Convert existing provider status values into the
    canonical intelligence status.
    """

    mapping = {
        "REAL": "AVAILABLE",
        "REAL_OBSERVED": "AVAILABLE",
        "REAL_NETWORK_DATA": "AVAILABLE",

        "NOT_CALCULATED": "UNAVAILABLE",
        "UNKNOWN": "UNAVAILABLE",
        "ERROR": "ERROR",
        "INVALID": "INVALID",
    }

    return mapping.get(
        status,
        "UNAVAILABLE",
    )


# ============================================================
# CONFIDENCE MAPPING
# ============================================================

def normalize_confidence(confidence):
    """
    Convert numeric confidence into the canonical confidence
    level used by the Intelligence Contract.
    """

    if confidence is None:
        return "LOW"

    if confidence >= 0.80:
        return "HIGH"

    if confidence >= 0.50:
        return "MEDIUM"

    return "LOW"


# ============================================================
# VALIDATION
# ============================================================

def determine_validation(
    value,
    status,
):
    """
    Determine whether the normalized evidence can be treated
    as structurally valid.

    This is deliberately conservative.
    """

    if status != "AVAILABLE":
        return "VALID"

    if value is None:
        return "INVALID"

    return "VALID"


# ============================================================
# NETWORK METRIC
# ============================================================

def normalize_network_metric(
    route,
):
    metric = route["network_metric"]

    status = normalize_status(
        metric["status"]
    )

    confidence = normalize_confidence(
        metric.get("confidence")
    )

    validation = determine_validation(
        metric.get("value"),
        status,
    )

    return build_intelligence_evidence(
        metric=metric["name"],
        value=metric.get("value"),
        unit=metric.get("unit"),
        source=metric.get("source"),
        timestamp=datetime.now(
            timezone.utc
        ).isoformat(),
        status=status,
        confidence=confidence,
        validation=validation,
    )


# ============================================================
# COST
# ============================================================

def normalize_cost(route):

    cost = route["cost"]

    status = normalize_status(
        cost["status"]
    )

    confidence = normalize_confidence(
        cost.get("confidence")
    )

    validation = determine_validation(
        cost.get("value"),
        status,
    )

    return build_intelligence_evidence(
        metric="network_cost",
        value=cost.get("value"),
        unit=cost.get("currency"),
        source=cost.get("source"),
        timestamp=datetime.now(
            timezone.utc
        ).isoformat(),
        status=status,
        confidence=confidence,
        validation=validation,
    )


# ============================================================
# MARKET PRICE
# ============================================================

def normalize_market(route):

    if "market" not in route:
        return None

    market = route["market"]

    status = normalize_status(
        market["status"]
    )

    confidence = normalize_confidence(
        market.get("confidence")
    )

    validation = determine_validation(
        market.get("price_usd"),
        status,
    )

    return build_intelligence_evidence(
        metric="asset_price",
        value=market.get("price_usd"),
        unit="USD",
        source=market.get("source"),
        timestamp=datetime.now(
            timezone.utc
        ).isoformat(),
        status=status,
        confidence=confidence,
        validation=validation,
    )


# ============================================================
# SETTLEMENT TIME
# ============================================================

def normalize_settlement_time(route):

    settlement = route["settlement_time"]

    status = normalize_status(
        settlement["status"]
    )

    confidence = normalize_confidence(
        settlement.get("confidence")
    )

    validation = determine_validation(
        settlement.get("value"),
        status,
    )

    return build_intelligence_evidence(
        metric="settlement_time",
        value=settlement.get("value"),
        unit=settlement.get("unit"),
        source=settlement.get("source"),
        timestamp=datetime.now(
            timezone.utc
        ).isoformat(),
        status=status,
        confidence=confidence,
        validation=validation,
    )


# ============================================================
# ROUTE NORMALIZATION
# ============================================================

def normalize_route(route_id, route):

    evidence = []

    evidence.append(
        normalize_network_metric(route)
    )

    evidence.append(
        normalize_cost(route)
    )

    market = normalize_market(route)

    if market is not None:
        evidence.append(market)

    evidence.append(
        normalize_settlement_time(route)
    )

    return build_route_intelligence_contract(
        route_id=route_id,
        asset=route["asset"],
        network=route["network"],
        evidence=evidence,
    )


# ============================================================
# COMPLETE NORMALIZATION
# ============================================================

def normalize_route_intelligence(
    route_intelligence,
    request_id="unknown",
):
    """
    Convert existing route intelligence into the new
    NormalizedIntelligence contract.
    """

    routes = {}

    for route_id, route in route_intelligence.items():

        routes[route_id] = normalize_route(
            route_id,
            route,
        )

    return build_normalized_intelligence(
        request_id=request_id,
        generated_at=datetime.now(
            timezone.utc
        ).isoformat(),
        routes=routes,
    )


# ============================================================
# LIVE DEMO
# ============================================================

if __name__ == "__main__":

    from route_intelligence import (
        build_route_intelligence,
    )

    existing_intelligence = (
        build_route_intelligence()
    )

    normalized = normalize_route_intelligence(
        existing_intelligence,
        request_id="phase-b-test",
    )

    print("=== NORMALIZED INTELLIGENCE ===")

    for route_id, route in normalized["routes"].items():

        print()
        print(f"Route: {route_id}")
        print(f"Asset: {route['asset']}")
        print(f"Network: {route['network']}")

        for evidence in route["evidence"]:

            print()
            print(
                f"Metric: "
                f"{evidence['metric']}"
            )

            print(
                f"Value: "
                f"{evidence['value']}"
            )

            print(
                f"Unit: "
                f"{evidence['unit']}"
            )

            print(
                f"Source: "
                f"{evidence['source']}"
            )

            print(
                f"Status: "
                f"{evidence['status']}"
            )

            print(
                f"Confidence: "
                f"{evidence['confidence']}"
            )

            print(
                f"Validation: "
                f"{evidence['validation']}"
            )
