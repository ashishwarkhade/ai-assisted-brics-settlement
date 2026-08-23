from real_transaction import get_transaction_facts
from real_route_source import get_real_eth_price
from transaction_cost import get_transaction_cost


def build_economic_intelligence():

    transaction = get_transaction_facts()

    market = get_real_eth_price()

    if market["status"] != "REAL":
        return {
            "status": "UNKNOWN",
            "reason": "MARKET_DATA_UNAVAILABLE",
            "confidence": 0.0,
        }

    cost = get_transaction_cost()

    eth_amount = transaction["value_eth"]
    eth_price = market["value"]

    transaction_value_usd = eth_amount * eth_price

    return {
        "status": "REAL",
        "asset": "ETH",
        "network": transaction["network"],
        "chain_id": transaction["chain_id"],
        "transaction_status": transaction["status"],
        "transaction_confidence": transaction["confidence"],
        "transaction_value_eth": eth_amount,
        "transaction_value_usd": transaction_value_usd,
        "eth_price_usd": eth_price,
        "network_cost_usd": cost["total_network_cost_usd"],
        "gas_used": cost["gas_used"],
        "effective_gas_price_wei": cost[
            "effective_gas_price_wei"
        ],
        "l1_fee_wei": cost["l1_fee_wei"],
        "source": "Base RPC + CoinGecko",
        "confidence": 1.0,
    }


if __name__ == "__main__":

    economic = build_economic_intelligence()

    print("=== NORMALIZED ECONOMIC INTELLIGENCE ===")

    for key, value in economic.items():
        print(f"{key}: {value}")