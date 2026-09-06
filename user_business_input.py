"""
USER / BUSINESS INPUT LAYER

Purpose:
    Convert structured user/business transaction information
    into the canonical PaymentIntent.

Architecture:

    User / Business
          ↓
    UserBusinessInput
          ↓
    PaymentIntent
          ↓
    Validation
          ↓
    DecisionInput
          ↓
    Intelligence
          ↓
    Deterministic Settlement Decision

Authority boundary:

    This module describes what the user/business wants.
    It does not:
        - select a settlement route
        - select an asset
        - select a network
        - determine regulatory approval
        - determine compliance
        - determine risk
        - rank routes
        - make a settlement recommendation
"""


from payment_intent import (
    build_payment_intent,
    validate_payment_intent,
)


# ============================================================
# USER / BUSINESS INPUT STATUS
# ============================================================

USER_BUSINESS_INPUT_STATUS = (
    "DRAFT",
    "VALIDATED",
    "INCOMPLETE",
    "INVALID",
)


# ============================================================
# BUILD USER / BUSINESS INPUT
# ============================================================

def build_user_business_input(
    amount,
    source_currency,
    destination_currency,
    counterparty,
    source_jurisdiction=None,
    destination_jurisdiction=None,
    settlement_asset=None,
    settlement_network=None,
    max_cost=None,
    max_settlement_time=None,
    risk_tolerance=None,
    constraints=None,
):
    """
    Build a structured User/Business input.

    The resulting structure is converted directly into the
    canonical PaymentIntent.

    User/business input expresses transaction intent only.
    No settlement route is selected here.
    """

    user_business_input = {
        "transaction": {
            "amount": amount,
            "source_currency": source_currency,
            "destination_currency": destination_currency,
        },

        "counterparty": counterparty,

        "corridor": {
            "source_jurisdiction": source_jurisdiction,
            "destination_jurisdiction": destination_jurisdiction,
        },

        "settlement_preferences": {
            "asset": settlement_asset,
            "network": settlement_network,
            "max_cost": max_cost,
            "max_settlement_time": max_settlement_time,
        },

        "risk_tolerance": risk_tolerance,

        "constraints": constraints or {},
    }

    return user_business_input


# ============================================================
# CONVERT USER / BUSINESS INPUT → PAYMENT INTENT
# ============================================================

def build_payment_intent_from_user_business_input(
    user_business_input,
):
    """
    Convert User/Business input into the canonical PaymentIntent.

    This function does not perform route selection.
    """

    if not isinstance(user_business_input, dict):
        raise ValueError(
            "User/Business input must be a dictionary"
        )

    transaction = user_business_input.get(
        "transaction",
        {},
    )

    counterparty = user_business_input.get(
        "counterparty"
    )

    corridor = user_business_input.get(
        "corridor",
        {},
    )

    settlement_preferences = (
        user_business_input.get(
            "settlement_preferences",
            {},
        )
    )

    payment_intent = build_payment_intent(
        amount=transaction.get("amount"),

        source_currency=transaction.get(
            "source_currency"
        ),

        destination_currency=transaction.get(
            "destination_currency"
        ),

        counterparty=counterparty,

        settlement_asset=(
            settlement_preferences.get("asset")
        ),

        settlement_network=(
            settlement_preferences.get("network")
        ),

        max_cost=(
            settlement_preferences.get("max_cost")
        ),

        max_settlement_time=(
            settlement_preferences.get(
                "max_settlement_time"
            )
        ),

        risk_tolerance=(
            user_business_input.get(
                "risk_tolerance"
            )
        ),

        constraints=(
            user_business_input.get(
                "constraints",
                {},
            )
        ),

        source_jurisdiction=(
            corridor.get(
                "source_jurisdiction"
            )
        ),

        destination_jurisdiction=(
            corridor.get(
                "destination_jurisdiction"
            )
        ),
    )

    return payment_intent


# ============================================================
# VALIDATE USER / BUSINESS INPUT
# ============================================================

def validate_user_business_input(
    user_business_input,
):
    """
    Convert and validate User/Business input.

    Validation is delegated to the canonical PaymentIntent
    validator so there is only one validation contract.
    """

    payment_intent = (
        build_payment_intent_from_user_business_input(
            user_business_input
        )
    )

    payment_intent = validate_payment_intent(
        payment_intent
    )

    return payment_intent


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # REAL USER / BUSINESS REQUEST
    # --------------------------------------------------------

    user_business_input = (
        build_user_business_input(
            amount=1000,
            source_currency="USD",
            destination_currency="USD",
            counterparty="Brazilian supplier",
            source_jurisdiction="India",
            destination_jurisdiction="Brazil",
        )
    )

    # --------------------------------------------------------
    # CONVERT + VALIDATE
    # --------------------------------------------------------

    payment_intent = (
        validate_user_business_input(
            user_business_input
        )
    )

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    print("=== USER / BUSINESS INPUT ===")

    print(
        f"Amount: "
        f"{user_business_input['transaction']['amount']}"
    )

    print(
        "Source jurisdiction: "
        f"{user_business_input['corridor']['source_jurisdiction']}"
    )

    print(
        "Destination jurisdiction: "
        f"{user_business_input['corridor']['destination_jurisdiction']}"
    )

    print(
        "Counterparty: "
        f"{user_business_input['counterparty']}"
    )

    print()

    print("=== PAYMENT INTENT ===")

    print(
        f"Intent ID: "
        f"{payment_intent['intent_id']}"
    )

    print(
        f"Status: "
        f"{payment_intent['metadata']['status']}"
    )

    print(
        f"Amount: "
        f"{payment_intent['transaction']['amount']}"
    )

    print(
        "Source jurisdiction: "
        f"{payment_intent['corridor']['source_jurisdiction']}"
    )

    print(
        "Destination jurisdiction: "
        f"{payment_intent['corridor']['destination_jurisdiction']}"
    )

    print(
        "Settlement asset: "
        f"{payment_intent['settlement_preferences']['asset']}"
    )

    print(
        "Settlement network: "
        f"{payment_intent['settlement_preferences']['network']}"
    )

    print()

    print(
        "User/Business → PaymentIntent: PASS"
    )

    print(
        "Route selection: NOT PERFORMED"
    )
