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


# ============================================================
# ECONOMIC GATE
# ============================================================

if network_cost_usd > transaction_value_usd:

    economic_status = "REJECTED"
    economic_reason = "NETWORK_COST_EXCEEDS_VALUE"

else:

    economic_status = "PASSED"
    economic_reason = None


print()
print("=== ECONOMIC GATE ===")
print(f"Status: {economic_status}")

if economic_reason:
    print(f"Reason: {economic_reason}")


# ============================================================
# NORMALIZED ROUTE INPUT
# ============================================================

normalized_routes = get_normalized_routes()


# ============================================================
# POLICY INTELLIGENCE
# ============================================================

policies = build_policy_intelligence()


# ============================================================
# BUILD ROUTE DECISIONS
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
        })

        continue


    if compliance["value"] != "ALLOWED":

        decisions.append({
            "route": route,
            "status": "ELIGIBLE_DATA_INCOMPLETE",
            "reason": "COMPLIANCE_REQUIRES_JURISDICTION_REVIEW",
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
        })

        continue


    if geopolitical["value"] != "PERMITTED":

        decisions.append({
            "route": route,
            "status": "ELIGIBLE_DATA_INCOMPLETE",
            "reason": "GEOPOLITICAL_STATUS_NOT_ESTABLISHED",
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
        })

        continue


    if risk["value"] > MAX_RISK:

        decisions.append({
            "route": route,
            "status": "REJECTED",
            "reason": "RISK_LIMIT_EXCEEDED",
        })

        continue


    # --------------------------------------------------------
    # Economic route cost
    # --------------------------------------------------------

    cost = route["cost"]

    if cost["status"] in (
        "NOT_CALCULATED",
        "UNKNOWN",
    ):

        decisions.append({
            "route": route,
            "status": "ELIGIBLE_DATA_INCOMPLETE",
            "reason": "ROUTE_COST_UNKNOWN",
        })

        continue


    if cost["value"] is None:

        decisions.append({
            "route": route,
            "status": "ELIGIBLE_DATA_INCOMPLETE",
            "reason": "ROUTE_COST_UNKNOWN",
        })

        continue


    # --------------------------------------------------------
    # Fully eligible
    # --------------------------------------------------------

    decisions.append({
        "route": route,
        "status": "ELIGIBLE",
        "reason": None,
    })


# ============================================================
# DISPLAY DECISIONS
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


# ============================================================
# ECONOMICALLY RANKABLE ROUTES
# ============================================================

rankable_routes = [

    decision["route"]

    for decision in decisions

    if decision["status"] == "ELIGIBLE"

    and decision["route"]["cost"]["value"] is not None
]


print()
print("=== ROUTE RANKING ===")


if not rankable_routes:

    print(
        "No route has sufficient "
        "policy and economic data."
    )

else:

    ranked_routes = sorted(
        rankable_routes,
        key=lambda route: route["cost"]["value"]
    )

    for route in ranked_routes:

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


if not rankable_routes:

    print("NO_RECOMMENDATION")
    print(
        "Reason: "
        "NO_ROUTE_HAS_SUFFICIENT_POLICY_AND_COST_DATA"
    )

else:

    best_route = min(
        rankable_routes,
        key=lambda route: route["cost"]["value"]
    )

    print(
        f"{best_route['route']} | "
        f"{best_route['asset']} / "
        f"{best_route['network']}"
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

print(
    "Route risk: "
    "TEST"
)

print(
    "Compliance: "
    "REFERENCE"
)

print(
    "Geopolitical: "
    "REFERENCE"
)