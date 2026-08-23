import json


# ============================================================
# CONFIGURATION
# ============================================================

REPORT_FILE = "audit/settlement_report_8_12.json"


# ============================================================
# AI AUTHORITY
# ============================================================

AI_AUTHORITY = "EXPLANATION_ONLY"


# ============================================================
# LOAD REPORT
# ============================================================

def load_settlement_report():

    with open(REPORT_FILE, "r") as file:

        return json.load(file)


# ============================================================
# BUILD CONTROLLED AI CONTEXT
# ============================================================

def build_ai_decision_context(report):

    economic = report.get(
        "economic",
        {}
    )

    economic_gate = report.get(
        "economic_gate",
        {}
    )

    route_decisions = report.get(
        "route_decisions",
        []
    )

    provenance = report.get(
        "provenance",
        {}
    )

    # --------------------------------------------------------
    # Route information
    # --------------------------------------------------------

    routes = []

    for decision in route_decisions:

        route = {
            "route": decision.get("route"),
            "asset": decision.get("asset"),
            "network": decision.get("network"),
            "status": decision.get("status"),
            "reason": decision.get("reason"),
        }

        evidence = decision.get(
            "evidence"
        )

        if evidence:

            route["evidence"] = {
                "value": evidence.get("value"),
                "source": evidence.get("source"),
                "source_type":
                    evidence.get("source_type"),
                "confidence":
                    evidence.get("confidence"),
            }

        explanation = decision.get(
            "explanation"
        )

        if explanation:

            cost = explanation.get(
                "cost"
            )

            if cost:

                route["cost"] = {
                    "value": cost.get("value"),
                    "currency": cost.get("currency"),
                    "status": cost.get("status"),
                    "source": cost.get("source"),
                    "confidence":
                        cost.get("confidence"),
                }

        routes.append(route)

    # --------------------------------------------------------
    # Controlled context
    # --------------------------------------------------------

    context = {

        "context_version": "8.14",

        "ai_authority": AI_AUTHORITY,

        "instruction": (
            "Explain the deterministic settlement "
            "decision. Do not create, modify, or "
            "override a settlement recommendation."
        ),

        "economic": {
            "transaction_value_usd":
                economic.get(
                    "transaction_value_usd"
                ),
            "network_cost_usd":
                economic.get(
                    "network_cost_usd"
                ),
            "status":
                economic.get("status"),
            "source":
                economic.get("source"),
            "confidence":
                economic.get("confidence"),
        },

        "economic_gate": {
            "status":
                economic_gate.get("status"),
            "reason":
                economic_gate.get("reason"),
        },

        "routes": routes,

        "route_ranking":
            report.get(
                "route_ranking",
                []
            ),

        "recommendation":
            report.get(
                "recommendation"
            ),

        "recommendation_reason":
            report.get(
                "recommendation_reason"
            ),

        "provenance": provenance,

        "ai_constraints": [

            "Do not select a route.",

            "Do not override NO_RECOMMENDATION.",

            "Do not modify compliance status.",

            "Do not modify geopolitical status.",

            "Do not modify risk values.",

            "Do not invent missing evidence.",

            "Do not invent costs.",

            "Clearly identify incomplete data.",

            "Explain the deterministic result only.",
        ],
    }

    return context


# ============================================================
# DISPLAY CONTROLLED CONTEXT
# ============================================================

def print_ai_decision_context(context):

    print(
        "=== CONTROLLED AI DECISION CONTEXT ==="
    )

    print()

    print(
        f"Context version: "
        f"{context['context_version']}"
    )

    print(
        f"AI authority: "
        f"{context['ai_authority']}"
    )

    print()

    print("Instruction")
    print("-" * 60)

    print(
        context["instruction"]
    )

    print()

    print("Deterministic recommendation")
    print("-" * 60)

    recommendation = context.get(
        "recommendation"
    )

    if recommendation:

        print(recommendation)

    else:

        print("NO_RECOMMENDATION")

    print()

    print("Recommendation reason")
    print("-" * 60)

    print(
        context.get(
            "recommendation_reason"
        )
    )

    print()

    print("AI constraints")
    print("-" * 60)

    for constraint in context[
        "ai_constraints"
    ]:

        print(
            f"- {constraint}"
        )

    print()

    print("Routes")
    print("=" * 60)

    for route in context["routes"]:

        print(
            f"{route['route']} | "
            f"{route['asset']} / "
            f"{route['network']}"
        )

        print(
            f"  Status: "
            f"{route['status']}"
        )

        print(
            f"  Reason: "
            f"{route['reason']}"
        )

        evidence = route.get(
            "evidence"
        )

        if evidence:

            print(
                f"  Evidence source: "
                f"{evidence['source']}"
            )

            print(
                f"  Evidence confidence: "
                f"{evidence['confidence']}"
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    report = load_settlement_report()

    context = build_ai_decision_context(
        report
    )

    print_ai_decision_context(
        context
    )

    print()
    print("Status: READY")
