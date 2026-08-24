"""
BRICS Payment Infrastructure Registry

Phase 9.3

This module records payment infrastructure associated
with the BRICS jurisdictions in our initial intelligence
scope.

IMPORTANT:

Infrastructure availability does NOT imply:

    - cryptocurrency permission
    - asset support
    - crypto/infrastructure linkage
    - cross-border settlement permission
    - regulatory approval

Those questions belong to later intelligence layers.
"""


# ============================================================
# PAYMENT INFRASTRUCTURE
# ============================================================

BRICS_INFRASTRUCTURE = {

    "India": [
        {
            "name": "UPI",
            "status": "AVAILABLE",
            "type": "PAYMENT_INFRASTRUCTURE",
        }
    ],

    "China": [
        {
            "name": "CIPS",
            "status": "AVAILABLE",
            "type": "PAYMENT_INFRASTRUCTURE",
        }
    ],

    "Russia": [
        {
            "name": "SPFS",
            "status": "AVAILABLE",
            "type": "PAYMENT_INFRASTRUCTURE",
        }
    ],

    "Brazil": [
        {
            "name": "Pix",
            "status": "AVAILABLE",
            "type": "PAYMENT_INFRASTRUCTURE",
        }
    ],

    "South Africa": [
        {
            "name": "UNKNOWN",
            "status": "UNKNOWN",
            "type": "PAYMENT_INFRASTRUCTURE",
        }
    ],
}


# ============================================================
# GET INFRASTRUCTURE
# ============================================================

def get_infrastructure(jurisdiction):

    if jurisdiction not in BRICS_INFRASTRUCTURE:

        raise ValueError(
            f"Unknown BRICS jurisdiction: "
            f"{jurisdiction}"
        )

    return BRICS_INFRASTRUCTURE[jurisdiction]


# ============================================================
# CHECK INFRASTRUCTURE AVAILABILITY
# ============================================================

def infrastructure_available(
    jurisdiction,
    infrastructure,
):

    records = get_infrastructure(
        jurisdiction
    )

    for record in records:

        if record["name"] == infrastructure:

            return record["status"] == "AVAILABLE"

    return False


# ============================================================
# BUILD INFRASTRUCTURE INTELLIGENCE
# ============================================================

def build_infrastructure_intelligence(
    jurisdiction,
    infrastructure,
):

    records = get_infrastructure(
        jurisdiction
    )

    for record in records:

        if record["name"] == infrastructure:

            return {
                "jurisdiction": jurisdiction,
                "infrastructure":
                    infrastructure,
                "status":
                    record["status"],
                "type":
                    record["type"],
            }

    return {
        "jurisdiction": jurisdiction,
        "infrastructure":
            infrastructure,
        "status": "UNKNOWN",
        "type": "PAYMENT_INFRASTRUCTURE",
    }


# ============================================================
# DISPLAY
# ============================================================

def print_infrastructure_registry():

    print(
        "=== BRICS PAYMENT INFRASTRUCTURE ==="
    )

    print()

    for jurisdiction, records in (
        BRICS_INFRASTRUCTURE.items()
    ):

        for record in records:

            print(
                f"{jurisdiction} | "
                f"{record['name']} | "
                f"{record['status']}"
            )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print_infrastructure_registry()

    print()

    print(
        "=== EXAMPLE INTELLIGENCE ==="
    )

    print()

    india_upi = (
        build_infrastructure_intelligence(
            "India",
            "UPI",
        )
    )

    print(india_upi)

    print()

    print(
        "UPI available in India:",
        infrastructure_available(
            "India",
            "UPI",
        ),
    )

    print()

    print(
        "ETH linkage:",
        "UNKNOWN",
    )

    print(
        "Regulatory status:",
        "UNKNOWN",
    )

    print(
        "Cross-border status:",
        "UNKNOWN",
    )

    print()

    print("Status: READY")
