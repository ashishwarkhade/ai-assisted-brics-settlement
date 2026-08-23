
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


BITCOIN_MEMPOOL_API = "https://mempool.space/api/v1/fees/recommended"
BITCOIN_PRICE_API = (
    "https://api.coingecko.com/api/v3/"
    "simple/price?ids=bitcoin&vs_currencies=usd"
)

# Explicit model assumption.
# This is NOT an observed transaction size.
ESTIMATED_TRANSACTION_VBYTES = 140


def get_bitcoin_fee_intelligence():

    request = Request(
        BITCOIN_MEMPOOL_API,
        headers={
            "User-Agent": "AI-Assisted-BRICS-Settlement/1.0"
        }
    )

    with urlopen(request, timeout=10) as response:
        data = json.load(response)

    if "fastestFee" not in data:
        raise RuntimeError(
            "Bitcoin fee data unavailable"
        )

    return {
        "network": "Bitcoin",
        "unit": "sat/vByte",

        "fastest_fee": data["fastestFee"],
        "half_hour_fee": data["halfHourFee"],
        "hour_fee": data["hourFee"],
        "minimum_fee": data["minimumFee"],

        "source": "mempool.space",
        "status": "REAL",
        "confidence": 1.0,
    }


def get_real_btc_price():

    request = Request(
        BITCOIN_PRICE_API,
        headers={
            "User-Agent": "AI-Assisted-BRICS-Settlement/1.0"
        }
    )

    try:

        with urlopen(request, timeout=10) as response:
            data = json.load(response)

        price = data["bitcoin"]["usd"]

        return {
            "asset": "BTC",
            "value": price,
            "unit": "USD",
            "source": "CoinGecko",
            "status": "REAL",
            "confidence": 1.0,
        }

    except (HTTPError, URLError, KeyError, ValueError):

        return {
            "asset": "BTC",
            "value": None,
            "unit": "USD",
            "source": "CoinGecko",
            "status": "UNKNOWN",
            "confidence": 0.0,
        }


def estimate_bitcoin_transaction_cost():

    fee = get_bitcoin_fee_intelligence()
    market = get_real_btc_price()

    if market["status"] != "REAL":

        return {
            "value": None,
            "currency": "USD",
            "status": "UNKNOWN",
            "source": "mempool.space + CoinGecko",
            "confidence": 0.0,
        }

    fee_rate_sat_vbyte = fee["fastest_fee"]

    estimated_fee_sat = (
        fee_rate_sat_vbyte
        * ESTIMATED_TRANSACTION_VBYTES
    )

    estimated_fee_btc = estimated_fee_sat / 100_000_000

    estimated_fee_usd = (
        estimated_fee_btc
        * market["value"]
    )

    return {
        "value": estimated_fee_usd,
        "currency": "USD",
        "status": "REAL_ESTIMATE",
        "source": "mempool.space + CoinGecko",
        "confidence": 0.8,

        "fee_rate": fee_rate_sat_vbyte,
        "fee_rate_unit": "sat/vByte",

        "estimated_transaction_vbytes":
            ESTIMATED_TRANSACTION_VBYTES,

        "estimated_fee_sat": estimated_fee_sat,
        "estimated_fee_btc": estimated_fee_btc,

        "btc_price_usd": market["value"],
    }


if __name__ == "__main__":

    fee = get_bitcoin_fee_intelligence()
    market = get_real_btc_price()
    cost = estimate_bitcoin_transaction_cost()

    print("=== REAL BITCOIN NETWORK INTELLIGENCE ===")

    print(f"Network: {fee['network']}")
    print(f"Unit: {fee['unit']}")

    print()
    print(
        f"Fastest fee: "
        f"{fee['fastest_fee']} sat/vByte"
    )

    print(
        f"30-minute fee: "
        f"{fee['half_hour_fee']} sat/vByte"
    )

    print(
        f"60-minute fee: "
        f"{fee['hour_fee']} sat/vByte"
    )

    print(
        f"Minimum fee: "
        f"{fee['minimum_fee']} sat/vByte"
    )

    print()
    print(f"BTC price: ${market['value']}")
    print(f"Price source: {market['source']}")

    print()
    print("=== BITCOIN COST ESTIMATE ===")

    print(
        f"Estimated transaction size: "
        f"{ESTIMATED_TRANSACTION_VBYTES} vBytes"
    )

    print(
        f"Estimated fee: "
        f"{cost['estimated_fee_sat']} sat"
    )

    print(
        f"Estimated fee: "
        f"{cost['estimated_fee_btc']:.8f} BTC"
    )

    print(
        f"Estimated cost: "
        f"${cost['value']:.6f}"
    )

    print(f"Status: {cost['status']}")
    print(f"Confidence: {cost['confidence']}")
