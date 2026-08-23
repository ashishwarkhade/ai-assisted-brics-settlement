from data_provenance import add_provenance
from policy_source import build_policy_source_data


def build_policy_intelligence():

    source_data = build_policy_source_data()

    return {
        "Bitcoin": {
            "risk": add_provenance(
                35,
                "TEST_POLICY",
                "TEST",
                0.0,
            ),

            "compliance": source_data["Bitcoin"]["compliance"],

            "geopolitical_status":
                source_data["Bitcoin"]["geopolitical_status"],

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

            "compliance": source_data["Base"]["compliance"],

            "geopolitical_status":
                source_data["Base"]["geopolitical_status"],

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