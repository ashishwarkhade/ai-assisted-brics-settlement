import json

import ai_decision_context


# ============================================================
# PHASE 8.15
# FINAL CONTROL / VALIDATION
# ============================================================

AUDIT_FILE = "audit/settlement_audit.json"
REPORT_FILE = "audit/settlement_report_8_12.json"


# ============================================================
# LOAD JSON
# ============================================================

def load_json(filename):

    with open(filename, "r") as file:
        return json.load(file)


# ============================================================
# VALIDATION HELPER
# ============================================================

def check(condition, message):

    if condition:

        print(f"[PASS] {message}")
        return True

    print(f"[FAIL] {message}")
    return False


# ============================================================
# MAIN VALIDATION
# ============================================================

def validate_phase_8_15():

    audit = load_json(AUDIT_FILE)
    report = load_json(REPORT_FILE)

    results = []

    print("=== PHASE 8.15 FINAL CONTROL VALIDATION ===")
    print()

    # ========================================================
    # 1. ECONOMIC DATA
    # ========================================================

    economic = audit.get(
        "economic",
        {},
    )

    results.append(
        check(
            economic.get("status") == "REAL",
            "Economic input is REAL",
        )
    )

    results.append(
        check(
            economic.get("confidence", 0) > 0,
            "Economic confidence is available",
        )
    )

    # ========================================================
    # 2. ECONOMIC GATE
    # ========================================================

    economic_gate = audit.get(
        "economic_gate",
        {},
    )

    results.append(
        check(
            economic_gate.get("status")
            in ("PASSED", "REJECTED"),
            "Economic gate has a deterministic status",
        )
    )

    # ========================================================
    # 3. ROUTE DECISIONS
    # ========================================================

    route_decisions = audit.get(
        "route_decisions",
        [],
    )

    results.append(
        check(
            len(route_decisions) > 0,
            "Route decisions are present",
        )
    )

    valid_statuses = {
        "ELIGIBLE",
        "ELIGIBLE_DATA_INCOMPLETE",
        "REJECTED",
        "INVALID",
    }

    for decision in route_decisions:

        route_name = decision.get(
            "route",
            "UNKNOWN",
        )

        results.append(
            check(
                decision.get("status")
                in valid_statuses,
                f"{route_name} has a valid deterministic status",
            )
        )

    # ========================================================
    # 4. DETERMINISTIC RECOMMENDATION
    # ========================================================

    recommendation = audit.get(
        "recommendation"
    )

    recommendation_reason = audit.get(
        "recommendation_reason"
    )

    results.append(
        check(
            recommendation is None,
            "Deterministic recommendation is NO_RECOMMENDATION",
        )
    )

    results.append(
        check(
            recommendation_reason
            == "NO_ROUTE_HAS_SUFFICIENT_POLICY_AND_COST_DATA",
            "NO_RECOMMENDATION reason is preserved",
        )
    )

    # ========================================================
    # 5. ROUTE RANKING
    # ========================================================

    ranking = audit.get(
        "route_ranking",
        [],
    )

    results.append(
        check(
            len(ranking) == 0,
            "Route ranking is empty when no route is eligible",
        )
    )

    # ========================================================
    # 6. DECISION CONFIDENCE
    #
    # IMPORTANT:
    # The settlement report stores this under:
    #
    # report["confidence"]
    #
    # ========================================================

    confidence = report.get(
        "confidence",
        {},
    )

    overall_confidence = confidence.get(
        "overall_confidence"
    )

    results.append(
        check(
            overall_confidence is not None,
            "Decision confidence is present",
        )
    )

    # ========================================================
    # 7. AUTOMATION READINESS
    # ========================================================

    automation_readiness = confidence.get(
        "automation_readiness"
    )

    results.append(
        check(
            automation_readiness
            == "NOT_READY_FOR_AUTOMATED_RECOMMENDATION",
            "Automation readiness blocks automated recommendation",
        )
    )

    # ========================================================
    # 8. AI AUTHORITY
    # ========================================================

    ai_authority = getattr(
        ai_decision_context,
        "AI_AUTHORITY",
        None,
    )

    results.append(
        check(
            ai_authority == "EXPLANATION_ONLY",
            "AI authority is EXPLANATION_ONLY",
        )
    )

    # ========================================================
    # 9. AI CANNOT CREATE RECOMMENDATION
    # ========================================================

    results.append(
        check(
            recommendation is None,
            "AI cannot create a settlement recommendation",
        )
    )

    # ========================================================
    # 10. INCOMPLETE POLICY DATA REMAINS UNRESOLVED
    # ========================================================

    incomplete_routes = [

        decision

        for decision in route_decisions

        if decision.get("status")
        == "ELIGIBLE_DATA_INCOMPLETE"
    ]

    results.append(
        check(
            len(incomplete_routes) > 0,
            "Incomplete policy routes remain unresolved",
        )
    )

    # ========================================================
    # 11. AI CANNOT OVERRIDE DETERMINISTIC RESULT
    # ========================================================

    results.append(
        check(
            ai_authority == "EXPLANATION_ONLY"
            and recommendation is None,
            "AI cannot override NO_RECOMMENDATION",
        )
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("=== FINAL VALIDATION RESULT ===")

    if all(results):

        print("PHASE_8_15_VALIDATION: PASS")

        print()
        print(
            "Deterministic decision remains:"
        )

        print(
            "NO_RECOMMENDATION"
        )

        print()
        print(
            "AI authority remains:"
        )

        print(
            "EXPLANATION_ONLY"
        )

        print()
        print(
            "Automation readiness remains:"
        )

        print(
            "NOT_READY_FOR_AUTOMATED_RECOMMENDATION"
        )

        return True

    print("PHASE_8_15_VALIDATION: FAIL")

    return False


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = validate_phase_8_15()

    if not success:

        raise SystemExit(1)