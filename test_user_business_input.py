from user_business_input import (
    build_user_business_input,
    build_payment_intent_from_user_business_input,
    validate_user_business_input,
)


def test_user_business_input_builds():

    user_input = build_user_business_input(
        amount=1000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="Brazilian supplier",
        source_jurisdiction="India",
        destination_jurisdiction="Brazil",
    )

    assert (
        user_input["transaction"]["amount"]
        == 1000
    )

    assert (
        user_input["corridor"]["source_jurisdiction"]
        == "India"
    )

    assert (
        user_input["corridor"]["destination_jurisdiction"]
        == "Brazil"
    )

    assert (
        user_input["counterparty"]
        == "Brazilian supplier"
    )


def test_user_business_input_creates_payment_intent():

    user_input = build_user_business_input(
        amount=1000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="Brazilian supplier",
        source_jurisdiction="India",
        destination_jurisdiction="Brazil",
    )

    intent = (
        build_payment_intent_from_user_business_input(
            user_input
        )
    )

    assert (
        intent["transaction"]["amount"]
        == 1000
    )

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
        == "Brazilian supplier"
    )

    assert (
        intent["corridor"]["source_jurisdiction"]
        == "India"
    )

    assert (
        intent["corridor"]["destination_jurisdiction"]
        == "Brazil"
    )


def test_user_business_input_validation():

    user_input = build_user_business_input(
        amount=1000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="Brazilian supplier",
        source_jurisdiction="India",
        destination_jurisdiction="Brazil",
    )

    intent = validate_user_business_input(
        user_input
    )

    assert (
        intent["metadata"]["status"]
        == "VALIDATED"
    )


def test_user_business_input_does_not_select_route():

    user_input = build_user_business_input(
        amount=1000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="Brazilian supplier",
        source_jurisdiction="India",
        destination_jurisdiction="Brazil",
    )

    intent = validate_user_business_input(
        user_input
    )

    assert (
        intent["settlement_preferences"]["asset"]
        is None
    )

    assert (
        intent["settlement_preferences"]["network"]
        is None
    )


def test_optional_user_constraints_are_preserved():

    user_input = build_user_business_input(
        amount=1000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="Brazilian supplier",
        source_jurisdiction="India",
        destination_jurisdiction="Brazil",
        max_cost=25,
        max_settlement_time=30,
        risk_tolerance="LOW",
        constraints={
            "purpose": "import_payment"
        },
    )

    intent = validate_user_business_input(
        user_input
    )

    assert (
        intent["metadata"]["status"]
        == "VALIDATED"
    )

    assert (
        intent["settlement_preferences"]["max_cost"]
        == 25
    )

    assert (
        intent["settlement_preferences"][
            "max_settlement_time"
        ]
        == 30
    )

    assert (
        intent["risk_constraints"]["risk_tolerance"]
        == "LOW"
    )

    assert (
        intent["constraints"]["purpose"]
        == "import_payment"
    )
