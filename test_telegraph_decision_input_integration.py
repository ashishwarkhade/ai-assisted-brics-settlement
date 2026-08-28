from decision_input import build_decision_input
from telegraph_intelligence_adapter import (
    normalize_telegraph_trade_context,
)


def test_telegraph_normalized_intelligence_can_enter_decision_input():

    trade_context = {
        "fear_greed": {
            "classification": "Greed",
            "source": "alternative.me",
            "timestamp": 1787788800,
            "value": 71,
        },

        "funding": {
            "btc": {
                "funding_rate_8h_equiv": 0.0001,
                "funding_rate_hourly": 0.0000125,
                "funding_rate_pct_hourly": 0.00125,
                "mark_price": 79279,
                "open_interest": 37784.00964,
                "source": "hyperliquid",
                "symbol": "BTC",
            },

            "sol": {
                "funding_rate_8h_equiv": 0.0001,
                "funding_rate_hourly": 0.0000125,
                "funding_rate_pct_hourly": 0.00125,
                "mark_price": 104.53,
                "open_interest": 6403203.28,
                "source": "hyperliquid",
                "symbol": "SOL",
            },
        },

        "liquidations": {
            "btc": {
                "1h": {
                    "events": 16,
                    "total_usd": 142134.53,
                    "longs_liquidated_usd": 138875.77,
                    "shorts_liquidated_usd": 3258.76,
                    "biggest_print_usd": 52671.14,
                    "by_exchange": {},
                },

                "24h": {
                    "events": 2458,
                    "total_usd": 18409365.30,
                    "longs_liquidated_usd": 3669372.93,
                    "shorts_liquidated_usd": 14739992.37,
                    "biggest_print_usd": 3020585.75,
                    "by_exchange": {},
                },
            },

            "sol": {
                "1h": {
                    "events": 1,
                    "total_usd": 1.0,
                    "longs_liquidated_usd": 0.5,
                    "shorts_liquidated_usd": 0.5,
                    "biggest_print_usd": 1.0,
                    "by_exchange": {},
                },

                "24h": {
                    "events": 1,
                    "total_usd": 1.0,
                    "longs_liquidated_usd": 0.5,
                    "shorts_liquidated_usd": 0.5,
                    "biggest_print_usd": 1.0,
                    "by_exchange": {},
                },
            },

            "source": "multi_exchange_collector",
        },

        "positioning": {
            "btc": {
                "long_short_ratio": {
                    "long_pct": 53.34,
                    "long_pct_prev_hour": 53.29,
                    "short_pct": 46.66,
                    "ts": 1787835600000,
                },

                "open_interest": {
                    "base": 48941.699,
                    "change_1h_pct": -0.05,
                    "change_24h_pct": 4.06,
                    "usd": 3885372188,
                },
            },

            "sol": {
                "long_short_ratio": {
                    "long_pct": 67.37,
                    "long_pct_prev_hour": 67.47,
                    "short_pct": 32.63,
                    "ts": 1787835600000,
                },

                "open_interest": {
                    "base": 7348794.1,
                    "change_1h_pct": 0.67,
                    "change_24h_pct": 15.55,
                    "usd": 768626135,
                },
            },

            "period": "1h",
            "source": "bybit_v5_public",
        },

        "prices": {
            "btc": {
                "confidence": None,
                "price": 79303.41,
                "publish_time": None,
                "source": "coinbase",
                "symbol": "BTC",
            },

            "sol": {
                "confidence": None,
                "price": 104.52,
                "publish_time": None,
                "source": "coinbase",
                "symbol": "SOL",
            },
        },

        "ts": 1787836306181,
    }

    transaction_intelligence = {
        "asset": "ETH",
        "network": "Base",
        "chain_id": 8453,
        "status": "CONFIRMED",
        "confidence": "HIGH",
        "value_usd": 1000.0,
        "network_cost_usd": 0.25,
        "market_price_usd": 3000.0,
    }

    telegraph_intelligence = (
        normalize_telegraph_trade_context(
            trade_context,
            request_id="phase-10.4-integration",
        )
    )

    decision_input = build_decision_input(
        intelligence=transaction_intelligence,
        telegraph_intelligence=telegraph_intelligence,
    )

    assert (
        decision_input["telegraph_intelligence"]
        == telegraph_intelligence
    )

    assert (
        decision_input["telegraph_intelligence"]
        ["request_id"]
        == "phase-10.4-integration"
    )

    assert (
        set(
            decision_input[
                "telegraph_intelligence"
            ]["routes"].keys()
        )
        == {"bitcoin", "solana"}
    )


def test_decision_input_remains_decision_free():

    transaction_intelligence = {
        "asset": "ETH",
        "network": "Base",
        "chain_id": 8453,
        "status": "CONFIRMED",
        "confidence": "HIGH",
        "value_usd": 1000.0,
        "network_cost_usd": 0.25,
        "market_price_usd": 3000.0,
    }

    telegraph_intelligence = {
        "request_id": "test",
        "generated_at": "2026-08-28T00:00:00+00:00",
        "routes": {},
    }

    decision_input = build_decision_input(
        intelligence=transaction_intelligence,
        telegraph_intelligence=telegraph_intelligence,
    )

    forbidden = {
        "decision",
        "recommendation",
        "eligible",
        "settlement_decision",
        "settlement_recommendation",
    }

    assert forbidden.isdisjoint(
        decision_input.keys()
    )
