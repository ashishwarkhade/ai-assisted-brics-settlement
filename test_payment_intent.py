from payment_intent import (
    build_payment_intent,
    validate_payment_intent,
)


def test_valid_payment_intent():

    intent = build_payment_intent(
        amount=50000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="counterparty-A",
    )

    intent = validate_payment_intent(intent)

    assert intent["metadata"]["status"] == "VALIDATED"

    assert intent["transaction"]["amount"] == 50000

    assert (
        intent["transaction"]["source_currency"]
        == "USD"
    )

    assert (
        intent["transaction"]["destination_currency"]
        == "USD"
    )

    assert (
        intent["counterparty"]["identifier"]
        == "counterparty-A"
    )


def test_missing_amount():

    intent = build_payment_intent(
        amount=None,
        source_currency="USD",
        destination_currency="USD",
        counterparty="counterparty-A",
    )

    intent = validate_payment_intent(intent)

    assert intent["metadata"]["status"] == "INCOMPLETE"

    assert "amount" in intent["metadata"]["missing_fields"]


def test_missing_counterparty():

    intent = build_payment_intent(
        amount=50000,
        source_currency="USD",
        destination_currency="USD",
        counterparty=None,
    )

    intent = validate_payment_intent(intent)

    assert intent["metadata"]["status"] == "INCOMPLETE"

    assert (
        "counterparty"
        in intent["metadata"]["missing_fields"]
    )


def test_invalid_amount():

    intent = build_payment_intent(
        amount=0,
        source_currency="USD",
        destination_currency="USD",
        counterparty="counterparty-A",
    )

    intent = validate_payment_intent(intent)

    assert intent["metadata"]["status"] == "INVALID"


def test_optional_constraints_are_preserved():

    intent = build_payment_intent(
        amount=50000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="counterparty-A",
        settlement_asset="USDC",
        settlement_network="Base",
        max_cost=100,
        max_settlement_time=10,
        risk_tolerance="LOW",
    )

    intent = validate_payment_intent(intent)

    assert intent["metadata"]["status"] == "VALIDATED"

    assert (
        intent["settlement_preferences"]["asset"]
        == "USDC"
    )

    assert (
        intent["settlement_preferences"]["network"]
        == "Base"
    )

    assert (
        intent["settlement_preferences"]["max_cost"]
        == 100
    )

    assert (
        intent["settlement_preferences"]["max_settlement_time"]
        == 10
    )

    assert (
        intent["risk_constraints"]["risk_tolerance"]
        == "LOW"
    )
