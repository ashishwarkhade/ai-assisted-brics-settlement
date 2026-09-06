from data_provenance import add_provenance


# ============================================================
# ROUTE RISK MODEL
# ============================================================

MAX_ROUTE_RISK = 50


def _risk_evidence(
    value,
    source,
    source_type,
    confidence,
):
    return add_provenance(
        value,
        source,
        source_type,
        confidence,
    )


def calculate_route_risk(route):
    """
    Deterministically calculate route risk from the
    normalized route intelligence.

    This model does NOT evaluate:
        - regulatory status
        - compliance
        - geopolitical status

    Those remain separate decision gates.

    Risk range:
        0   = lowest observed risk
        100 = highest observed risk
    """

    if not isinstance(route, dict):
        raise ValueError(
            "route must be a dictionary"
        )

    score = 0
    components = {}

    # --------------------------------------------------------
    # Network data
    # --------------------------------------------------------

    network_metric = route.get(
        "network_metric"
    )

    if not isinstance(
        network_metric,
        dict,
    ):

        raise ValueError(
            "route.network_metric is required"
        )

    if (
        network_metric.get("status")
        != "REAL"
    ):

        components["network"] = (
            _risk_evidence(
                30,
                "ROUTE_NETWORK_DATA",
                "UNKNOWN",
                0.0,
            )
        )

        score += 30

    else:

        components["network"] = (
            _risk_evidence(
                10,
                network_metric.get(
                    "source",
                    "UNKNOWN",
                ),
                "REAL",
                network_metric.get(
                    "confidence",
                    0.0,
                ),
            )
        )

        score += 10

    # --------------------------------------------------------
    # Cost data
    # --------------------------------------------------------

    cost = route.get("cost")

    if not isinstance(cost, dict):

        raise ValueError(
            "route.cost is required"
        )

    cost_status = cost.get(
        "status"
    )

    if cost_status in (
        "NOT_CALCULATED",
        "UNKNOWN",
    ) or cost.get("value") is None:

        components["cost_data"] = (
            _risk_evidence(
                25,
                cost.get(
                    "source",
                    "UNKNOWN",
                ),
                "UNKNOWN",
                cost.get(
                    "confidence",
                    0.0,
                ),
            )
        )

        score += 25

    else:

        components["cost_data"] = (
            _risk_evidence(
                5,
                cost.get(
                    "source",
                    "UNKNOWN",
                ),
                "REAL",
                cost.get(
                    "confidence",
                    0.0,
                ),
            )
        )

        score += 5

    # --------------------------------------------------------
    # Settlement-time data
    # --------------------------------------------------------

    settlement_time = route.get(
        "settlement_time"
    )

    if (
        not isinstance(
            settlement_time,
            dict,
        )
        or settlement_time.get("value")
        is None
        or settlement_time.get("status")
        != "REAL"
    ):

        components["settlement_time"] = (
            _risk_evidence(
                20,
                "SETTLEMENT_TIME",
                "UNKNOWN",
                0.0,
            )
        )

        score += 20

    else:

        components["settlement_time"] = (
            _risk_evidence(
                5,
                settlement_time.get(
                    "source",
                    "UNKNOWN",
                ),
                "REAL",
                settlement_time.get(
                    "confidence",
                    0.0,
                ),
            )
        )

        score += 5

    # --------------------------------------------------------
    # Market data
    # --------------------------------------------------------

    market = route.get("market")

    if market is None:

        components["market_data"] = (
            _risk_evidence(
                15,
                "MARKET_DATA",
                "UNKNOWN",
                0.0,
            )
        )

        score += 15

    elif (
        market.get("price_usd") is None
        or market.get("status")
        != "REAL"
    ):

        components["market_data"] = (
            _risk_evidence(
                15,
                market.get(
                    "source",
                    "UNKNOWN",
                ),
                "UNKNOWN",
                market.get(
                    "confidence",
                    0.0,
                ),
            )
        )

        score += 15

    else:

        components["market_data"] = (
            _risk_evidence(
                5,
                market.get(
                    "source",
                    "UNKNOWN",
                ),
                "REAL",
                market.get(
                    "confidence",
                    0.0,
                ),
            )
        )

        score += 5

    # --------------------------------------------------------
    # Normalize
    # --------------------------------------------------------

    score = min(
        score,
        100,
    )

    return {
        "value": score,

        "source":
            "DETERMINISTIC_ROUTE_RISK_MODEL",

        "source_type":
            "CALCULATED",

        "confidence":
            1.0,

        "components":
            components,
    }


# ============================================================
# BUILD ALL ROUTE RISKS
# ============================================================

def build_route_risk_model(
    normalized_routes,
):

    if not isinstance(
        normalized_routes,
        dict,
    ):

        raise ValueError(
            "normalized_routes must be a dictionary"
        )

    risks = {}

    for route_key, route in (
        normalized_routes.items()
    ):

        risks[route_key] = (
            calculate_route_risk(route)
        )

    return risks


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    from normalized_routes import (
        get_normalized_routes,
    )

    routes = get_normalized_routes()

    risks = build_route_risk_model(
        routes
    )

    print(
        "=== ROUTE RISK MODEL ==="
    )

    for route_key, risk in risks.items():

        print()
        print(
            f"Route: {route_key}"
        )

        print(
            f"Risk score: "
            f"{risk['value']}"
        )

        print(
            f"Source: "
            f"{risk['source']}"
        )

        print(
            f"Confidence: "
            f"{risk['confidence']}"
        )

        print()
        print("Components:")

        for name, component in (
            risk["components"].items()
        ):

            print(
                f"  {name}: "
                f"{component['value']}"
            )
