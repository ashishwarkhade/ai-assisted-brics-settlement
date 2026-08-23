def build_decision_input(intelligence):
    """
    Convert normalized transaction intelligence
    into a provider-independent decision input.
    """

    return {
        "asset": intelligence["asset"],
        "network": intelligence["network"],
        "chain_id": intelligence["chain_id"],

        "transaction_status": intelligence["status"],
        "confidence": intelligence["confidence"],

        "transaction_value_usd": intelligence["value_usd"],
        "network_cost_usd": intelligence["network_cost_usd"],

        "economic_data": {
            "asset_price_usd": intelligence["market_price_usd"],
            "network_cost_usd": intelligence["network_cost_usd"],
        }
    }


if __name__ == "__main__":

    from transaction_intelligence import build_transaction_intelligence

    intelligence = build_transaction_intelligence()

    decision_input = build_decision_input(intelligence)

    print("=== DECISION INPUT ===")

    for key, value in decision_input.items():
        print(f"{key}: {value}")
