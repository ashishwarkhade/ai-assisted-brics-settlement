import json
import subprocess

from real_route_source import get_real_eth_price


TX_HASH = "0xc4eb143d25b904e28c391d7aea44c2f0f23790eee84836bb90aab9d091f20a6a"
BASE_RPC = "https://mainnet.base.org"


def get_transaction_receipt(tx_hash):

    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getTransactionReceipt",
        "params": [tx_hash]
    })

    result = subprocess.run(
        [
            "curl",
            "-s",
            "-X", "POST",
            BASE_RPC,
            "-H", "Content-Type: application/json",
            "--data", payload
        ],
        capture_output=True,
        text=True,
        check=True
    )

    data = json.loads(result.stdout)

    if "error" in data:
        raise RuntimeError(data["error"])

    if data.get("result") is None:
        raise RuntimeError("Transaction receipt not found")

    return data["result"]


def calculate_transaction_fee(gas_used, gas_price_wei, l1_fee_wei):

    execution_fee_wei = gas_used * gas_price_wei
    total_fee_wei = execution_fee_wei + l1_fee_wei

    execution_fee_eth = execution_fee_wei / 10**18
    l1_fee_eth = l1_fee_wei / 10**18
    total_fee_eth = total_fee_wei / 10**18

    return (
        execution_fee_wei,
        execution_fee_eth,
        l1_fee_eth,
        total_fee_wei,
        total_fee_eth
    )


def get_transaction_cost():

    receipt = get_transaction_receipt(TX_HASH)

    gas_used = int(receipt["gasUsed"], 16)
    gas_price_wei = int(receipt["effectiveGasPrice"], 16)
    l1_fee_wei = int(receipt["l1Fee"], 16)

    market = get_real_eth_price()

    if market["status"] != "REAL":
        raise RuntimeError(
            "ETH market price unavailable"
        )

    (
        execution_fee_wei,
        execution_fee_eth,
        l1_fee_eth,
        total_fee_wei,
        total_fee_eth
    ) = calculate_transaction_fee(
        gas_used,
        gas_price_wei,
        l1_fee_wei
    )

    execution_fee_usd = execution_fee_eth * market["value"]
    l1_fee_usd = l1_fee_eth * market["value"]
    total_fee_usd = total_fee_eth * market["value"]

    return {
        "transaction_hash": TX_HASH,
        "network": "Base",
        "gas_used": gas_used,
        "effective_gas_price_wei": gas_price_wei,
        "execution_fee_wei": execution_fee_wei,
        "execution_fee_eth": execution_fee_eth,
        "execution_fee_usd": execution_fee_usd,
        "l1_fee_wei": l1_fee_wei,
        "l1_fee_eth": l1_fee_eth,
        "l1_fee_usd": l1_fee_usd,
        "total_network_fee_wei": total_fee_wei,
        "total_network_fee_eth": total_fee_eth,
        "total_network_cost_usd": total_fee_usd,
        "source": "Base RPC",
        "status": "REAL",
        "confidence": 1.0,
    }


if __name__ == "__main__":

    print("Getting real Base transaction receipt...")

    cost = get_transaction_cost()

    print()
    print("=== REAL TRANSACTION COST ===")
    print(f"Transaction: {cost['transaction_hash']}")
    print(f"Network: {cost['network']}")
    print(f"Gas used: {cost['gas_used']}")
    print(
        f"Effective gas price: "
        f"{cost['effective_gas_price_wei']} wei"
    )

    print()
    print(
        f"Execution fee: "
        f"{cost['execution_fee_wei']} wei"
    )
    print(
        f"Execution fee: "
        f"{cost['execution_fee_eth']:.12f} ETH"
    )
    print(
        f"Execution fee: "
        f"${cost['execution_fee_usd']:.6f}"
    )

    print()
    print(
        f"L1 fee: "
        f"{cost['l1_fee_wei']} wei"
    )
    print(
        f"L1 fee: "
        f"{cost['l1_fee_eth']:.12f} ETH"
    )
    print(
        f"L1 fee: "
        f"${cost['l1_fee_usd']:.6f}"
    )

    print()
    print(
        f"Total network fee: "
        f"{cost['total_network_fee_wei']} wei"
    )
    print(
        f"Total network fee: "
        f"{cost['total_network_fee_eth']:.12f} ETH"
    )
    print(
        f"Total network fee: "
        f"${cost['total_network_cost_usd']:.6f}"
    )