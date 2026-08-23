from normalized_routes import get_normalized_routes
from policy_intelligence import build_policy_intelligence
from economic_intelligence import build_economic_intelligence


# ============================================================
# DECISION POLICY
# ============================================================

MAX_RISK = 50


# ============================================================
# BUILD AUDIT RECORD
# ============================================================

def build_settlement_audit():

    # --------------------------------------------------------
    # Economic input
    # --------------------------------------------------------

    economic = build_economic_intelligence()

    transaction_value_usd = economic["transaction_value_usd"]
    network_cost_usd = economic["network_cost_usd"]

    if network_cost_usd > transaction_value_usd:

        economic_status = "REJECTED"
        economic_reason = "NETWORK_COST_EXCEEDS_VALUE"

    else:

        economic_status = "PASSED"
        economic_reason = None


    # --------------------------------------------------------
    # Route + policy input
    # --------------------------------------------------------

    normalized_routes = get_normalized_routes()
    policies = build_policy_intelligence()

    decisions = []


    # ========================================================
    # ROUTE DECISION ENGINE
    # ========================================================

    for route_key, route in normalized_routes.items():

        network = route["network"]

        policy = policies.get(network)


        # ----------------------------------------------------
        # Missing policy
        # ----------------------------------------------------

        if policy is None:

            decisions.append({
                "route": route["route"],
                "asset": route["asset"],
                "network": network,
                "status": "INVALID",
                "reason": "MISSING_ROUTE_POLICY",
                "evidence": None,
            })

            continue


        # ----------------------------------------------------
        # Compliance
        # ----------------------------------------------------

        compliance = policy["compliance"]

        if compliance["value"] == "BLOCKED":

            decisions.append({
                "route": route["route"],
                "asset": route["asset"],
                "network": network,
                "status": "REJECTED",
                "reason": "COMPLIANCE_BLOCKED",
                "evidence": compliance,
            })

            continue


        if compliance["value"] != "ALLOWED":

            decisions.append({
                "route": route["route"],
                "asset": route["asset"],
                "network": network,
                "status": "ELIGIBLE_DATA_INCOMPLETE",
                "reason": (
                    "COMPLIANCE_REQUIRES_JURISDICTION_REVIEW"
                ),
                "evidence": compliance,
            })

            continue


        # ----------------------------------------------------
        # Geopolitical
        # ----------------------------------------------------

        geopolitical = policy["geopolitical_status"]

        if geopolitical["value"] == "RESTRICTED":

            decisions.append({
                "route": route["route"],
                "asset": route["asset"],
                "network": network,
                "status": "REJECTED",
                "reason": "GEOPOLITICAL_RESTRICTION",
                "evidence": geopolitical,
            })

            continue


        if geopolitical["value"] != "PERMITTED":

            decisions.append({
                "route": route["route"],
                "asset": route["asset"],
                "network": network,
                "status": "ELIGIBLE_DATA_INCOMPLETE",
                "reason": (
                    "GEOPOLITICAL_STATUS_NOT_ESTABLISHED"
                ),
                "evidence": geopolitical,
            })

            continue


        # ----------------------------------------------------
        # Risk
        # ----------------------------------------------------

        risk = policy["risk"]

        if risk["value"] is None:

            decisions.append({
                "route": route["route"],
                "asset": route["asset"],
                "network": network,
                "status": "ELIGIBLE_DATA_INCOMPLETE",
                "reason": "RISK_UNKNOWN",
                "evidence": risk,
            })

            continue


        if risk["value"] > MAX_RISK:

            decisions.append({
                "route": route["route"],
                "asset": route["asset"],
                "network": network,
                "status": "REJECTED",
                "reason": "RISK_LIMIT_EXCEEDED",
                "evidence": risk,
            })

            continue


        # ----------------------------------------------------
        # Route cost
        # ----------------------------------------------------

        cost = route["cost"]

        if cost["value"] is None:

            decisions.append({
                "route": route["route"],
                "asset": route["asset"],
                "network": network,
                "status": "ELIGIBLE_DATA_INCOMPLETE",
                "reason": "ROUTE_COST_UNKNOWN",
                "evidence": cost,
            })

            continue


        if cost["status"] in (
            "NOT_CALCULATED",
            "UNKNOWN",
        ):

            decisions.append({
                "route": route["route"],
                "asset": route["asset"],
                "network": network,
                "status": "ELIGIBLE_DATA_INCOMPLETE",
                "reason": "ROUTE_COST_UNKNOWN",
                "evidence": cost,
            })

            continue


        # ----------------------------------------------------
        # Fully eligible
        # ----------------------------------------------------

        confidence = min(
            cost["confidence"],
            risk["confidence"],
            compliance["confidence"],
            geopolitical["confidence"],
        )

        decisions.append({
            "route": route["route"],
            "asset": route["asset"],
            "network": network,
            "status": "ELIGIBLE",
            "reason": None,
            "evidence": {
                "source": "COMBINED_ROUTE_AND_POLICY_DATA",
                "type": "REAL_AND_REFERENCE",
                "confidence": confidence,
            },
        })


    # ========================================================
    # ROUTE RANKING
    # ========================================================

    rankable_routes = [

        decision

        for decision in decisions

        if decision["status"] == "ELIGIBLE"

        and decision["route"] is not None
    ]


    ranked_routes = sorted(
        rankable_routes,
        key=lambda decision: next(
            route["cost"]["value"]
            for route in normalized_routes.values()
            if route["route"] == decision["route"]
        )
    )


    # ========================================================
    # RECOMMENDATION
    # ========================================================

    if economic_status != "PASSED":

        recommendation = None

        recommendation_reason = economic_reason

    elif not ranked_routes:

        recommendation = None

        recommendation_reason = (
            "NO_ROUTE_HAS_SUFFICIENT_POLICY_AND_COST_DATA"
        )

    else:

        best = ranked_routes[0]

        recommendation = {
            "route": best["route"],
            "asset": best["asset"],
            "network": best["network"],
        }

        recommendation_reason = None


    # ========================================================
    # AUDIT RECORD
    # ========================================================

    audit_record = {

        "economic": {
            "transaction_value_usd": transaction_value_usd,
            "network_cost_usd": network_cost_usd,
            "status": economic["status"],
            "source": economic["source"],
            "confidence": economic["confidence"],
        },

        "economic_gate": {
            "status": economic_status,
            "reason": economic_reason,
        },

        "route_decisions": decisions,

        "route_ranking": [
            {
                "route": decision["route"],
                "asset": decision["asset"],
                "network": decision["network"],
            }
            for decision in ranked_routes
        ],

        "recommendation": recommendation,

        "recommendation_reason": recommendation_reason,

        "provenance": {
            "economic_input": economic["status"],
            "economic_source": economic["source"],
            "route_network_data": "REAL",
            "route_risk": "TEST",
            "compliance": "REFERENCE",
            "geopolitical": "REFERENCE",
        },
    }

    return audit_record


# ============================================================
# DISPLAY AUDIT RECORD
# ============================================================

if __name__ == "__main__":

    audit = build_settlement_audit()

    economic = audit["economic"]

    print("=== REAL ECONOMIC INPUT ===")

    print(
        f"Transaction value: "
        f"${economic['transaction_value_usd']:.2f}"
    )

    print(
        f"Network cost: "
        f"${economic['network_cost_usd']:.6f}"
    )

    print(
        f"Source: "
        f"{economic['source']}"
    )

    print(
        f"Confidence: "
        f"{economic['confidence']}"
    )


    # --------------------------------------------------------
    # Economic gate
    # --------------------------------------------------------

    gate = audit["economic_gate"]

    print()
    print("=== ECONOMIC GATE ===")

    print(
        f"Status: "
        f"{gate['status']}"
    )

    if gate["reason"]:

        print(
            f"Reason: "
            f"{gate['reason']}"
        )


    # --------------------------------------------------------
    # Decisions
    # --------------------------------------------------------

    print()
    print("=== SETTLEMENT DECISION ===")

    print()
    print("Route decisions:")

    for decision in audit["route_decisions"]:

        print(
            f"{decision['route']} | "
            f"{decision['status']}"
        )

        if decision["reason"]:

            print(
                f"  Reason: "
                f"{decision['reason']}"
            )

        evidence = decision["evidence"]

        if evidence:

            print(
                f"  Evidence source: "
                f"{evidence.get('source', 'UNKNOWN')}"
            )

            print(
                f"  Evidence type: "
                f"{evidence.get('source_type', evidence.get('type', 'UNKNOWN'))}"
            )

            print(
                f"  Evidence confidence: "
                f"{evidence.get('confidence', 0.0)}"
            )


    # --------------------------------------------------------
    # Ranking
    # --------------------------------------------------------

    print()
    print("=== ROUTE RANKING ===")

    if not audit["route_ranking"]:

        print(
            "No route has sufficient "
            "policy and economic data."
        )

    else:

        for ranked in audit["route_ranking"]:

            route_name = ranked["route"]

            route = next(
                route
                for route in get_normalized_routes().values()
                if route["route"] == route_name
            )

            print(
                f"{ranked['route']} | "
                f"{ranked['asset']} / "
                f"{ranked['network']} | "
                f"${route['cost']['value']:.6f}"
            )


    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    print()
    print("=== RECOMMENDATION ===")

    if audit["recommendation"] is None:

        print("NO_RECOMMENDATION")

        print(
            f"Reason: "
            f"{audit['recommendation_reason']}"
        )

    else:

        recommendation = audit["recommendation"]

        print(
            f"{recommendation['route']} | "
            f"{recommendation['asset']} / "
            f"{recommendation['network']}"
        )


    # --------------------------------------------------------
    # Provenance
    # --------------------------------------------------------

    print()
    print("=== DATA PROVENANCE ===")

    provenance = audit["provenance"]

    print(
        f"Economic input: "
        f"{provenance['economic_input']}"
    )

    print(
        f"Economic source: "
        f"{provenance['economic_source']}"
    )

    print(
        f"Route network data: "
        f"{provenance['route_network_data']}"
    )

    print(
        f"Route risk: "
        f"{provenance['route_risk']}"
    )

    print(
        f"Compliance: "
        f"{provenance['compliance']}"
    )

    print(
        f"Geopolitical: "
        f"{provenance['geopolitical']}"
    )