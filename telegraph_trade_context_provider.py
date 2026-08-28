"""
Phase 10.4 — Telegraph Trade Context Provider

Responsibility:

    Load a captured Telegraph /trade-context JSON response.

This module ONLY handles provider-response acquisition.

It does NOT:

    - normalize intelligence
    - make settlement decisions
    - calculate settlement risk
    - select routes
    - recommend routes
"""

import json
from pathlib import Path


TRADE_CONTEXT_FILE = Path(
    "/tmp/telegraph_trade_context.json"
)


def load_trade_context(
    path=TRADE_CONTEXT_FILE,
):
    """
    Load a raw Telegraph /trade-context JSON response.

    Returns:
        dict

    Raises:
        FileNotFoundError
        ValueError
    """

    path = Path(path)

    if not path.exists():

        raise FileNotFoundError(
            f"Telegraph trade-context file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        trade_context = json.load(file)

    if not isinstance(
        trade_context,
        dict,
    ):

        raise ValueError(
            "Telegraph trade-context response "
            "must be a JSON object"
        )

    return trade_context


if __name__ == "__main__":

    trade_context = load_trade_context()

    print(
        "=== TELEGRAPH TRADE CONTEXT ==="
    )

    print(
        f"Top-level keys: "
        f"{list(trade_context.keys())}"
    )
