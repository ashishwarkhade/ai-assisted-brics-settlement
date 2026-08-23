from real_transaction import get_transaction_facts
from market_data import get_eth_price
from transaction_cost import get_transaction_receipt


TX_HASH = "0xc4eb143d25b904e28c391d7aea44c2f0f23790eee84836bb90aab9d091f20a6a"


def build_transaction_intelligence():

    # 1. Blockchain transaction facts
    transaction = get_transaction_facts()

    # 2. Live market data
    market = get_eth_price()

    # 3. Real transaction receipt
    receipt = get_transaction_receipt(TX_HASH)

    # Convert blockchain hexadecimal values
    gas_used = int(receipt["gasUsed"], 16)
    gas_price_wei = int(receipt["effectiveGasPrice"], 16)
    l1_fee_wei = int(receipt["l1Fee"], 16)

    # Calculate execution fee
    execution_fee_wei = gas_used * gas_price_wei

    # Calculate total network fee
    total_fee_wei = execution_fee_wei + l1_fee_wei

    # Convert to ETH
    total_fee_eth = total_fee_wei / 10**18

    # Calculate transaction value in USD
    value_usd = transaction["value_eth"] * market["price"]

    # Calculate network cost in USD
    network_cost_usd = total_fee_eth * market["price"]

    return {
        "type": "transaction",
        "asset": transaction["asset"],
        "network": transaction["network"],
        "chain_id": transaction["chain_id"],
        "status": transaction["status"],
        "confidence": transaction["confidence"],

        "value_eth": transaction["value_eth"],
        "value_usd": value_usd,

        "gas_used": gas_used,
        "effective_gas_price_wei": gas_price_wei,
        "l1_fee_wei": l1_fee_wei,

        "network_cost_eth": total_fee_eth,
        "network_cost_usd": network_cost_usd,

        "market_price_usd": market["price"],
    }


if __name__ == "__main__":

    intelligence = build_transaction_intelligence()

    print("=== NORMALIZED TRANSACTION INTELLIGENCE ===")

    print(f"Asset: {intelligence['asset']}")
    print(f"Network: {intelligence['network']}")
    print(f"Chain ID: {intelligence['chain_id']}")
    print(f"Status: {intelligence['status']}")
    print(f"Confidence: {intelligence['confidence']}")

    print()
    print(f"Value: {intelligence['value_eth']} ETH")
    print(f"Value: ${intelligence['value_usd']:.2f}")

    print()
    print(f"Gas used: {intelligence['gas_used']}")
    print(
        f"Effective gas price: "
        f"{intelligence['effective_gas_price_wei']} wei"
    )
    print(f"L1 fee: {intelligence['l1_fee_wei']} wei")

    print()
    print(
        f"Network cost: "
        f"{intelligence['network_cost_eth']:.12f} ETH"
    )
    print(
        f"Network cost: "
        f"${intelligence['network_cost_usd']:.6f}"
    )

    print()
    print(f"ETH/USD: ${intelligence['market_price_usd']}")
