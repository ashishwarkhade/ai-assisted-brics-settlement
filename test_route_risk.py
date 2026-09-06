import pytest

from route_risk import (
    calculate_route_risk,
    build_route_risk_model,
)


def build_bitcoin_route():

    return {
        "route": "Bitcoin",
        "asset": "BTC",
        "network": "Bitcoin",

        "network_metric": {
            "name": "fee_rate",
            "value": 10,
            "unit": "sat/vB",
            "status": "REAL",
            "source": "mempool.space",
            "confidence": 1.0,
        },

        "cost": {
            "value": 0.25,
            "currency": "USD",
            "status": "REAL_OBSERVED",
            "source": "mempool.space",
            "confidence": 1.0,
        },

        "settlement_time": {
            "value": None,
            "unit": "minutes",
            "status": "NOT_CALCULATED",
            "source": "Bitcoin network",
            "confidence": 0.0,
        },
    }


def build_base_route():

    return {
        "route": "Base",
        "asset": "ETH",
        "network": "Base",

        "network_metric": {
            "name": "gas_price",
            "value": 1000000000,
            "unit": "wei",
            "status": "REAL",
            "source": "Base RPC",
            "confidence": 1.0,
        },

        "market": {
            "asset": "ETH",
            "price_usd": 4500.0,
            "status": "REAL",
            "source": "CoinGecko",
            "confidence": 1.0,
        },

        "cost": {
            "value": 0.001,
            "currency": "USD",
            "status": "REAL_OBSERVED",
            "source": "Base RPC + CoinGecko",
            "confidence": 1.0,
        },

        "settlement_time": {
            "value": None,
            "unit": "minutes",
            "status": "NOT_CALCULATED",
            "source": "Base network",
            "confidence": 0.0,
        },
    }


# ============================================================
# BASIC RISK CALCULATION
# ============================================================

def test_bitcoin_route_risk():

    route = build_bitcoin_route()

    risk = calculate_route_risk(route)

    assert risk["value"] == 50

    assert (
        risk["source"]
        == "DETERMINISTIC_ROUTE_RISK_MODEL"
    )

    assert (
        risk["source_type"]
        == "CALCULATED"
    )

    assert risk["confidence"] == 1.0


def test_base_route_risk():

    route = build_base_route()

    risk = calculate_route_risk(route)

    assert risk["value"] == 40

    assert (
        risk["source"]
        == "DETERMINISTIC_ROUTE_RISK_MODEL"
    )


# ============================================================
# COMPONENT VALIDATION
# ============================================================

def test_bitcoin_risk_components():

    risk = calculate_route_risk(
        build_bitcoin_route()
    )

    components = risk["components"]

    assert components["network"]["value"] == 10

    assert components["cost_data"]["value"] == 5

    assert (
        components["settlement_time"]["value"]
        == 20
    )

    assert (
        components["market_data"]["value"]
        == 15
    )


def test_base_risk_components():

    risk = calculate_route_risk(
        build_base_route()
    )

    components = risk["components"]

    assert components["network"]["value"] == 10

    assert components["cost_data"]["value"] == 5

    assert (
        components["settlement_time"]["value"]
        == 20
    )

    assert (
        components["market_data"]["value"]
        == 5
    )


# ============================================================
# UNKNOWN DATA MUST INCREASE RISK
# ============================================================

def test_unknown_network_data_increases_risk():

    route = build_base_route()

    route["network_metric"]["status"] = (
        "UNKNOWN"
    )

    risk = calculate_route_risk(route)

    assert (
        risk["components"]["network"]["value"]
        == 30
    )


def test_unknown_cost_data_increases_risk():

    route = build_base_route()

    route["cost"]["value"] = None
    route["cost"]["status"] = "UNKNOWN"

    risk = calculate_route_risk(route)

    assert (
        risk["components"]["cost_data"]["value"]
        == 25
    )


def test_unknown_settlement_time_increases_risk():

    route = build_base_route()

    route["settlement_time"]["value"] = None
    route["settlement_time"]["status"] = (
        "NOT_CALCULATED"
    )

    risk = calculate_route_risk(route)

    assert (
        risk["components"]["settlement_time"]["value"]
        == 20
    )


def test_missing_market_data_increases_risk():

    route = build_base_route()

    del route["market"]

    risk = calculate_route_risk(route)

    assert (
        risk["components"]["market_data"]["value"]
        == 15
    )


# ============================================================
# COMPLETE DATA
# ============================================================

def test_complete_route_has_lower_risk():

    route = build_base_route()

    route["settlement_time"] = {
        "value": 1,
        "unit": "minutes",
        "status": "REAL",
        "source": "Base network",
        "confidence": 1.0,
    }

    risk = calculate_route_risk(route)

    assert risk["value"] == 25

    assert (
        risk["components"]["settlement_time"]["value"]
        == 5
    )


# ============================================================
# INPUT VALIDATION
# ============================================================

def test_invalid_route_type():

    with pytest.raises(
        ValueError,
        match="route must be a dictionary",
    ):

        calculate_route_risk(None)


def test_missing_network_metric():

    route = build_base_route()

    del route["network_metric"]

    with pytest.raises(
        ValueError,
        match="route.network_metric is required",
    ):

        calculate_route_risk(route)


def test_missing_cost():

    route = build_base_route()

    del route["cost"]

    with pytest.raises(
        ValueError,
        match="route.cost is required",
    ):

        calculate_route_risk(route)


# ============================================================
# REGULATORY / POLICY SEPARATION
# ============================================================

def test_regulatory_fields_do_not_change_route_risk():

    route = build_base_route()

    baseline = calculate_route_risk(
        route
    )["value"]

    route["regulatory_state"] = "PROHIBITED"

    route["compliance"] = {
        "value": "BLOCKED",
        "source": "TEST",
        "source_type": "TEST",
        "confidence": 1.0,
    }

    route["geopolitical_status"] = {
        "value": "RESTRICTED",
        "source": "TEST",
        "source_type": "TEST",
        "confidence": 1.0,
    }

    modified = calculate_route_risk(
        route
    )["value"]

    assert modified == baseline


# ============================================================
# BUILD ALL ROUTE RISKS
# ============================================================

def test_build_route_risk_model():

    routes = {
        "bitcoin": build_bitcoin_route(),
        "base": build_base_route(),
    }

    risks = build_route_risk_model(
        routes
    )

    assert "bitcoin" in risks

    assert "base" in risks

    assert (
        risks["bitcoin"]["value"]
        == 50
    )

    assert (
        risks["base"]["value"]
        == 40
    )


def test_build_route_risk_model_requires_dictionary():

    with pytest.raises(
        ValueError,
        match="normalized_routes must be a dictionary",
    ):

        build_route_risk_model(None)
