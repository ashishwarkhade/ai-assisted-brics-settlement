# Real-world transaction adapter


def wei_to_eth(value_wei):
    return value_wei / 10**18
def get_transaction_facts():
    """
    Convert external blockchain intelligence
    into our project's standard format.
    """

    raw_transaction = {
        "chain": "base",
        "chain_id": 8453,
        "status": "confirmed_success",
        "confidence": 1,
        "value_wei": 50900000000000000,
    }

    # Our normalized internal representation
    transaction = {
        "type": "transaction",
        "asset": "ETH",
        "network": raw_transaction["chain"],
        "chain_id": raw_transaction["chain_id"],
        "status": raw_transaction["status"],
        "confidence": raw_transaction["confidence"],
        "value_wei": raw_transaction["value_wei"],
        "value_eth": wei_to_eth(raw_transaction["value_wei"])
    }

    return transaction


if __name__ == "__main__":

    transaction = get_transaction_facts()

    print("=== NORMALIZED TRANSACTION ===")
    print(f"Type: {transaction['type']}")
    print(f"Asset: {transaction['asset']}")
    print(f"Network: {transaction['network']}")
    print(f"Chain ID: {transaction['chain_id']}")
    print(f"Status: {transaction['status']}")
    print(f"Confidence: {transaction['confidence']}")
    print(f"Value: {transaction['value_wei']} wei")
    print(f"Value: {transaction['value_wei']} wei")
    print(f"Value: {transaction['value_eth']} ETH")
