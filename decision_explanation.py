def build_decision_explanation(decision):

    route = decision["route"]

    explanation = {
        "route": route["route"],
        "asset": route["asset"],
        "network": route["network"],
        "decision": decision["status"],
        "reason": decision["reason"],
    }

    if "evidence" in decision:
        evidence = decision["evidence"]

        explanation["evidence"] = {
            "value": evidence["value"],
            "source": evidence["source"],
            "source_type": evidence["source_type"],
            "confidence": evidence["confidence"],
        }

    cost = route.get("cost")

    if cost:
        explanation["cost"] = {
            "value": cost.get("value"),
            "currency": cost.get("currency"),
            "status": cost.get("status"),
            "source": cost.get("source"),
            "confidence": cost.get("confidence"),
        }

    explanation["network_data"] = {
        "status": route.get("status"),
    }

    return explanation


if __name__ == "__main__":

    print("=== DECISION EXPLANATION MODULE ===")
    print("Status: READY")
