import json
import subprocess


BASE_RPC = "https://mainnet.base.org"


def get_base_network_intelligence():

    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_gasPrice",
        "params": []
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
        raise RuntimeError("Base gas price unavailable")

    gas_price_wei = int(data["result"], 16)

    return {
        "network": "Base",
        "chain_id": 8453,
        "gas_price_wei": gas_price_wei,
        "source": "Base RPC",
        "status": "REAL",
        "confidence": 1.0,
    }


if __name__ == "__main__":

    network = get_base_network_intelligence()

    print("=== REAL BASE NETWORK INTELLIGENCE ===")

    print(f"Network: {network['network']}")
    print(f"Chain ID: {network['chain_id']}")
    print(
        f"Gas price: "
        f"{network['gas_price_wei']} wei"
    )

    print()
    print(f"Source: {network['source']}")
    print(f"Status: {network['status']}")
    print(f"Confidence: {network['confidence']}")
