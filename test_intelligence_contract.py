from intelligence_contract import (
    build_intelligence_evidence,
    build_route_intelligence_contract,
    build_normalized_intelligence,
    is_usable,
)


def test_available_valid_evidence_is_usable():

    evidence = build_intelligence_evidence(
        metric="eth_usd",
        value=4500,
        unit="USD",
        source="CoinGecko",
        timestamp="2026-08-27T11:30:00+00:00",
        status="AVAILABLE",
        confidence="HIGH",
        validation="VALID",
    )

    assert is_usable(evidence) is True


def test_unknown_value_is_not_usable():

    evidence = build_intelligence_evidence(
        metric="bitcoin_transaction_cost",
        value=None,
        unit="USD",
        source="mempool.space",
        timestamp="2026-08-27T11:30:00+00:00",
        status="UNAVAILABLE",
        confidence="HIGH",
        validation="VALID",
    )

    assert is_usable(evidence) is False


def test_unvalidated_evidence_is_not_usable():

    evidence = build_intelligence_evidence(
        metric="base_gas_price",
        value=1000000,
        unit="wei",
        source="Base RPC",
        timestamp="2026-08-27T11:30:00+00:00",
        status="AVAILABLE",
        confidence="HIGH",
        validation="NOT_VALIDATED",
    )

    assert is_usable(evidence) is False


def test_stale_evidence_is_not_usable():

    evidence = build_intelligence_evidence(
        metric="eth_usd",
        value=4500,
        unit="USD",
        source="CoinGecko",
        timestamp="2026-08-20T11:30:00+00:00",
        status="STALE",
        confidence="HIGH",
        validation="VALID",
    )

    assert is_usable(evidence) is False


def test_invalid_status_is_rejected():

    try:

        build_intelligence_evidence(
            metric="eth_usd",
            value=4500,
            unit="USD",
            source="CoinGecko",
            timestamp="2026-08-27T11:30:00+00:00",
            status="REAL",
            confidence="HIGH",
            validation="VALID",
        )

    except ValueError:
        return

    assert False, "Expected ValueError"


def test_route_contract():

    evidence = build_intelligence_evidence(
        metric="fee_rate",
        value=12,
        unit="sat/vB",
        source="mempool.space",
        timestamp="2026-08-27T11:30:00+00:00",
        status="AVAILABLE",
        confidence="HIGH",
        validation="VALID",
    )

    route = build_route_intelligence_contract(
        route_id="bitcoin",
        asset="BTC",
        network="Bitcoin",
        evidence=[evidence],
    )

    assert route["route_id"] == "bitcoin"
    assert route["asset"] == "BTC"
    assert len(route["evidence"]) == 1


def test_normalized_intelligence():

    normalized = build_normalized_intelligence(
        request_id="test-request",
        generated_at="2026-08-27T11:30:00+00:00",
        routes={},
    )

    assert normalized["request_id"] == "test-request"
    assert normalized["routes"] == {}
