import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def get_real_eth_price():

    url = (
        "https://api.coingecko.com/api/v3/"
        "simple/price?ids=ethereum&vs_currencies=usd"
    )

    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    try:
        with urlopen(request, timeout=10) as response:
            data = json.load(response)

        return {
    "type": "MARKET_PRICE",
    "asset": "ETH",
    "value": data["ethereum"]["usd"],
    "unit": "USD",
    "source": "CoinGecko",
    "status": "REAL",
    "confidence": 1.0,
}

    except HTTPError as error:
        return {
    "type": "MARKET_PRICE",
    "asset": "ETH",
    "value": None,
    "unit": "USD",
    "source": "CoinGecko",
    "status": "UNKNOWN",
    "reason": f"HTTP_{error.code}",
    "confidence": 0.0,
}

    except URLError as error:
        return {
    "type": "MARKET_PRICE",
    "asset": "ETH",
    "value": None,
    "unit": "USD",
    "source": "CoinGecko",
    "status": "UNKNOWN",
    "reason": "NETWORK_ERROR",
    "confidence": 0.0,
}

    except Exception as error:
        return {
    "type": "MARKET_PRICE",
    "asset": "ETH",
    "value": None,
    "unit": "USD",
    "source": "CoinGecko",
    "status": "UNKNOWN",
    "reason": "UNEXPECTED_ERROR",
    "confidence": 0.0,
}


if __name__ == "__main__":

    result = get_real_eth_price()

    print("=== REAL SOURCE ADAPTER ===")

    for key, value in result.items():
        print(f"{key}: {value}")
