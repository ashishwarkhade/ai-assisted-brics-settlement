import pytest

from decision_engine import DecisionEngine
from decision_input import build_decision_input


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
def decision_input(intelligence):
    return build_decision_input(
        intelligence
    )


@pytest.fixture
def normalized_routes():
    return {
        "base": {
            "route": "base",
            "asset": "ETH",
            "network": "Base",
            "cost": {
                "value": 0.25,
                "status": "CALCULATED",
            },
        },
        "bitcoin": {
            "route": "bitcoin",
            "asset": "BTC",
            "network": "Bitcoin",
            "cost": {
                "value": 1.25,
                "status": "CALCULATED",
            },
        },
    }

@pytest.fixture
def decision_input(intelligence):
    return build_decision_input(
        intelligence
    )


@pytest.fixture
def normalized_routes():
    return {
        "base": {
            "route": "base",
            "asset": "ETH",
            "network": "Base",
            "cost": {
                "value": 0.25,
                "status": "CALCULATED",
            },
        },
        "bitcoin": {
            "route": "bitcoin",
            "asset": "BTC",
            "network": "Bitcoin",
            "cost": {
                "value": 1.25,
                "status": "CALCULATED",
            },
        },
    }


@pytest.fixture
def policies():
    return {
        "Base": {
            "compliance": {
                "value": "ALLOWED",
                "source": "TEST",
                "source_type": "REFERENCE",
                "confidence": 1.0,
            },
            "geopolitical_status": {
                "value": "PERMITTED",
                "source": "TEST",
                "source_type": "REFERENCE",
                "confidence": 1.0,
            },
            "risk": {
                "value": 10,
                "source": "TEST",
                "source_type": "REFERENCE",
                "confidence": 1.0,
            },
        },
        "Bitcoin": {
            "compliance": {
                "value": "ALLOWED",
                "source": "TEST",
                "source_type": "REFERENCE",
                "confidence": 1.0,
            },
            "geopolitical_status": {
                "value": "PERMITTED",
                "source": "TEST",
                "source_type": "REFERENCE",
                "confidence": 1.0,
            },
            "risk": {
                "value": 10,
                "source": "TEST",
                "source_type": "REFERENCE",
                "confidence": 1.0,
            },
        },
    }

@pytest.fixture
def permitted_policy():
    policy = {
        "compliance": {
            "value": "ALLOWED",
            "source": "TEST",
            "source_type": "REFERENCE",
            "confidence": 1.0,
        },
        "geopolitical_status": {
            "value": "PERMITTED",
            "source": "TEST",
            "source_type": "REFERENCE",
            "confidence": 1.0,
        },
        "risk": {
            "value": 10,
            "source": "TEST",
            "source_type": "REFERENCE",
            "confidence": 1.0,
        },
    }

    return {
        "Base": policy,
        "Bitcoin": policy,
    }

@pytest.fixture
def regulatory_evidence():
    return {
        "jurisdiction": "TEST",
        "asset": "ETH",
        "activity": "SETTLEMENT",
        "status": "PERMITTED",
        "source": "TEST",
        "source_type": "REFERENCE",
        "confidence": 1.0,
        "evidence_text": "Test regulatory evidence",
    }


# ============================================================
# E.4.3 — ROUTE RANKING
# ============================================================

def test_rank_routes_returns_only_eligible_routes(
    normalized_routes,
):

    decisions = [
        {
            "route": normalized_routes["base"],
            "status": "ELIGIBLE",
            "reason": None,
        },

        {
            "route": normalized_routes["bitcoin"],
            "status": "ELIGIBLE_DATA_INCOMPLETE",
            "reason": "REGULATORY_STATUS_UNKNOWN",
        },
    ]

    engine = DecisionEngine()

    ranked_routes = engine.rank_routes(
        decisions
    )

    assert len(
        ranked_routes
    ) == 1

    assert (
        ranked_routes[0]["route"]
        == "base"
    )


def test_rank_routes_orders_by_lowest_cost(
    normalized_routes,
):

    decisions = [
        {
            "route": normalized_routes["base"],
            "status": "ELIGIBLE",
            "reason": None,
        },

        {
            "route": normalized_routes["bitcoin"],
            "status": "ELIGIBLE",
            "reason": None,
        },
    ]

    engine = DecisionEngine()

    ranked_routes = engine.rank_routes(
        decisions
    )

    assert [
        route["route"]
        for route in ranked_routes
    ] == [
        "base",
        "bitcoin",
    ]

    assert (
        ranked_routes[0]["cost"]["value"]
        == 0.25
    )

    assert (
        ranked_routes[1]["cost"]["value"]
        == 1.25
    )


def test_rejected_routes_are_not_ranked(
    normalized_routes,
):

    decisions = [
        {
            "route": normalized_routes["base"],
            "status": "REJECTED",
            "reason": "COMPLIANCE_BLOCKED",
        },

        {
            "route": normalized_routes["bitcoin"],
            "status": "ELIGIBLE",
            "reason": None,
        },
    ]

    engine = DecisionEngine()

    ranked_routes = engine.rank_routes(
        decisions
    )

    assert [
        route["route"]
        for route in ranked_routes
    ] == [
        "bitcoin",
    ]


def test_unknown_cost_routes_are_not_ranked():

    routes = {
        "base": {
            "route": "base",
            "asset": "ETH",
            "network": "Base",
            "cost": {
                "value": None,
                "status": "UNKNOWN",
            },
        },

        "bitcoin": {
            "route": "bitcoin",
            "asset": "BTC",
            "network": "Bitcoin",
            "cost": {
                "value": 1.25,
                "status": "CALCULATED",
            },
        },
    }

    decisions = [
        {
            "route": routes["base"],
            "status": "ELIGIBLE_DATA_INCOMPLETE",
            "reason": "ROUTE_COST_UNKNOWN",
        },

        {
            "route": routes["bitcoin"],
            "status": "ELIGIBLE",
            "reason": None,
        },
    ]

    engine = DecisionEngine()

    ranked_routes = engine.rank_routes(
        decisions
    )

    assert [
        route["route"]
        for route in ranked_routes
    ] == [
        "bitcoin",
    ]


# ============================================================
# E.4.3 — RECOMMENDATION
# ============================================================

def test_recommend_returns_cheapest_route(
    normalized_routes,
):

    ranked_routes = [
        normalized_routes["base"],
        normalized_routes["bitcoin"],
    ]

    engine = DecisionEngine()

    result = engine.recommend(
        ranked_routes
    )

    assert (
        result["recommendation"]
        == {
            "route": "base",
            "asset": "ETH",
            "network": "Base",
        }
    )

    assert (
        result["recommendation_reason"]
        is None
    )


def test_recommend_returns_no_recommendation_when_empty():

    engine = DecisionEngine()

    result = engine.recommend(
        []
    )

    assert (
        result["recommendation"]
        is None
    )

    assert (
        result["recommendation_reason"]
        == "NO_ROUTE_HAS_SUFFICIENT_POLICY_AND_COST_DATA"
    )


# ============================================================
# E.4.3 — DECIDE INTEGRATION
# ============================================================

def test_decide_includes_ranking_and_recommendation(
    decision_input,
    normalized_routes,
    permitted_policy,
    regulatory_evidence,
):

    engine = DecisionEngine()

    result = engine.decide(
        decision_input=
            decision_input,

        normalized_routes=
            normalized_routes,

        policies=
            permitted_policy,

        regulatory_state=
            "PERMITTED",

        regulatory_evidence=
            regulatory_evidence,
    )

    assert (
        result["status"]
        == "DECISION_EVALUATED"
    )

    assert (
        result["decision_made"]
        is True
    )

    assert "ranked_routes" in result

    assert "recommendation" in result

    assert (
        result["recommendation"]
        == {
            "route": "base",
            "asset": "ETH",
            "network": "Base",
        }
    )


def test_decide_makes_no_recommendation_when_regulatory_unknown(
    decision_input,
    normalized_routes,
    permitted_policy,
    regulatory_evidence,
):

    engine = DecisionEngine()

    result = engine.decide(
        decision_input=
            decision_input,

        normalized_routes=
            normalized_routes,

        policies=
            permitted_policy,

        regulatory_state=
            "UNKNOWN",

        regulatory_evidence=
            regulatory_evidence,
    )

    assert (
        result["ranked_routes"]
        == []
    )

    assert (
        result["recommendation"]
        is None
    )

    assert (
        result["recommendation_reason"]
        == "NO_ROUTE_HAS_SUFFICIENT_POLICY_AND_COST_DATA"
    )


def test_decision_engine_does_not_use_telegraph_for_ranking(
    decision_input,
    normalized_routes,
    permitted_policy,
    regulatory_evidence,
):

    decision_input[
        "telegraph_intelligence"
    ] = {
        "request_id":
            "phase-10.4-test",

        "routes": {
            "bitcoin": {
                "evidence": [
                    {
                        "metric": "special_provider_metric",
                        "value": 0.0,
                    }
                ]
            }
        },
    }

    engine = DecisionEngine()

    result = engine.decide(
        decision_input=
            decision_input,

        normalized_routes=
            normalized_routes,

        policies=
            permitted_policy,

        regulatory_state=
            "PERMITTED",

        regulatory_evidence=
            regulatory_evidence,
    )

    assert (
        result["recommendation"]["route"]
        == "base"
    )

    assert (
        result["ranked_routes"][0]["route"]
        == "base"
    )