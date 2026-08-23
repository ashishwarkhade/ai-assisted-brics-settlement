from normalized_routes import get_normalized_routes
from policy_intelligence import build_policy_intelligence
from economic_intelligence import build_economic_intelligence


# ============================================================
# DECISION POLICY
# ============================================================

MAX_RISK = 50


# ============================================================
# REAL ECONOMIC INPUT
# ============================================================

economic = build_economic_intelligence()

transaction_value_usd = economic["transaction_value_usd"]
network_cost_usd = economic["network_cost_usd"]


# ============================================================
# ECONOMIC GATE
# ============================================================

if network_cost_usd > transaction_value_usd:

    economic_status = "REJECTED"
    economic_reason = "NETWORK_COST_EXCEEDS_VALUE"

else:

    economic_status = "PASSED"
    economic_reason = None


# ============================================================
# ROUTE + POLICY INPUT
# ============================================================

normalized_routes = get_normalized_routes()
policies = build_policy_intelligence()


# ============================================================
# DECISION ENGINE
# ============================================================

decisions = []


for route_key, route in normalized_routes.items():

    network = route["network"]
    policy = policies.get(network)


    # --------------------------------------------------------
    # Missing policy
    # --------------------------------------------------------

    if policy is None:

        decisions.append({
            "route": route,
            "status": "INVALID",
            "reason": "MISSING_ROUTE_POLICY",
            "evidence": None,
        })

        continue


    # --------------------------------------------------------
    # Compliance
    # --------------------------------------------------------

    compliance = policy["compliance"]

    if compliance["value"] == "BLOCKED":

        decisions.append({
            "route": route,
            "status": "REJECTED",
            "reason": "COMPLIANCE_BLOCKED",
            "evidence": compliance,
        })

        continue


    if compliance["value"] != "ALLOWED":

        decisions.append({
            "route": route,
            "status": "ELIGIBLE_DATA_INCOMPLETE",
            "reason": "COMPLIANCE_REQUIRES_JURISDICTION_REVIEW",
            "evidence": compliance,
        })

        continue


    # --------------------------------------------------------
    # Geopolitical
    # --------------------------------------------------------

    geopolitical = policy["geopolitical_status"]

    if geopolitical["value"] == "RESTRICTED":

        decisions.append({
            "route": route,
            "status": "REJECTED",
            "reason": "GEOPOLITICAL_RESTRICTION",
            "evidence": geopolitical,
        })

        continue


    if geopolitical["value"] != "PERMITTED":

        decisions.append({
            "route": route,
            "status": "ELIGIBLE_DATA_INCOMPLETE",
            "reason": "GEOPOLITICAL_STATUS_NOT_ESTABLISHED",
            "evidence": geopolitical,
        })

        continue


    # --------------------------------------------------------
    # Risk
    # --------------------------------------------------------

    risk = policy["risk"]

    if risk["value"] is None:

        decisions.append({
            "route": route,
            "status": "ELIGIBLE_DATA_INCOMPLETE",
            "reason": "RISK_UNKNOWN",
            "evidence": risk,
        })

        continue


    if risk["value"] > MAX_RISK:

        decisions.append({
            "route": route,
            "status": "REJECTED",
            "reason": "RISK_LIMIT_EXCEEDED",
            "evidence": risk,
        })

        continue


    # --------------------------------------------------------
    # Route cost
    # --------------------------------------------------------

    cost = route["cost"]

    if cost["value"] is None:

        decisions.append({
            "route": route,
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
            "route": route,
            "status": "ELIGIBLE_DATA_INCOMPLETE",
            "reason": "ROUTE_COST_UNKNOWN",
            "evidence": cost,
        })

        continue


    # --------------------------------------------------------
    # Fully eligible
    # --------------------------------------------------------

    decisions.append({
        "route": route,
        "status": "ELIGIBLE",
        "reason": None,
        "evidence": {
            "source": "COMBINED_ROUTE_AND_POLICY_DATA",
            "type": "REAL_AND_REFERENCE",
            "confidence": min(
                cost["confidence"],
                risk["confidence"],
                compliance["confidence"],
                geopolitical["confidence"],
            ),
        },
    })


# ============================================================
# RANK ELIGIBLE ROUTES
# ============================================================

rankable_routes = [

    decision

    for decision in decisions

    if decision["status"] == "ELIGIBLE"

    and decision["route"]["cost"]["value"] is not None
]


ranked_routes = sorted(
    rankable_routes,
    key=lambda decision:
        decision["route"]["cost"]["value"]
)


# ============================================================
# RECOMMENDATION
# ============================================================

if economic_status != "PASSED":

    recommendation = None
    recommendation_reason = economic_reason

elif not ranked_routes:

    recommendation = None
    recommendation_reason = (
        "NO_ROUTE_HAS_SUFFICIENT_POLICY_AND_COST_DATA"
    )

else:

    recommendation = ranked_routes[0]["route"]
    recommendation_reason = None


# ============================================================
# DISPLAY
# ============================================================

print("=== REAL ECONOMIC INPUT ===")

print(
    f"Transaction value: "
    f"${transaction_value_usd:.2f}"
)

print(
    f"Network cost: "
    f"${network_cost_usd:.6f}"
)

print(
    f"Source: "
    f"{economic['source']}"
)

print(
    f"Confidence: "
    f"{economic['confidence']}"
)


print()
print("=== ECONOMIC GATE ===")

print(
    f"Status: "
    f"{economic_status}"
)

if economic_reason:

    print(
        f"Reason: "
        f"{economic_reason}"
    )


# ============================================================
# SETTLEMENT DECISION
# ============================================================

print()
print("=== SETTLEMENT DECISION ===")

print()
print("Route decisions:")


for decision in decisions:

    route = decision["route"]

    print(
        f"{route['route']} | "
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


# ============================================================
# ROUTE RANKING
# ============================================================

print()
print("=== ROUTE RANKING ===")


if not ranked_routes:

    print(
        "No route has sufficient "
        "policy and economic data."
    )

else:

    for decision in ranked_routes:

        route = decision["route"]

        print(
            f"{route['route']} | "
            f"{route['asset']} / "
            f"{route['network']} | "
            f"${route['cost']['value']:.6f}"
        )


# ============================================================
# RECOMMENDATION
# ============================================================

print()
print("=== RECOMMENDATION ===")


if recommendation is None:

    print("NO_RECOMMENDATION")

    print(
        f"Reason: "
        f"{recommendation_reason}"
    )

else:

    print(
        f"{recommendation['route']} | "
        f"{recommendation['asset']} / "
        f"{recommendation['network']}"
    )


# ============================================================
# DATA PROVENANCE
# ============================================================

print()
print("=== DATA PROVENANCE ===")

print(
    f"Economic input: "
    f"{economic['status']}"
)

print(
    f"Economic source: "
    f"{economic['source']}"
)

print("Route network data: REAL")

print("Route risk: TEST")

print("Compliance: REFERENCE")

print("Geopolitical: REFERENCE")