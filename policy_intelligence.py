from data_provenance import add_provenance


def build_policy_intelligence():

    return {
        "Bitcoin": {
            "risk": add_provenance(
                35,
                "TEST_POLICY",
                "TEST",
                0.0,
            ),

            "compliance": add_provenance(
                "ALLOWED",
                "TEST_POLICY",
                "TEST",
                0.0,
            ),

            "geopolitical_status": add_provenance(
                "PERMITTED",
                "TEST_POLICY",
                "TEST",
                0.0,
            ),

            "time_minutes": add_provenance(
                10,
                "TEST_POLICY",
                "TEST",
                0.0,
            ),
        },

        "Base": {
            "risk": add_provenance(
                10,
                "TEST_POLICY",
                "TEST",
                0.0,
            ),

            "compliance": add_provenance(
                "ALLOWED",
                "TEST_POLICY",
                "TEST",
                0.0,
            ),

            "geopolitical_status": add_provenance(
                "RESTRICTED",
                "TEST_POLICY",
                "TEST",
                0.0,
            ),

            "time_minutes": add_provenance(
                2,
                "TEST_POLICY",
                "TEST",
                0.0,
            ),
        },
    }


if __name__ == "__main__":

    policies = build_policy_intelligence()

    print("=== POLICY INTELLIGENCE ===")

    for network, policy in policies.items():

        print()
        print(f"Network: {network}")

        for name, item in policy.items():

            print()
            print(f"{name}:")
            print(f"  Value: {item['value']}")
            print(f"  Source: {item['source']}")
            print(f"  Type: {item['source_type']}")
            print(f"  Confidence: {item['confidence']}")
