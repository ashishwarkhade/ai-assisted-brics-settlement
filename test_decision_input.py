import pytest

from decision_input import build_decision_input


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def intelligence():
    return {
        "asset": "ETH",
        "network": "Base",
        "chain_id": 8453,

        "status": "REAL",
        "confidence": 1.0,

        "value_usd": 126.78,
        "network_cost_usd": 0.00085,

        "market_price_usd": 4210.50,
    }


@pytest.fixture
def regulatory_evidence():
    return {
        "jurisdiction": "TEST",
        "asset": "ETH",
        "activity": "SETTLEMENT",
        "status": "UNKNOWN",
        "source": "TEST",
        "source_type": "REFERENCE",
        "confidence": 0.0,
        "evidence_text": "Test regulatory evidence",
    }


@pytest.fixture
def telegraph_intelligence():
    return {
        "provider": "telegraph",
        "status": "AVAILABLE",
        "routes": {
            "bitcoin": {
                "asset": "BTC",
                "network": "Bitcoin",
                "evidence": [
                    {
                        "metric": "btc_price",
                        "value": 79676.65,
                        "unit": "USD",
                        "status": "AVAILABLE",
                        "confidence": "HIGH",
                    }
                ],
            },
            "solana": {
                "asset": "SOL",
                "network": "Solana",
                "evidence": [
                    {
                        "metric": "sol_price",
                        "value": 107.105,
                        "unit": "USD",
                        "status": "AVAILABLE",
                        "confidence": "HIGH",
                    }
                ],
            },
        },
    }


# ============================================================
# BASIC BEHAVIOR
# ============================================================

def test_build_decision_input_preserves_transaction_intelligence(
    intelligence,
):

    decision_input = build_decision_input(
        intelligence
    )

    assert decision_input["asset"] == "ETH"
    assert decision_input["network"] == "Base"
    assert decision_input["chain_id"] == 8453

    assert (
        decision_input["transaction_status"]
        == "REAL"
    )

    assert (
        decision_input["confidence"]
        == 1.0
    )

    assert (
        decision_input["transaction_value_usd"]
        == 126.78
    )

    assert (
        decision_input["network_cost_usd"]
        == 0.00085
    )


# ============================================================
# ECONOMIC DATA
# ============================================================

def test_decision_input_contains_economic_data(
    intelligence,
):

    decision_input = build_decision_input(
        intelligence
    )

    assert "economic_data" in decision_input

    assert (
        decision_input["economic_data"][
            "asset_price_usd"
        ]
        == 4210.50
    )

    assert (
        decision_input["economic_data"][
            "network_cost_usd"
        ]
        == 0.00085
    )


# ============================================================
# REGULATORY CONTEXT
# ============================================================

def test_regulatory_evidence_is_optional(
    intelligence,
):

    decision_input = build_decision_input(
        intelligence
    )

    assert "regulatory" not in decision_input


def test_regulatory_evidence_is_preserved(
    intelligence,
    regulatory_evidence,
):

    decision_input = build_decision_input(
        intelligence,
        regulatory_evidence=regulatory_evidence,
    )

    assert (
        decision_input["regulatory"]
        == regulatory_evidence
    )


# ============================================================
# PHASE 10.4 — TELEGRAPH INTELLIGENCE
# ============================================================

def test_telegraph_intelligence_is_optional(
    intelligence,
):

    decision_input = build_decision_input(
        intelligence
    )

    assert (
        "telegraph_intelligence"
        not in decision_input
    )


def test_telegraph_intelligence_is_preserved(
    intelligence,
    telegraph_intelligence,
):

    decision_input = build_decision_input(
        intelligence,
        telegraph_intelligence=
            telegraph_intelligence,
    )

    assert (
        decision_input["telegraph_intelligence"]
        == telegraph_intelligence
    )


def test_regulatory_and_telegraph_intelligence_can_coexist(
    intelligence,
    regulatory_evidence,
    telegraph_intelligence,
):

    decision_input = build_decision_input(
        intelligence,
        regulatory_evidence=
            regulatory_evidence,
        telegraph_intelligence=
            telegraph_intelligence,
    )

    assert (
        decision_input["regulatory"]
        == regulatory_evidence
    )

    assert (
        decision_input["telegraph_intelligence"]
        == telegraph_intelligence
    )


# ============================================================
# ARCHITECTURAL SAFETY
# ============================================================

def test_decision_input_does_not_make_settlement_decision(
    intelligence,
    telegraph_intelligence,
):

    decision_input = build_decision_input(
        intelligence,
        telegraph_intelligence=
            telegraph_intelligence,
    )

    assert "decision" not in decision_input
    assert "recommendation" not in decision_input
    assert "eligible" not in decision_input
    assert "settlement_decision" not in decision_input


def test_telegraph_data_does_not_override_transaction_fields(
    intelligence,
    telegraph_intelligence,
):

    original_asset = intelligence["asset"]
    original_network = intelligence["network"]
    original_value = intelligence["value_usd"]

    decision_input = build_decision_input(
        intelligence,
        telegraph_intelligence=
            telegraph_intelligence,
    )

    assert (
        decision_input["asset"]
        == original_asset
    )

    assert (
        decision_input["network"]
        == original_network
    )

    assert (
        decision_input["transaction_value_usd"]
        == original_value
    )


# ============================================================
# PROVIDER INDEPENDENCE
# ============================================================

def test_decision_input_keeps_telegraph_as_intelligence_only(
    intelligence,
    telegraph_intelligence,
):

    decision_input = build_decision_input(
        intelligence,
        telegraph_intelligence=
            telegraph_intelligence,
    )

    telegraph = (
        decision_input[
            "telegraph_intelligence"
        ]
    )

    assert (
        telegraph["provider"]
        == "telegraph"
    )

    assert (
        telegraph["status"]
        == "AVAILABLE"
    )

    assert "decision" not in telegraph
    assert "recommendation" not in telegraph