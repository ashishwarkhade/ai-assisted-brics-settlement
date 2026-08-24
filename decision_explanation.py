"""
Settlement Decision Explanation

Purpose:
    Build a human-readable explanation for a deterministic
    settlement route decision.

Important:

    This module explains an existing decision.

    It does NOT:
        - make a settlement decision
        - change eligibility
        - interpret regulatory evidence
        - override the deterministic decision engine

The explanation layer must support both:

    Phase 8 policy evidence
        value / source / source_type / confidence

and

    Phase 9 regulatory evidence
        jurisdiction / asset / activity / status /
        source / source_type / confidence / evidence_text
"""


# ============================================================
# BUILD DECISION EXPLANATION
# ============================================================

def build_decision_explanation(decision):
    """
    Build a human-readable explanation for one route decision.

    The decision itself remains authoritative.

    This function only explains the already-determined
    status and reason.
    """

    route = decision["route"]

    route_name = route.get(
        "route",
        "UNKNOWN",
    )

    asset = route.get(
        "asset",
        "UNKNOWN",
    )

    network = route.get(
        "network",
        "UNKNOWN",
    )

    status = decision.get(
        "status",
        "UNKNOWN",
    )

    reason = decision.get(
        "reason",
        None,
    )

    explanation = {
        "route": route_name,
        "asset": asset,
        "network": network,
        "status": status,
        "reason": reason,
    }


    # ========================================================
    # NO EVIDENCE
    # ========================================================

    if "evidence" not in decision:

        explanation["evidence"] = None

        explanation["text"] = (
            f"Route {route_name} "
            f"({asset} / {network}) "
            f"has status {status}."
        )

        if reason:

            explanation["text"] += (
                f" Reason: {reason}."
            )

        return explanation


    # ========================================================
    # EVIDENCE
    # ========================================================

    evidence = decision["evidence"]


    # --------------------------------------------------------
    # Common evidence fields
    # --------------------------------------------------------

    evidence_summary = {
        "source":
            evidence.get(
                "source",
                "UNKNOWN",
            ),

        "source_type":
            evidence.get(
                "source_type",
                "UNKNOWN",
            ),

        "confidence":
            evidence.get(
                "confidence",
                0.0,
            ),
    }


    # ========================================================
    # PHASE 9 REGULATORY EVIDENCE
    # ========================================================

    if "jurisdiction" in evidence:

        evidence_summary.update({

            "jurisdiction":
                evidence.get(
                    "jurisdiction",
                    "UNKNOWN",
                ),

            "asset":
                evidence.get(
                    "asset",
                    "UNKNOWN",
                ),

            "activity":
                evidence.get(
                    "activity",
                    "UNKNOWN",
                ),

            "regulatory_status":
                evidence.get(
                    "status",
                    "UNKNOWN",
                ),

            "evidence_text":
                evidence.get(
                    "evidence_text",
                    "",
                ),
        })


    # ========================================================
    # PHASE 8 / POLICY EVIDENCE
    # ========================================================

    else:

        evidence_summary["value"] = (
            evidence.get(
                "value",
                None,
            )
        )


    explanation["evidence"] = evidence_summary


    # ========================================================
    # HUMAN-READABLE EXPLANATION
    # ========================================================

    if "jurisdiction" in evidence:

        jurisdiction = evidence.get(
            "jurisdiction",
            "UNKNOWN",
        )

        regulatory_status = evidence.get(
            "status",
            "UNKNOWN",
        )

        activity = evidence.get(
            "activity",
            "UNKNOWN",
        )

        source = evidence.get(
            "source",
            "UNKNOWN",
        )

        explanation["text"] = (
            f"Route {route_name} "
            f"({asset} / {network}) "
            f"is {status} because regulatory status "
            f"for {asset} in {jurisdiction} "
            f"for activity {activity} is "
            f"{regulatory_status}. "
            f"Evidence source: {source}."
        )

    else:

        value = evidence.get(
            "value",
            None,
        )

        source = evidence.get(
            "source",
            "UNKNOWN",
        )

        explanation["text"] = (
            f"Route {route_name} "
            f"({asset} / {network}) "
            f"is {status}."
        )

        if value is not None:

            explanation["text"] += (
                f" Evidence value: {value}."
            )

        explanation["text"] += (
            f" Evidence source: {source}."
        )


    # ========================================================
    # DECISION REASON
    # ========================================================

    if reason:

        explanation["text"] += (
            f" Decision reason: {reason}."
        )


    return explanation


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_decision = {

        "route": {
            "route": "Base",
            "asset": "ETH",
            "network": "Base",
        },

        "status":
            "ELIGIBLE_DATA_INCOMPLETE",

        "reason":
            "REGULATORY_STATUS_UNKNOWN",

        "evidence": {

            "jurisdiction":
                "India",

            "asset":
                "ETH",

            "activity":
                "CROSS_BORDER_PAYMENT",

            "status":
                "UNKNOWN",

            "source":
                "NOT_YET_VALIDATED",

            "source_type":
                "UNKNOWN",

            "confidence":
                0.0,

            "evidence_text":
                "No jurisdiction-specific validated "
                "evidence has yet been entered.",
        },
    }


    explanation = (
        build_decision_explanation(
            test_decision
        )
    )


    print(
        "=== DECISION EXPLANATION TEST ==="
    )

    print()

    print(
        explanation["text"]
    )

    print()

    print(
        "Status:",
        explanation["status"],
    )

    print(
        "Reason:",
        explanation["reason"],
    )

    print(
        "Evidence:",
        explanation["evidence"],
    )