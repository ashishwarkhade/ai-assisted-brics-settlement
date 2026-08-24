"""
BRICS Jurisdiction Registry

Phase 9.2

Purpose:
    Maintain the initial jurisdiction registry for the
    BRICS settlement intelligence layer.

Important:
    This module does NOT determine regulatory status.

    It only identifies jurisdictions that are part of the
    initial BRICS intelligence scope.

Architecture:

    BRICS Jurisdiction Registry
              |
              v
    Infrastructure Intelligence
              |
              v
    Regulatory Evidence
              |
              v
    Asset / Infrastructure Linkage
              |
              v
    Cross-Border Settlement Intelligence
"""


# ============================================================
# BRICS JURISDICTIONS
# ============================================================

BRICS_JURISDICTIONS = {

    "India": {
        "code": "IN",
        "name": "India",
    },

    "China": {
        "code": "CN",
        "name": "China",
    },

    "Russia": {
        "code": "RU",
        "name": "Russia",
    },

    "Brazil": {
        "code": "BR",
        "name": "Brazil",
    },

    "South Africa": {
        "code": "ZA",
        "name": "South Africa",
    },
}


# ============================================================
# JURISDICTION LOOKUP
# ============================================================

def get_jurisdiction(name):

    """
    Return a jurisdiction record.

    Raises:
        ValueError if jurisdiction is not registered.
    """

    if name not in BRICS_JURISDICTIONS:

        raise ValueError(
            f"Unknown BRICS jurisdiction: {name}"
        )

    return BRICS_JURISDICTIONS[name]


# ============================================================
# JURISDICTION VALIDATION
# ============================================================

def is_brics_jurisdiction(name):

    """
    Return True when the jurisdiction belongs to the
    current BRICS intelligence scope.
    """

    return name in BRICS_JURISDICTIONS


# ============================================================
# LIST JURISDICTIONS
# ============================================================

def list_brics_jurisdictions():

    """
    Return the registered BRICS jurisdictions.
    """

    return list(
        BRICS_JURISDICTIONS.keys()
    )


# ============================================================
# BUILD SETTLEMENT PAIR
# ============================================================

def build_settlement_pair(
    source,
    destination,
):
    """
    Build a validated source/destination jurisdiction pair.

    Both jurisdictions must exist in the registry.
    """

    if not is_brics_jurisdiction(source):

        raise ValueError(
            f"Invalid source jurisdiction: {source}"
        )

    if not is_brics_jurisdiction(destination):

        raise ValueError(
            f"Invalid destination jurisdiction: "
            f"{destination}"
        )

    return {
        "source_jurisdiction": source,
        "source_code":
            BRICS_JURISDICTIONS[source]["code"],

        "destination_jurisdiction": destination,
        "destination_code":
            BRICS_JURISDICTIONS[destination]["code"],
    }


# ============================================================
# DISPLAY
# ============================================================

def print_registry():

    print("=== BRICS JURISDICTION REGISTRY ===")
    print()

    for name, jurisdiction in BRICS_JURISDICTIONS.items():

        print(
            f"{name} | "
            f"{jurisdiction['code']}"
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print_registry()

    print()

    pair = build_settlement_pair(
        "India",
        "Brazil",
    )

    print("Example settlement pair")
    print("----------------------------------------")

    print(
        f"{pair['source_jurisdiction']} "
        f"({pair['source_code']})"
    )

    print(
        f"→ "
        f"{pair['destination_jurisdiction']} "
        f"({pair['destination_code']})"
    )

    print()

    print(
        "India is BRICS jurisdiction:",
        is_brics_jurisdiction("India"),
    )

    print(
        "Brazil is BRICS jurisdiction:",
        is_brics_jurisdiction("Brazil"),
    )

    print()

    print("Status: READY")
