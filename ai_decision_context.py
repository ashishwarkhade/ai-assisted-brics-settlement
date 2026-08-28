import json


# ============================================================
# CONFIGURATION
# ============================================================

REPORT_FILE = "audit/settlement_report_8_12.json"

AUDIT_FILE = "audit/settlement_audit.json"


# ============================================================
# AI AUTHORITY
# ============================================================

AI_AUTHORITY = "EXPLANATION_ONLY"


# ============================================================
# LOAD REPORT
# ============================================================

def load_settlement_report():

    with open(
        REPORT_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# ============================================================
# LOAD AUDIT
# ============================================================

def load_settlement_audit():

    try:

        with open(
            AUDIT_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except (
        FileNotFoundError,
        json.JSONDecodeError,
    ):

        return {}


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
    # Telegraph intelligence
    #
    # Primary source:
    #     settlement report
    #
    # Fallback:
    #     settlement audit
    #
    # Telegraph remains an intelligence provider only.
    # It does not make settlement decisions.
    # --------------------------------------------------------

    telegraph_intelligence = report.get(
        "telegraph_intelligence"
    )

    if telegraph_intelligence is None:

        audit = load_settlement_audit()

        telegraph_intelligence = audit.get(
            "telegraph_intelligence"
        )

    # --------------------------------------------------------
    # Route information
    # --------------------------------------------------------

    routes = []

    for decision in route_decisions:

        route = {
            "route": decision.get(
                "route"
            ),

            "asset": decision.get(
                "asset"
            ),

            "network": decision.get(
                "network"
            ),

            "status": decision.get(
                "status"
            ),

            "reason": decision.get(
                "reason"
            ),
        }

        evidence = decision.get(
            "evidence"
        )

        if evidence:

            route["evidence"] = {

                "value":
                    evidence.get(
                        "value"
                    ),

                "source":
                    evidence.get(
                        "source"
                    ),

                "source_type":
                    evidence.get(
                        "source_type"
                    ),

                "confidence":
                    evidence.get(
                        "confidence"
                    ),
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

                    "value":
                        cost.get(
                            "value"
                        ),

                    "currency":
                        cost.get(
                            "currency"
                        ),

                    "status":
                        cost.get(
                            "status"
                        ),

                    "source":
                        cost.get(
                            "source"
                        ),

                    "confidence":
                        cost.get(
                            "confidence"
                        ),
                }

        routes.append(
            route
        )

    # --------------------------------------------------------
    # Controlled context
    # --------------------------------------------------------

    context = {

        "context_version":
            "10.5",

        "ai_authority":
            AI_AUTHORITY,

        "instruction": (
            "Explain the deterministic settlement "
            "decision using the supplied evidence. "
            "Do not create, modify, override, or "
            "recommend a settlement route."
        ),

        # ----------------------------------------------------
        # Economic
        # ----------------------------------------------------

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
                economic.get(
                    "status"
                ),

            "source":
                economic.get(
                    "source"
                ),

            "confidence":
                economic.get(
                    "confidence"
                ),
        },

        # ----------------------------------------------------
        # Economic gate
        # ----------------------------------------------------

        "economic_gate": {

            "status":
                economic_gate.get(
                    "status"
                ),

            "reason":
                economic_gate.get(
                    "reason"
                ),
        },

        # ----------------------------------------------------
        # Deterministic route decisions
        # ----------------------------------------------------

        "routes":
            routes,

        "route_ranking":
            report.get(
                "route_ranking",
                []
            ),

        # ----------------------------------------------------
        # Deterministic recommendation
        # ----------------------------------------------------

        "recommendation":
            report.get(
                "recommendation"
            ),

        "recommendation_reason":
            report.get(
                "recommendation_reason"
            ),

        # ----------------------------------------------------
        # Telegraph intelligence
        # ----------------------------------------------------

        "telegraph_intelligence":
            telegraph_intelligence,

        # ----------------------------------------------------
        # Provenance
        # ----------------------------------------------------

        "provenance":
            provenance,

        # ----------------------------------------------------
        # AI safety constraints
        # ----------------------------------------------------

        "ai_constraints": [

            "Do not select a route.",

            "Do not override NO_RECOMMENDATION.",

            "Do not create a recommendation.",

            "Do not modify a deterministic recommendation.",

            "Do not modify compliance status.",

            "Do not modify regulatory status.",

            "Do not modify geopolitical status.",

            "Do not modify risk values.",

            "Do not modify economic values.",

            "Do not treat Telegraph intelligence "
            "as a settlement decision.",

            "Do not use Telegraph intelligence "
            "to override deterministic eligibility.",

            "Do not use Telegraph intelligence "
            "to override deterministic ranking.",

            "Do not invent missing evidence.",

            "Do not invent costs.",

            "Do not invent regulatory conclusions.",

            "Do not invent geopolitical conclusions.",

            "Clearly identify incomplete data.",

            "Clearly identify provider-derived "
            "Telegraph intelligence.",

            "Explain the deterministic result only.",
        ],
    }

    return context


# ============================================================
# DISPLAY CONTROLLED CONTEXT
# ============================================================

def print_ai_decision_context(
    context
):

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

    # --------------------------------------------------------
    # Instruction
    # --------------------------------------------------------

    print("Instruction")
    print("-" * 60)

    print(
        context["instruction"]
    )

    print()

    # --------------------------------------------------------
    # Economic
    # --------------------------------------------------------

    economic = context[
        "economic"
    ]

    print("Economic")
    print("-" * 60)

    print(
        f"Transaction value: "
        f"${economic['transaction_value_usd']}"
    )

    print(
        f"Network cost: "
        f"${economic['network_cost_usd']}"
    )

    print(
        f"Status: "
        f"{economic['status']}"
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

    # --------------------------------------------------------
    # Economic gate
    # --------------------------------------------------------

    economic_gate = context[
        "economic_gate"
    ]

    print("Economic Gate")
    print("-" * 60)

    print(
        f"Status: "
        f"{economic_gate['status']}"
    )

    print(
        f"Reason: "
        f"{economic_gate['reason']}"
    )

    print()

    # --------------------------------------------------------
    # Routes
    # --------------------------------------------------------

    print("Route Decisions")
    print("-" * 60)

    for route in context[
        "routes"
    ]:

        print(
            f"{route['route']} | "
            f"{route['asset']} / "
            f"{route['network']}"
        )

        print(
            f"  Status: "
            f"{route['status']}"
        )

        if route["reason"]:

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
                f"  Evidence type: "
                f"{evidence['source_type']}"
            )

            print(
                f"  Evidence confidence: "
                f"{evidence['confidence']}"
            )

        cost = route.get(
            "cost"
        )

        if cost:

            print(
                f"  Cost: "
                f"{cost['value']} "
                f"{cost['currency']}"
            )

            print(
                f"  Cost status: "
                f"{cost['status']}"
            )

            print(
                f"  Cost source: "
                f"{cost['source']}"
            )

    print()

    # --------------------------------------------------------
    # Route ranking
    # --------------------------------------------------------

    print("Route Ranking")
    print("-" * 60)

    for route in context[
        "route_ranking"
    ]:

        print(
            f"{route}"
        )

    print()

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    print(
        "Deterministic Recommendation"
    )

    print("-" * 60)

    print(
        f"Recommendation: "
        f"{context['recommendation']}"
    )

    print(
        f"Reason: "
        f"{context['recommendation_reason']}"
    )

    print()

    # --------------------------------------------------------
    # Telegraph intelligence
    # --------------------------------------------------------

    telegraph = context.get(
        "telegraph_intelligence"
    )

    print(
        "Telegraph Intelligence"
    )

    print("-" * 60)

    if telegraph is None:

        print(
            "Status: NOT_AVAILABLE"
        )

    else:

        print(
            "Status: AVAILABLE"
        )

        if isinstance(
            telegraph,
            dict,
        ):

            print(
                f"Request ID: "
                f"{telegraph.get('request_id')}"
            )

            print(
                f"Generated at: "
                f"{telegraph.get('generated_at')}"
            )

            routes = telegraph.get(
                "routes",
                {}
            )

            print(
                f"Routes: "
                f"{list(routes.keys())}"
            )

            for route_id, route in (
                routes.items()
            ):

                evidence = route.get(
                    "evidence",
                    []
                )

                print(
                    f"  {route_id} | "
                    f"{route.get('asset')} / "
                    f"{route.get('network')} | "
                    f"evidence={len(evidence)}"
                )

    print()

    # --------------------------------------------------------
    # Provenance
    # --------------------------------------------------------

    print("Provenance")
    print("-" * 60)

    for key, value in context[
        "provenance"
    ].items():

        print(
            f"{key}: {value}"
        )

    print()

    # --------------------------------------------------------
    # AI constraints
    # --------------------------------------------------------

    print("AI Constraints")
    print("-" * 60)

    for constraint in context[
        "ai_constraints"
    ]:

        print(
            f"- {constraint}"
        )


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    report = load_settlement_report()

    context = build_ai_decision_context(
        report
    )

    print_ai_decision_context(
        context
    )