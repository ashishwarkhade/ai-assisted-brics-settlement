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

    print(
        f"Reason: "
        f"{economic_reason}"
    )


# ============================================================
# NORMALIZED ROUTE INPUT
# ============================================================

normalized_routes = get_normalized_routes()


# ============================================================
# POLICY INTELLIGENCE
# ============================================================

policy_intelligence = build_policy_intelligence()


# ============================================================
# BUILD ROUTE DECISIONS
# ============================================================

decisions = []


for route_key, route in normalized_routes.items():

    network = route["network"]

    policy = policy_intelligence.get(network)


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

    compliance = policy["compliance"]["value"]

    if compliance == "BLOCKED":

        decisions.append({
            "route": route,
            "status": "REJECTED",
            "reason": "COMPLIANCE_BLOCKED",
        })

        continue


    # --------------------------------------------------------
    # Geopolitical
    # --------------------------------------------------------

    geopolitical_status = (
        policy["geopolitical_status"]["value"]
    )

    if geopolitical_status == "UNKNOWN":

        decisions.append({
            "route": route,
            "status": "INVALID",
            "reason": "GEOPOLITICAL_STATUS_UNKNOWN",
        })

        continue


    if geopolitical_status != "PERMITTED":

        decisions.append({
            "route": route,
            "status": "REJECTED",
            "reason": "GEOPOLITICAL_RESTRICTION",
        })

        continue


    # --------------------------------------------------------
    # Risk
    # --------------------------------------------------------

    risk = policy["risk"]["value"]

    if risk > MAX_RISK:

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
        "real economic data."
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
        "NO_ROUTE_HAS_SUFFICIENT_REAL_COST_DATA"
    )

else:

    recommended = sorted(
        rankable_routes,
        key=lambda route: route["cost"]["value"]
    )[0]

    print(
        f"{recommended['route']} | "
        f"{recommended['asset']} / "
        f"{recommended['network']}"
    )


# ============================================================
# DATA PROVENANCE
# ============================================================

print()
print("=== DATA PROVENANCE ===")

print("Economic input: REAL")

print(
    f"Economic source: "
    f"{economic['source']}"
)

print("Route network data: REAL")

print("Route risk: TEST_DATA")
print("Compliance: TEST_RULE")
print("Geopolitical: TEST_RULE")