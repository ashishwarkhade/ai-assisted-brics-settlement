

from bitcoin_route_source import (
    get_bitcoin_fee_intelligence,
    estimate_bitcoin_transaction_cost,
)
from evm_route_source import get_base_network_intelligence
from real_route_source import get_real_eth_price
from transaction_cost import get_transaction_cost


def build_bitcoin_route_intelligence():

    bitcoin = get_bitcoin_fee_intelligence()
    bitcoin_cost = estimate_bitcoin_transaction_cost()

    return {
        "route": "Bitcoin",
        "asset": "BTC",
        "network": "Bitcoin",

        "network_metric": {
            "name": "fee_rate",
            "value": bitcoin["fastest_fee"],
            "unit": bitcoin["unit"],
            "status": "REAL",
            "source": bitcoin["source"],
            "confidence": bitcoin["confidence"],
        },

        "cost": {
           "value": bitcoin_cost["value"],
           "currency": bitcoin_cost["currency"],
           "status": bitcoin_cost["status"],
           "source": bitcoin_cost["source"],
           "confidence": bitcoin_cost["confidence"],
        },

        "settlement_time": {
            "value": None,
            "unit": "minutes",
            "status": "NOT_CALCULATED",
            "source": "Bitcoin network",
            "confidence": 0.0,
        },

        "status": "REAL_NETWORK_DATA",
    }


def build_base_route_intelligence():

    base = get_base_network_intelligence()
    market = get_real_eth_price()
    transaction_cost = get_transaction_cost()

    return {
        "route": "Base",
        "asset": "ETH",
        "network": "Base",

        "network_metric": {
            "name": "gas_price",
            "value": base["gas_price_wei"],
            "unit": "wei",
            "status": "REAL",
            "source": base["source"],
            "confidence": base["confidence"],
        },

        "market": {
            "asset": market["asset"],
            "price_usd": market["value"],
            "status": market["status"],
            "source": market["source"],
            "confidence": market["confidence"],
        },

        "cost": {
            "value": transaction_cost["total_network_cost_usd"],
            "currency": "USD",
            "status": "REAL_OBSERVED",
            "source": "Base RPC + CoinGecko",
            "confidence": 1.0,
        },

        "settlement_time": {
            "value": None,
            "unit": "minutes",
            "status": "NOT_CALCULATED",
            "source": "Base network",
            "confidence": 0.0,
        },

        "status": "REAL_NETWORK_DATA",
    }


def build_route_intelligence():

    return {
        "bitcoin": build_bitcoin_route_intelligence(),
        "base": build_base_route_intelligence(),
    }


if __name__ == "__main__":

    routes = build_route_intelligence()

    print("=== NORMALIZED ROUTE INTELLIGENCE ===")

    for name, route in routes.items():

        print()
        print(f"Route: {route['route']}")
        print(f"Asset: {route['asset']}")
        print(f"Network: {route['network']}")

        metric = route["network_metric"]

        print()
        print("Network metric:")
        print(f"  Type: {metric['name']}")
        print(f"  Value: {metric['value']}")
        print(f"  Unit: {metric['unit']}")
        print(f"  Source: {metric['source']}")
        print(f"  Status: {metric['status']}")
        print(f"  Confidence: {metric['confidence']}")

        if "market" in route:

            market = route["market"]

            print()
            print("Market:")
            print(f"  Asset: {market['asset']}")
            print(f"  Price: ${market['price_usd']}")
            print(f"  Source: {market['source']}")
            print(f"  Status: {market['status']}")

        cost = route["cost"]

        print()
        print("Cost:")

        if cost["value"] is None:
            print("  Value: None")
        else:
            print(
                f"  Value: "
                f"${cost['value']:.6f}"
            )

        print(f"  Currency: {cost['currency']}")
        print(f"  Status: {cost['status']}")
        print(f"  Source: {cost['source']}")
        print(f"  Confidence: {cost['confidence']}")

        settlement = route["settlement_time"]

        print()
        print("Settlement time:")
        print(f"  Value: {settlement['value']}")
        print(f"  Unit: {settlement['unit']}")
        print(f"  Status: {settlement['status']}")

        print()
        print(f"Status: {route['status']}")