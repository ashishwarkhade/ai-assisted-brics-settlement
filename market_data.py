from real_route_source import get_real_eth_price
from real_transaction import get_transaction_facts


def calculate_usd_value(eth_amount, eth_price):
    return eth_amount * eth_price


if __name__ == "__main__":

    # Get real transaction data
    transaction = get_transaction_facts()

    # Get real market data
    market = get_real_eth_price()

    # Make sure market data is actually available
    if market["status"] != "REAL":
        print("=== REAL ECONOMIC INTELLIGENCE ===")
        print("Market data unavailable.")
        print(f"Status: {market['status']}")
        print(f"Reason: {market.get('reason', 'UNKNOWN')}")
        raise SystemExit(1)

    # Extract ETH amount from transaction
    eth_amount = transaction["value_eth"]

    # Calculate USD value
    usd_value = calculate_usd_value(
        eth_amount,
        market["value"]
    )

    print("=== REAL ECONOMIC INTELLIGENCE ===")
    print(f"Asset: {market['asset']}")
    print(f"ETH amount: {eth_amount}")
    print(f"ETH/USD: ${market['value']}")
    print(f"USD value: ${usd_value:.2f}")