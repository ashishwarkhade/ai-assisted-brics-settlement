from datetime import datetime, timezone
from uuid import uuid4


# ============================================================
# PAYMENT INTENT STATUS
# ============================================================

PAYMENT_INTENT_STATUS = (
    "DRAFT",
    "VALIDATED",
    "INCOMPLETE",
    "INVALID",
)


# ============================================================
# BUILD PAYMENT INTENT
# ============================================================

def build_payment_intent(
    amount,
    source_currency,
    destination_currency,
    counterparty,
    settlement_asset=None,
    settlement_network=None,
    max_cost=None,
    max_settlement_time=None,
    risk_tolerance=None,
    constraints=None,
):
    """
    Build the canonical payment intent.

    PaymentIntent describes what the user wants to accomplish.
    It does not recommend a settlement route.
    """

    intent = {
        "intent_id": str(uuid4()),

        "transaction": {
            "amount": amount,
            "source_currency": source_currency,
            "destination_currency": destination_currency,
        },

        "counterparty": {
            "identifier": counterparty,
        },

        "settlement_preferences": {
            "asset": settlement_asset,
            "network": settlement_network,
            "max_cost": max_cost,
            "max_settlement_time": max_settlement_time,
        },

        "risk_constraints": {
            "risk_tolerance": risk_tolerance,
        },

        "constraints": constraints or {},

        "metadata": {
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),

            "status": "DRAFT",
        },
    }

    return intent


# ============================================================
# VALIDATE PAYMENT INTENT
# ============================================================

def validate_payment_intent(intent):
    """
    Validate the minimum information required to evaluate
    a payment request.

    This function does not select a route.
    """

    if not isinstance(intent, dict):
        raise ValueError(
            "PaymentIntent must be a dictionary"
        )

    transaction = intent.get("transaction", {})
    counterparty = intent.get("counterparty", {})

    required_fields = {
        "amount": transaction.get("amount"),
        "source_currency":
            transaction.get("source_currency"),
        "destination_currency":
            transaction.get("destination_currency"),
        "counterparty":
            counterparty.get("identifier"),
    }

    missing = [
        field
        for field, value in required_fields.items()
        if value is None
        or value == ""
    ]

    if missing:

        intent["metadata"]["status"] = "INCOMPLETE"

        intent["metadata"]["missing_fields"] = missing

        return intent

    if transaction["amount"] <= 0:

        intent["metadata"]["status"] = "INVALID"

        intent["metadata"]["validation_error"] = (
            "amount must be greater than zero"
        )

        return intent

    intent["metadata"]["status"] = "VALIDATED"

    intent["metadata"].pop(
        "missing_fields",
        None,
    )

    intent["metadata"].pop(
        "validation_error",
        None,
    )

    return intent


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    intent = build_payment_intent(
        amount=50000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="counterparty-A",
    )

    intent = validate_payment_intent(intent)

    print("=== PAYMENT INTENT ===")

    for key, value in intent.items():

        print(f"{key}: {value}")
