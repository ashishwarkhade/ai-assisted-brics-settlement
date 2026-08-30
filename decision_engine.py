# ============================================================
# DECISION ENGINE
# ============================================================
#
# Phase E.4.3
#
# Purpose:
#     Execute deterministic route evaluation, ranking, and
#     recommendation behind the DecisionEngine boundary.
#
# Architecture:
#
#     PaymentIntent
#          ↓
#     DecisionInput
#          ↓
#     DecisionEngine
#          ↓
#     Deterministic route evaluation
#          ↓
#     Deterministic route ranking
#          ↓
#     Deterministic recommendation
#
# The engine does NOT:
#     - create PaymentIntent
#     - collect provider intelligence
#     - discover routes
#     - normalize Telegraph data
#     - make AI-generated decisions
#     - override evidence
#
# Route and policy data are supplied explicitly.
#
# E.4.3 preserves the existing settlement_decision.py
# ranking behavior:
#
#     ELIGIBLE routes with known cost
#     → sorted by ascending cost
#     → cheapest route recommended
#
# No new scoring model is introduced.
# ============================================================


# ============================================================
# DECISION POLICY
# ============================================================

DEFAULT_MAX_RISK = 50


# ============================================================
# DECISION ENGINE
# ============================================================

class DecisionEngine:
    """
    Deterministic settlement decision engine.

    E.4.3 provides:

        1. DecisionInput validation
        2. Deterministic route evaluation
        3. Deterministic route ranking
        4. Deterministic recommendation

    The engine receives all external intelligence explicitly.
    """

    def __init__(
        self,
        max_risk=DEFAULT_MAX_RISK,
    ):

        self.max_risk = max_risk

    # --------------------------------------------------------
    # VALIDATE DECISION INPUT
    # --------------------------------------------------------

    def validate_input(
        self,
        decision_input,
    ):
        """
        Validate the minimum DecisionInput structure.

        This remains structural validation only.
        """

        if not isinstance(
            decision_input,
            dict,
        ):

            raise ValueError(
                "DecisionInput must be a dictionary"
            )

        required_fields = (
            "asset",
            "network",
            "chain_id",
            "transaction_status",
            "confidence",
            "transaction_value_usd",
            "network_cost_usd",
            "economic_data",
        )

        missing = [
            field
            for field in required_fields
            if field not in decision_input
        ]

        if missing:

            raise ValueError(
                "DecisionInput missing required fields: "
                + ", ".join(missing)
            )

        if not isinstance(
            decision_input["economic_data"],
            dict,
        ):

            raise ValueError(
                "DecisionInput economic_data "
                "must be a dictionary"
            )

        return True

    # --------------------------------------------------------
    # E.4.2 — EVALUATE ROUTES
    # --------------------------------------------------------

    def evaluate_routes(
        self,
        decision_input,
        normalized_routes,
        policies,
        regulatory_state,
        regulatory_evidence,
    ):
        """
        Apply the existing deterministic route rules.

        Rule order:

            1. Missing policy
            2. Regulatory gate
            3. Compliance
            4. Geopolitical status
            5. Risk
            6. Route cost
            7. ELIGIBLE

        No new eligibility policy is introduced.
        """

        self.validate_input(
            decision_input
        )

        if not isinstance(
            normalized_routes,
            dict,
        ):

            raise ValueError(
                "normalized_routes must be a dictionary"
            )

        if not isinstance(
            policies,
            dict,
        ):

            raise ValueError(
                "policies must be a dictionary"
            )

        if not isinstance(
            regulatory_evidence,
            dict,
        ):

            raise ValueError(
                "regulatory_evidence must be a dictionary"
            )

        decisions = []

        for route_key, route in (
            normalized_routes.items()
        ):

            network = route["network"]

            policy = policies.get(
                network
            )

            # ------------------------------------------------
            # Missing policy
            # ------------------------------------------------

            if policy is None:

                decisions.append({
                    "route": route,
                    "status": "INVALID",
                    "reason":
                        "MISSING_ROUTE_POLICY",
                })

                continue

            # ------------------------------------------------
            # Regulatory gate
            # ------------------------------------------------

            if regulatory_state == "PROHIBITED":

                decisions.append({
                    "route": route,

                    "status":
                        "REJECTED",

                    "reason":
                        "REGULATORY_STATUS_PROHIBITED",

                    "evidence":
                        regulatory_evidence,
                })

                continue

            if regulatory_state != "PERMITTED":

                decisions.append({
                    "route": route,

                    "status":
                        "ELIGIBLE_DATA_INCOMPLETE",

                    "reason":
                        "REGULATORY_STATUS_UNKNOWN",

                    "evidence":
                        regulatory_evidence,
                })

                continue

            # ------------------------------------------------
            # Compliance
            # ------------------------------------------------

            compliance = policy[
                "compliance"
            ]

            if compliance["value"] == "BLOCKED":

                decisions.append({
                    "route": route,

                    "status":
                        "REJECTED",

                    "reason":
                        "COMPLIANCE_BLOCKED",

                    "evidence":
                        compliance,
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

            # ------------------------------------------------
            # Geopolitical
            # ------------------------------------------------

            geopolitical = policy[
                "geopolitical_status"
            ]

            if geopolitical["value"] == "RESTRICTED":

                decisions.append({
                    "route": route,

                    "status":
                        "REJECTED",

                    "reason":
                        "GEOPOLITICAL_RESTRICTION",

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

            # ------------------------------------------------
            # Risk
            # ------------------------------------------------

            risk = policy[
                "risk"
            ]

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

            if risk["value"] > self.max_risk:

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

            # ------------------------------------------------
            # Economic route cost
            # ------------------------------------------------

            cost = route[
                "cost"
            ]

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

            # ------------------------------------------------
            # Fully eligible
            # ------------------------------------------------

            decisions.append({
                "route": route,

                "status":
                    "ELIGIBLE",

                "reason":
                    None,
            })

        return decisions

    # --------------------------------------------------------
    # E.4.3 — RANK ROUTES
    # --------------------------------------------------------

    def rank_routes(
        self,
        decisions,
    ):
        """
        Rank economically comparable eligible routes.

        Existing behavior is preserved:

            - only ELIGIBLE routes qualify
            - cost must be known
            - ascending cost determines ranking

        No route is ranked on AI, Telegraph, risk score,
        confidence, or any newly invented metric.
        """

        if not isinstance(
            decisions,
            list,
        ):

            raise ValueError(
                "decisions must be a list"
            )

        rankable_routes = [

            decision["route"]

            for decision in decisions

            if decision["status"]
            == "ELIGIBLE"

            and decision["route"]["cost"]["value"]
            is not None
        ]

        ranked_routes = sorted(
            rankable_routes,
            key=lambda route:
                route["cost"]["value"]
        )

        return ranked_routes

    # --------------------------------------------------------
    # E.4.3 — RECOMMEND
    # --------------------------------------------------------

    def recommend(
        self,
        ranked_routes,
    ):
        """
        Produce the deterministic route recommendation.

        The cheapest rankable route is recommended.

        If no route has sufficient policy and economic data,
        no recommendation is produced.
        """

        if not isinstance(
            ranked_routes,
            list,
        ):

            raise ValueError(
                "ranked_routes must be a list"
            )

        if not ranked_routes:

            return {
                "recommendation": None,

                "recommendation_reason":
                    "NO_ROUTE_HAS_SUFFICIENT_POLICY_AND_COST_DATA",
            }

        best_route = ranked_routes[0]

        recommendation = {
            "route":
                best_route["route"],

            "asset":
                best_route["asset"],

            "network":
                best_route["network"],
        }

        return {
            "recommendation":
                recommendation,

            "recommendation_reason":
                None,
        }

    # --------------------------------------------------------
    # DECIDE
    # --------------------------------------------------------

    def decide(
        self,
        decision_input,
        normalized_routes=None,
        policies=None,
        regulatory_state=None,
        regulatory_evidence=None,
    ):
        """
        Execute the deterministic decision boundary.

        E.4.1 compatibility:
            If deterministic route context is absent,
            only the input boundary is accepted.

        E.4.2:
            Evaluate deterministic route eligibility.

        E.4.3:
            Rank eligible routes and produce a deterministic
            recommendation.
        """

        self.validate_input(
            decision_input
        )

        # ----------------------------------------------------
        # E.4.1 compatibility mode
        # ----------------------------------------------------

        if (
            normalized_routes is None
            or policies is None
            or regulatory_state is None
            or regulatory_evidence is None
        ):

            return {
                "status":
                    "INPUT_ACCEPTED",

                "decision_input":
                    decision_input,

                "decision_made":
                    False,

                "reason":
                    "DECISION_ENGINE_BOUNDARY_ESTABLISHED",
            }

        # ----------------------------------------------------
        # E.4.2 — deterministic evaluation
        # ----------------------------------------------------

        decisions = self.evaluate_routes(
            decision_input=
                decision_input,

            normalized_routes=
                normalized_routes,

            policies=
                policies,

            regulatory_state=
                regulatory_state,

            regulatory_evidence=
                regulatory_evidence,
        )

        # ----------------------------------------------------
        # E.4.3 — deterministic ranking
        # ----------------------------------------------------

        ranked_routes = self.rank_routes(
            decisions
        )

        # ----------------------------------------------------
        # E.4.3 — deterministic recommendation
        # ----------------------------------------------------

        recommendation_result = self.recommend(
            ranked_routes
        )

        return {
            "status":
                "DECISION_EVALUATED",

            "decision_input":
                decision_input,

            "decision_made":
                True,

            "decisions":
                decisions,

            "ranked_routes":
                ranked_routes,

            "recommendation":
                recommendation_result[
                    "recommendation"
                ],

            "recommendation_reason":
                recommendation_result[
                    "recommendation_reason"
                ],

            "reason":
                "DETERMINISTIC_ROUTE_EVALUATION_COMPLETE",
        }


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    from decision_input import (
        build_decision_input,
    )

    from transaction_intelligence import (
        build_transaction_intelligence,
    )

    from normalized_routes import (
        get_normalized_routes,
    )

    from policy_intelligence import (
        build_policy_intelligence,
    )

    from brics_regulatory_evidence import (
        build_example_unknown,
        determine_regulatory_state,
    )

    intelligence = (
        build_transaction_intelligence()
    )

    decision_input = build_decision_input(
        intelligence
    )

    regulatory_evidence = (
        build_example_unknown()
    )

    regulatory_state = (
        determine_regulatory_state(
            regulatory_evidence
        )
    )

    normalized_routes = (
        get_normalized_routes()
    )

    policies = (
        build_policy_intelligence()
    )

    engine = DecisionEngine()

    result = engine.decide(
        decision_input=
            decision_input,

        normalized_routes=
            normalized_routes,

        policies=
            policies,

        regulatory_state=
            regulatory_state,

        regulatory_evidence=
            regulatory_evidence,
    )

    print(
        "=== PHASE E.4.3 DECISION ENGINE ==="
    )

    print(
        "DecisionInput validation: PASS"
    )

    print(
        f"Status: "
        f"{result['status']}"
    )

    print(
        f"Decision made: "
        f"{result['decision_made']}"
    )

    print(
        f"Reason: "
        f"{result['reason']}"
    )

    print()

    for decision in result[
        "decisions"
    ]:

        route = decision[
            "route"
        ]

        print(
            f"{route['route']} | "
            f"{decision['status']}"
        )

        if decision["reason"]:

            print(
                f"  Reason: "
                f"{decision['reason']}"
            )

    print()

    print(
        "=== ROUTE RANKING ==="
    )

    if not result[
        "ranked_routes"
    ]:

        print(
            "No route has sufficient "
            "policy and economic data."
        )

    else:

        for route in result[
            "ranked_routes"
        ]:

            print(
                f"{route['route']} | "
                f"{route['asset']} / "
                f"{route['network']} | "
                f"${route['cost']['value']:.6f}"
            )

    print()

    print(
        "=== RECOMMENDATION ==="
    )

    if result[
        "recommendation"
    ] is None:

        print(
            "NO_RECOMMENDATION"
        )

        print(
            f"Reason: "
            f"{result['recommendation_reason']}"
        )

    else:

        recommendation = result[
            "recommendation"
        ]

        print(
            f"{recommendation['route']} | "
            f"{recommendation['asset']} / "
            f"{recommendation['network']}"
        )