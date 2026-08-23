import json
from datetime import datetime, timezone

from normalized_routes import get_normalized_routes
from policy_intelligence import build_policy_intelligence
from economic_intelligence import build_economic_intelligence
from decision_explanation import build_decision_explanation


# ============================================================
# DECISION POLICY
# ============================================================

MAX_RISK = 50

AUDIT_FILE = "audit/settlement_audit.json"


# ============================================================
# BUILD SETTLEMENT AUDIT
# ============================================================

def build_settlement_audit(
    economic,
    economic_status,
    economic_reason,
    decisions,
    ranked_routes,
    recommendation,
    recommendation_reason,
):

    route_decisions = []

    for decision in decisions:

        route = decision["route"]

        item = {
            "route": route["route"],
            "asset": route["asset"],
            "network": route["network"],
            "status": decision["status"],
            "reason": decision["reason"],
        }

        if "evidence" in decision:

            evidence = decision["evidence"]

            item["evidence"] = {
                "value": evidence["value"],
                "source": evidence["source"],
                "source_type": evidence["source_type"],
                "confidence": evidence["confidence"],
            }

        if "explanation" in decision:

            item["explanation"] = decision["explanation"]

        route_decisions.append(item)

    route_ranking = []

    for route in ranked_routes:

        route_ranking.append({
            "route": route["route"],
            "asset": route["asset"],
            "network": route["network"],
            "cost_usd": route["cost"]["value"],
        })

    audit = {
        "audit_version": "8.7",

        "generated_at_utc":
            datetime.now(timezone.utc).isoformat(),

        "economic": {
            "transaction_value_usd":
                economic["transaction_value_usd"],

            "network_cost_usd":
                economic["network_cost_usd"],

            "status":
                economic["status"],

            "source":
                economic["source"],

            "confidence":
                economic["confidence"],
        },

        "economic_gate": {
            "status":
                economic_status,

            "reason":
                economic_reason,
        },

        "route_decisions":
            route_decisions,

        "route_ranking":
            route_ranking,

        "recommendation":
            recommendation,

        "recommendation_reason":
            recommendation_reason,

        "provenance": {
            "economic_input":
                economic["status"],

            "economic_source":
                economic["source"],

            "route_network_data":
                "REAL",

            "route_risk":
                "TEST",

            "compliance":
                "REFERENCE",

            "geopolitical":
                "REFERENCE",
        },
    }

    return audit


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

    economic_reason = (
        "NETWORK_COST_EXCEEDS_VALUE"
    )

else:

    economic_status = "PASSED"

    economic_reason = None


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

            "evidence": compliance,
        })

        continue


    if compliance["value"] != "ALLOWED":

        decisions.append({
            "route": route,

            "status":
                "ELIGIBLE_DATA_INCOMPLETE",

            "reason":
                "COMPLIANCE_REQUIRES_JURISDICTION_REVIEW",

            "evidence":
                compliance,
        })

        continue


    # --------------------------------------------------------
    # Geopolitical
    # --------------------------------------------------------

    geopolitical = policy[
        "geopolitical_status"
    ]


    if geopolitical["value"] == "RESTRICTED":

        decisions.append({
            "route": route,
            "status": "REJECTED",
            "reason": "GEOPOLITICAL_RESTRICTION",

            "evidence":
                geopolitical,
        })

        continue


    if geopolitical["value"] != "PERMITTED":

        decisions.append({
            "route": route,

            "status":
                "ELIGIBLE_DATA_INCOMPLETE",

            "reason":
                "GEOPOLITICAL_STATUS_NOT_ESTABLISHED",

            "evidence":
                geopolitical,
        })

        continue


    # --------------------------------------------------------
    # Risk
    # --------------------------------------------------------

    risk = policy["risk"]


    if risk["value"] is None:

        decisions.append({
            "route": route,

            "status":
                "ELIGIBLE_DATA_INCOMPLETE",

            "reason":
                "RISK_UNKNOWN",

            "evidence":
                risk,
        })

        continue


    if risk["value"] > MAX_RISK:

        decisions.append({
            "route": route,

            "status":
                "REJECTED",

            "reason":
                "RISK_LIMIT_EXCEEDED",

            "evidence":
                risk,
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

            "status":
                "ELIGIBLE_DATA_INCOMPLETE",

            "reason":
                "ROUTE_COST_UNKNOWN",

            "evidence":
                cost,
        })

        continue


    if cost["value"] is None:

        decisions.append({
            "route": route,

            "status":
                "ELIGIBLE_DATA_INCOMPLETE",

            "reason":
                "ROUTE_COST_UNKNOWN",

            "evidence":
                cost,
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
# DECISION EXPLANATIONS
# ============================================================

for decision in decisions:

    decision["explanation"] = (
        build_decision_explanation(
            decision
        )
    )


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

    if "evidence" in decision:

        evidence = decision["evidence"]

        print(
            f"  Evidence source: "
            f"{evidence['source']}"
        )

        print(
            f"  Evidence type: "
            f"{evidence['source_type']}"
        )

        print(
            f"  Evidence confidence: "
            f"{evidence['confidence']}"
        )


# ============================================================
# ECONOMICALLY RANKABLE ROUTES
# ============================================================

rankable_routes = [

    decision["route"]

    for decision in decisions

    if decision["status"] == "ELIGIBLE"

    and decision["route"]["cost"]["value"]
    is not None
]


print()
print("=== ROUTE RANKING ===")


if not rankable_routes:

    print(
        "No route has sufficient "
        "policy and economic data."
    )

    ranked_routes = []

else:

    ranked_routes = sorted(
        rankable_routes,
        key=lambda route:
            route["cost"]["value"]
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

    recommendation = None

    recommendation_reason = (
        "NO_ROUTE_HAS_SUFFICIENT_POLICY_AND_COST_DATA"
    )

    print(
        "NO_RECOMMENDATION"
    )

    print(
        f"Reason: "
        f"{recommendation_reason}"
    )

else:

    best_route = min(
        rankable_routes,
        key=lambda route:
            route["cost"]["value"]
    )

    recommendation = {
        "route":
            best_route["route"],

        "asset":
            best_route["asset"],

        "network":
            best_route["network"],
    }

    recommendation_reason = None

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

print(
    "Route network data: "
    "REAL"
)

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


# ============================================================
# BUILD AUDIT RECORD
# ============================================================

audit = build_settlement_audit(
    economic=economic,

    economic_status=
        economic_status,

    economic_reason=
        economic_reason,

    decisions=
        decisions,

    ranked_routes=
        ranked_routes,

    recommendation=
        recommendation,

    recommendation_reason=
        recommendation_reason,
)


# ============================================================
# WRITE AUDIT FILE
# ============================================================

with open(
    AUDIT_FILE,
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        audit,
        file,
        indent=4,
    )


print()
print("=== AUDIT ===")

print(
    f"Audit file: "
    f"{AUDIT_FILE}"
)

print(
    "Audit version: "
    "8.7"
)

print(
    "Status: "
    "WRITTEN"
)