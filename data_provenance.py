def add_provenance(value, source, source_type, confidence):
    return {
        "value": value,
        "source": source,
        "source_type": source_type,
        "confidence": confidence,
    }


if __name__ == "__main__":

    examples = {
        "transaction": add_provenance(
            "Base RPC transaction receipt",
            "Base RPC",
            "REAL",
            1.0,
        ),

        "market": add_provenance(
            "ETH/USD live price",
            "Market API",
            "REAL",
            1.0,
        ),

        "route_cost": add_provenance(
            25.00,
            "Test dataset",
            "TEST",
            0.0,
        ),
    }

    print("=== DATA PROVENANCE ===")

    for name, item in examples.items():
        print(f"{name}:")
        print(f"  value: {item['value']}")
        print(f"  source: {item['source']}")
        print(f"  type: {item['source_type']}")
        print(f"  confidence: {item['confidence']}")
