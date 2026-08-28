import json
from pathlib import Path

import pytest

from telegraph_intelligence_adapter import (
    normalize_telegraph_trade_context,
)
from intelligence_contract import is_usable


# ============================================================
# TEST DATA
# ============================================================

TELEGRAPH_RESPONSE = (
    Path(__file__).resolve().parent.parent
    / "Telegraph-MCP"
    / "trade_context_response.json"
)


@pytest.fixture
def trade_context():

    if not TELEGRAPH_RESPONSE.exists():
        pytest.skip(
            "Telegraph trade_context_response.json not available"
        )

    with TELEGRAPH_RESPONSE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


@pytest.fixture
def normalized(trade_context):

    return normalize_telegraph_trade_context(
        trade_context,
        request_id="test-telegraph",
    )


# ============================================================
# STRUCTURE
# ============================================================

def test_telegraph_response_normalizes(
    normalized,
):

    assert normalized["request_id"] == "test-telegraph"

    assert (
        normalized["generated_at"]
        is not None
    )

    assert set(
        normalized["routes"].keys()
    ) == {
        "bitcoin",
        "solana",
    }


# ============================================================
# BITCOIN
# ============================================================

def test_bitcoin_route_is_normalized(
    normalized,
):

    route = normalized["routes"]["bitcoin"]

    assert route["route_id"] == "bitcoin"
    assert route["asset"] == "BTC"
    assert route["network"] == "Bitcoin"

    assert len(
        route["evidence"]
    ) > 0


# ============================================================
# SOLANA
# ============================================================

def test_solana_route_is_normalized(
    normalized,
):

    route = normalized["routes"]["solana"]

    assert route["route_id"] == "solana"
    assert route["asset"] == "SOL"
    assert route["network"] == "Solana"

    assert len(
        route["evidence"]
    ) > 0


# ============================================================
# EVIDENCE CONTRACT
# ============================================================

def test_evidence_has_provider_independent_schema(
    normalized,
):

    required_fields = {
        "metric",
        "value",
        "unit",
        "source",
        "timestamp",
        "status",
        "confidence",
        "validation",
        "measurement_type",
    }

    for route in normalized["routes"].values():

        for evidence in route["evidence"]:

            assert set(
                evidence.keys()
            ) == required_fields


# ============================================================
# OBSERVED TELEGRAPH DATA
# ============================================================

def test_observed_telegraph_evidence_is_usable(
    normalized,
):

    observed_count = 0

    for route in normalized["routes"].values():

        for evidence in route["evidence"]:

            if (
                evidence["measurement_type"]
                == "OBSERVED"
            ):

                observed_count += 1

                assert (
                    evidence["status"]
                    == "AVAILABLE"
                )

                assert (
                    evidence["validation"]
                    == "VALID"
                )

                assert is_usable(
                    evidence
                )

    assert observed_count > 0


# ============================================================
# IMPORTANT AUTHORITY BOUNDARY
# ============================================================

def test_adapter_does_not_make_settlement_decision(
    normalized,
):

    assert (
        "decision"
        not in normalized
    )

    assert (
        "recommendation"
        not in normalized
    )

    assert (
        "eligible"
        not in normalized
    )

    assert (
        "settlement_decision"
        not in normalized
    )


# ============================================================
# MISSING DATA
# ============================================================

def test_missing_required_top_level_data_fails(
    trade_context,
):

    broken = dict(trade_context)

    broken.pop(
        "prices",
        None,
    )

    with pytest.raises(
        ValueError,
        match="prices",
    ):

        normalize_telegraph_trade_context(
            broken,
            request_id="test-missing",
        )
