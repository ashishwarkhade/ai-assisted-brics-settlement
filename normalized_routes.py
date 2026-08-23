from route_intelligence import build_route_intelligence


def get_normalized_routes():

    intelligence = build_route_intelligence()

    return intelligence


if __name__ == "__main__":

    routes = get_normalized_routes()

    print("=== NORMALIZED ROUTE INPUT ===")

    for name, route in routes.items():

        print()
        print(f"Route: {route['route']}")
        print(f"Asset: {route['asset']}")
        print(f"Network: {route['network']}")

        cost = route["cost"]

        print(
            f"Cost: {cost['value']} "
            f"{cost['currency']}"
        )

        print(
            f"Cost status: "
            f"{cost['status']}"
        )

        print(
            f"Cost source: "
            f"{cost['source']}"
        )

        print(
            f"Confidence: "
            f"{cost['confidence']}"
        )
