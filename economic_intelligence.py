from real_transaction import get_transaction_facts
from real_route_source import get_real_eth_price
from transaction_cost import get_transaction_cost


def build_economic_intelligence(payment_intent):

    if not isinstance(payment_intent, dict):
        raise ValueError(
            "PaymentIntent must be a dictionary"
        )

    transaction = payment_intent.get(
        "transaction",
        {}
    )

    user_amount = transaction.get("amount")
    source_currency = transaction.get(
        "source_currency"
    )

    if user_amount is None:
        raise ValueError(
            "PaymentIntent transaction amount is required"
        )

    if not source_currency:
        raise ValueError(
            "PaymentIntent source currency is required"
        )

    if source_currency != "USD":
        raise ValueError(
            "USD economic normalization is currently "
            "required; FX intelligence is not yet enabled"
        )

    if user_amount <= 0:
        raise ValueError(
            "PaymentIntent amount must be greater than zero"
        )

    transaction_facts = get_transaction_facts()

    market = get_real_eth_price()

    if market["status"] != "REAL":
        return {
            "status": "UNKNOWN",
            "reason": "MARKET_DATA_UNAVAILABLE",
            "confidence": 0.0,
            "user_transaction_amount": user_amount,
            "user_transaction_currency": source_currency,
        }

    cost = get_transaction_cost()

    # User/business transaction value.
    # This is the amount requested by the PaymentIntent.
    user_transaction_value_usd = user_amount

    # Observed blockchain transaction value.
    # This is intelligence about the transaction observed through
    # Base RPC and CoinGecko. It is NOT the user's requested amount.
    eth_amount = transaction_facts["value_eth"]
    eth_price = market["value"]

    observed_transaction_value_usd = (
        eth_amount * eth_price
    )

    return {
        "status": "REAL",

        # User/business transaction
        "user_transaction_amount": user_amount,
        "user_transaction_currency": source_currency,
        "user_transaction_value_usd":
            user_transaction_value_usd,

        # Observed blockchain transaction
        "asset": "ETH",
        "network": transaction_facts["network"],
        "chain_id": transaction_facts["chain_id"],
        "transaction_status":
            transaction_facts["status"],
        "transaction_confidence":
            transaction_facts["confidence"],
        "observed_transaction_value_eth":
            eth_amount,
        "observed_transaction_value_usd":
            observed_transaction_value_usd,
        "eth_price_usd": eth_price,

        # Real network economics
        "network_cost_usd":
            cost["total_network_cost_usd"],
        "gas_used": cost["gas_used"],
        "effective_gas_price_wei":
            cost["effective_gas_price_wei"],
        "l1_fee_wei":
            cost["l1_fee_wei"],

        "source": "Base RPC + CoinGecko",
        "confidence": 1.0,
    }


if __name__ == "__main__":

    from user_business_input import (
        build_user_business_input,
        validate_user_business_input,
    )

    user_input = build_user_business_input(
        amount=1000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="Brazilian supplier",
        source_jurisdiction="India",
        destination_jurisdiction="Brazil",
        constraints={
            "purpose": "import_payment"
        },
    )

    payment_intent = validate_user_business_input(
        user_input
    )

    economic = build_economic_intelligence(
        payment_intent
    )

    print(
        "=== NORMALIZED ECONOMIC INTELLIGENCE ==="
    )

    for key, value in economic.items():
        print(f"{key}: {value}")
