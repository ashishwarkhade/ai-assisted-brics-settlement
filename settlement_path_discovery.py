"""
BRICS Settlement Path Discovery

Phase 9.7

Purpose:
    Discover candidate BRICS settlement paths from the
    jurisdiction and payment-infrastructure registries.

IMPORTANT:

    Discovery is NOT recommendation.

    This module does NOT:
        - approve settlement paths
        - determine regulatory permission
        - infer crypto/infrastructure linkage
        - infer cross-border permission
        - rank routes
        - recommend a settlement route

    Unknown information remains UNKNOWN.

Architecture:

    BRICS Jurisdictions
            |
            v
    Payment Infrastructure
            |
            v
    Settlement Path Schema
            |
            v
    Candidate Settlement Paths
            |
            v
    Deterministic Decision Layer
"""


from brics_jurisdictions import (
    list_brics_jurisdictions,
    build_settlement_pair,
)

from brics_infrastructure import (
    get_infrastructure,
)

from brics_intelligence_schema import (
    build_settlement_path,
)


# ============================================================
# DISCOVERY CONFIGURATION
# ============================================================

DEFAULT_ASSET = "ETH"


# ============================================================
# INFRASTRUCTURE SELECTION
# ============================================================

def get_primary_infrastructure(
    jurisdiction,
):
    """
    Return the first registered payment infrastructure
    for a jurisdiction.

    Infrastructure availability does NOT imply:
        - asset support
        - crypto linkage
        - regulatory permission
        - cross-border settlement permission
    """

    records = get_infrastructure(
        jurisdiction
    )

    for record in records:

        if record["status"] == "AVAILABLE":

            return record["name"]

    return "UNKNOWN"


# ============================================================
# BUILD CANDIDATE PATH
# ============================================================

def build_candidate_path(
    source,
    destination,
    asset=DEFAULT_ASSET,
):
    """
    Build one candidate settlement path.

    Regulatory, linkage, and cross-border states remain
    UNKNOWN until validated evidence is available.
    """

    pair = build_settlement_pair(
        source,
        destination,
    )

    infrastructure = (
        get_primary_infrastructure(
            source
        )
    )

    return build_settlement_path(

        source_jurisdiction=
            pair["source_jurisdiction"],

        destination_jurisdiction=
            pair["destination_jurisdiction"],

        infrastructure=
            infrastructure,

        asset=
            asset,

        regulatory_status=
            "UNKNOWN",

        linkage_status=
            "UNKNOWN",

        cross_border_status=
            "UNKNOWN",
    )


# ============================================================
# DISCOVER SETTLEMENT PATHS
# ============================================================

def discover_settlement_paths(
    asset=DEFAULT_ASSET,
):
    """
    Discover candidate settlement paths between the
    registered BRICS jurisdictions.

    Self-to-self paths are excluded.
    """

    jurisdictions = (
        list_brics_jurisdictions()
    )

    paths = []

    for source in jurisdictions:

        for destination in jurisdictions:

            if source == destination:

                continue

            path = build_candidate_path(

                source=source,

                destination=destination,

                asset=asset,
            )

            paths.append(
                path
            )

    return paths


# ============================================================
# SUMMARY
# ============================================================

def summarize_paths(
    paths,
):
    """
    Build a small deterministic discovery summary.
    """

    return {
        "candidate_paths":
            len(paths),

        "asset":
            paths[0]["asset"]
            if paths
            else None,

        "regulatory_states":
            sorted(
                set(
                    path["regulatory_status"]
                    for path in paths
                )
            ),

        "linkage_states":
            sorted(
                set(
                    path["linkage_status"]
                    for path in paths
                )
            ),

        "cross_border_states":
            sorted(
                set(
                    path["cross_border_status"]
                    for path in paths
                )
            ),
    }


# ============================================================
# DISPLAY
# ============================================================

def print_settlement_paths(
    paths,
):
    """
    Display discovered candidate paths.
    """

    print(
        "=== PHASE 9.7 "
        "SETTLEMENT PATH DISCOVERY ==="
    )

    print()

    print(
        f"Candidate paths discovered: "
        f"{len(paths)}"
    )

    print()

    for index, path in enumerate(
        paths,
        start=1,
    ):

        print(
            f"[{index}] "
            f"{path['source_jurisdiction']} "
            f"→ "
            f"{path['destination_jurisdiction']}"
        )

        print(
            f"    Infrastructure: "
            f"{path['infrastructure']}"
        )

        print(
            f"    Asset: "
            f"{path['asset']}"
        )

        print(
            f"    Regulatory: "
            f"{path['regulatory_status']}"
        )

        print(
            f"    Linkage: "
            f"{path['linkage_status']}"
        )

        print(
            f"    Cross-border: "
            f"{path['cross_border_status']}"
        )

        print()


# ============================================================
# CONTROLLED TEST
# ============================================================

def run_controlled_test():

    paths = discover_settlement_paths()

    summary = summarize_paths(
        paths
    )

    print_settlement_paths(
        paths
    )

    print(
        "=== DISCOVERY SUMMARY ==="
    )

    print(
        f"Candidate paths: "
        f"{summary['candidate_paths']}"
    )

    print(
        f"Asset: "
        f"{summary['asset']}"
    )

    print(
        f"Regulatory states: "
        f"{summary['regulatory_states']}"
    )

    print(
        f"Linkage states: "
        f"{summary['linkage_states']}"
    )

    print(
        f"Cross-border states: "
        f"{summary['cross_border_states']}"
    )

    print()

    print(
        "Decision authority:",
        "NOT_PERFORMED",
    )

    print(
        "Status:",
        "READY",
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_controlled_test()