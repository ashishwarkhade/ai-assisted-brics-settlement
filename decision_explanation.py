import json


AUDIT_FILE = "audit/settlement_audit.json"


# ============================================================
# LOAD AUDIT
# ============================================================

def load_settlement_audit():

    with open(AUDIT_FILE, "r") as file:
        return json.load(file)


# ============================================================
# BUILD STRUCTURED DECISION EXPLANATION
# ============================================================

def build_decision_explanation(decision):

    route = decision["route"]

    explanation = {
        "route": route["route"],
        "asset": route["asset"],
        "network": route["network"],
        "decision": decision["status"],
        "reason": decision["reason"],
    }

    # --------------------------------------------------------
    # Evidence
    # --------------------------------------------------------

    if "evidence" in decision:

        evidence = decision["evidence"]

        explanation["evidence"] = {
            "value": evidence["value"],
            "source": evidence["source"],
            "source_type": evidence["source_type"],
            "confidence": evidence["confidence"],
        }

    # --------------------------------------------------------
    # Route cost
    # --------------------------------------------------------

    cost = route.get("cost")

    if cost:

        explanation["cost"] = {
            "value": cost.get("value"),
            "currency": cost.get("currency"),
            "status": cost.get("status"),
            "source": cost.get("source"),
            "confidence": cost.get("confidence"),
        }

    # --------------------------------------------------------
    # Network data
    # --------------------------------------------------------

    explanation["network_data"] = {
        "status": route.get("status"),
    }

    return explanation


# ============================================================
# HUMAN-READABLE EXPLANATION
# ============================================================

def print_route_explanation(explanation):

    print()
    print(
        f"{explanation['route']} "
        f"({explanation['asset']} / "
        f"{explanation['network']})"
    )

    print("-" * 55)

    print(
        f"Decision: "
        f"{explanation['decision']}"
    )

    if explanation.get("reason"):

        print(
            f"Reason: "
            f"{explanation['reason']}"
        )

    # --------------------------------------------------------
    # Evidence
    # --------------------------------------------------------

    evidence = explanation.get("evidence")

    if evidence:

        print()
        print("Compliance / Policy Evidence:")

        print(
            f"  Value: "
            f"{evidence['value']}"
        )

        print(
            f"  Source: "
            f"{evidence['source']}"
        )

        print(
            f"  Type: "
            f"{evidence['source_type']}"
        )

        print(
            f"  Confidence: "
            f"{evidence['confidence']}"
        )

    # --------------------------------------------------------
    # Cost
    # --------------------------------------------------------

    cost = explanation.get("cost")

    if cost:

        print()
        print("Route Cost:")

        value = cost.get("value")

        if value is None:

            print("  Value: UNKNOWN")

        else:

            currency = cost.get("currency", "")

            print(
                f"  Value: "
                f"{value:.6f} {currency}"
            )

        print(
            f"  Status: "
            f"{cost.get('status')}"
        )

        print(
            f"  Source: "
            f"{cost.get('source')}"
        )

        print(
            f"  Confidence: "
            f"{cost.get('confidence')}"
        )

    # --------------------------------------------------------
    # Network data
    # --------------------------------------------------------

    network_data = explanation.get("network_data")

    if network_data:

        print()
        print("Network Data:")

        print(
            f"  Status: "
            f"{network_data.get('status')}"
        )


# ============================================================
# FINAL DECISION EXPLANATION
# ============================================================

def print_final_explanation(audit):

    print()
    print("=== FINAL DECISION EXPLANATION ===")

    print()

    economic = audit["economic"]

    print("Economic Input")
    print("-" * 55)

    print(
        f"Transaction value: "
        f"${economic['transaction_value_usd']:.2f}"
    )

    print(
        f"Network cost: "
        f"${economic['network_cost_usd']:.6f}"
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

    # --------------------------------------------------------
    # Economic gate
    # --------------------------------------------------------

    gate = audit["economic_gate"]

    print()
    print("Economic Gate")
    print("-" * 55)

    print(
        f"Status: "
        f"{gate['status']}"
    )

    if gate.get("reason"):

        print(
            f"Reason: "
            f"{gate['reason']}"
        )

    # --------------------------------------------------------
    # Route explanations
    # --------------------------------------------------------

    print()
    print("Route Explanations")
    print("=" * 55)

    for decision in audit["route_decisions"]:

        if "explanation" in decision:

            explanation = decision["explanation"]

        else:

            explanation = build_decision_explanation(
                decision
            )

        print_route_explanation(explanation)

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    print()
    print("=== FINAL RECOMMENDATION ===")

    recommendation = audit.get("recommendation")

    if recommendation:

        print(
            f"Route: "
            f"{recommendation}"
        )

    else:

        print("NO_RECOMMENDATION")

    reason = audit.get("recommendation_reason")

    if reason:

        print(
            f"Reason: "
            f"{reason}"
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=== DECISION EXPLANATION MODULE ===")

    audit = load_settlement_audit()

    print_final_explanation(audit)

    print()
    print("Status: READY")