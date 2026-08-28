import copy

from decision_input import build_decision_input


def test_telegraph_intelligence_is_passed_through():
    intelligence = {
        "asset": "ETH",
        "network": "Base",
        "chain_id": 8453,
        "status": "CONFIRMED",
        "confidence": "HIGH",
        "value_usd": 100.0,
        "network_cost_usd": 0.25,
        "market_price_usd": 3000.0,
    }

    telegraph_intelligence = {
        "request_id": "phase-10.4-test",
        "generated_at": "2026-08-28T00:00:00+00:00",
        "routes": {
            "bitcoin": {
                "route_id": "bitcoin",
                "asset": "BTC",
                "network": "Bitcoin",
                "evidence": [],
            },
            "solana": {
                "route_id": "solana",
                "asset": "SOL",
                "network": "Solana",
                "evidence": [],
            },
        },
    }

    result = build_decision_input(
        intelligence=intelligence,
        telegraph_intelligence=telegraph_intelligence,
    )

    assert (
        result["telegraph_intelligence"]
        == telegraph_intelligence
    )


def test_telegraph_intelligence_does_not_replace_core_transaction_data():
    intelligence = {
        "asset": "ETH",
        "network": "Base",
        "chain_id": 8453,
        "status": "CONFIRMED",
        "confidence": "HIGH",
        "value_usd": 100.0,
        "network_cost_usd": 0.25,
        "market_price_usd": 3000.0,
    }

    telegraph_intelligence = {
        "request_id": "phase-10.4-test",
        "generated_at": "2026-08-28T00:00:00+00:00",
        "routes": {},
    }

    result = build_decision_input(
        intelligence=intelligence,
        telegraph_intelligence=telegraph_intelligence,
    )

    assert result["asset"] == "ETH"
    assert result["network"] == "Base"
    assert result["chain_id"] == 8453
    assert result["transaction_value_usd"] == 100.0
    assert result["network_cost_usd"] == 0.25


def test_telegraph_intelligence_is_not_a_settlement_decision():
    intelligence = {
        "asset": "ETH",
        "network": "Base",
        "chain_id": 8453,
        "status": "CONFIRMED",
        "confidence": "HIGH",
        "value_usd": 100.0,
        "network_cost_usd": 0.25,
        "market_price_usd": 3000.0,
    }

    telegraph_intelligence = {
        "request_id": "phase-10.4-test",
        "generated_at": "2026-08-28T00:00:00+00:00",
        "routes": {},
    }

    result = build_decision_input(
        intelligence=intelligence,
        telegraph_intelligence=telegraph_intelligence,
    )

    assert "decision" not in result
    assert "recommendation" not in result
    assert "eligible" not in result
    assert "settlement_decision" not in result
