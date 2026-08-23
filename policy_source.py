from data_provenance import add_provenance


def get_bitcoin_compliance_policy():

    return add_provenance(
        "REQUIRES_JURISDICTION_REVIEW",
        "FATF",
        "REFERENCE",
        0.7,
    )


def get_base_compliance_policy():

    return add_provenance(
        "REQUIRES_JURISDICTION_REVIEW",
        "FATF",
        "REFERENCE",
        0.7,
    )


def get_bitcoin_geopolitical_policy():

    return add_provenance(
        "NO_UNIVERSAL_STATUS",
        "BRICS_PAYMENT_DISCUSSIONS",
        "REFERENCE",
        0.5,
    )


def get_base_geopolitical_policy():

    return add_provenance(
        "NO_UNIVERSAL_STATUS",
        "BRICS_PAYMENT_DISCUSSIONS",
        "REFERENCE",
        0.5,
    )


def build_policy_source_data():

    return {
        "Bitcoin": {
            "compliance": get_bitcoin_compliance_policy(),
            "geopolitical_status":
                get_bitcoin_geopolitical_policy(),
        },

        "Base": {
            "compliance": get_base_compliance_policy(),
            "geopolitical_status":
                get_base_geopolitical_policy(),
        },
    }


if __name__ == "__main__":

    policies = build_policy_source_data()

    print("=== POLICY SOURCE DATA ===")

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
