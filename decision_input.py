def build_decision_input(
    intelligence,
    regulatory_evidence=None,
    telegraph_intelligence=None,
    payment_intent=None,
):

    """
    Convert normalized transaction intelligence
    into a provider-independent decision input.

    Regulatory evidence is optional so existing
    Phase 8.15 behavior remains unchanged.

    PaymentIntent is optional so existing callers
    remain compatible while Phase E integration
    is introduced incrementally.
    """

    decision_input = {
        "asset": intelligence["asset"],
        "network": intelligence["network"],
        "chain_id": intelligence["chain_id"],

        "transaction_status": intelligence["status"],
        "confidence": intelligence["confidence"],

        "transaction_value_usd": intelligence["value_usd"],
        "network_cost_usd": intelligence["network_cost_usd"],

        "economic_data": {
            "asset_price_usd": intelligence["market_price_usd"],
            "network_cost_usd": intelligence["network_cost_usd"],
        },
    }

    # --------------------------------------------------------
    # PHASE 9 — REGULATORY CONTEXT
    # --------------------------------------------------------

    if regulatory_evidence is not None:

        decision_input["regulatory"] = (
            regulatory_evidence
        )

    # --------------------------------------------------------
    # PHASE 10.4 — TELEGRAPH INTELLIGENCE
    # --------------------------------------------------------

    if telegraph_intelligence is not None:

        decision_input["telegraph_intelligence"] = (
            telegraph_intelligence
        )

    # --------------------------------------------------------
    # PHASE E.1 — PAYMENT INTENT
    # --------------------------------------------------------

    if payment_intent is not None:

        decision_input["payment_intent"] = (
            payment_intent
        )

    return decision_input


if __name__ == "__main__":

    from transaction_intelligence import (
        build_transaction_intelligence
    )

    from payment_intent import (
        build_payment_intent,
        validate_payment_intent,
    )

    # --------------------------------------------------------
    # REAL TRANSACTION INTELLIGENCE
    # --------------------------------------------------------

    intelligence = (
        build_transaction_intelligence()
    )

    # --------------------------------------------------------
    # PHASE E.2 — BUILD PAYMENT INTENT
    # --------------------------------------------------------

    payment_intent = build_payment_intent(
        amount=50000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="counterparty-A",
    )

    payment_intent = (
        validate_payment_intent(
            payment_intent
        )
    )

    # --------------------------------------------------------
    # VERIFY PAYMENT INTENT
    # --------------------------------------------------------

    if (
        payment_intent["metadata"]["status"]
        != "VALIDATED"
    ):

        raise ValueError(
            "PaymentIntent validation failed"
        )

    # --------------------------------------------------------
    # BUILD DECISION INPUT
    # --------------------------------------------------------

    decision_input = build_decision_input(
        intelligence,
        payment_intent=payment_intent,
    )

    # --------------------------------------------------------
    # VERIFY PAYMENT INTENT INTEGRATION
    # --------------------------------------------------------

    if (
        "payment_intent"
        not in decision_input
    ):

        raise ValueError(
            "PaymentIntent was not included "
            "in DecisionInput"
        )

    if (
        decision_input["payment_intent"]
        is not payment_intent
    ):

        raise ValueError(
            "DecisionInput does not preserve "
            "the canonical PaymentIntent"
        )

    # --------------------------------------------------------
    # VERIFY ROUTE IS NOT SELECTED BY INTENT
    # --------------------------------------------------------

    if (
        payment_intent[
            "settlement_preferences"
        ]["asset"]
        is not None
    ):

        raise ValueError(
            "PaymentIntent unexpectedly "
            "selected a settlement asset"
        )

    if (
        payment_intent[
            "settlement_preferences"
        ]["network"]
        is not None
    ):

        raise ValueError(
            "PaymentIntent unexpectedly "
            "selected a settlement network"
        )

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    print("=== PHASE E.2 PAYMENT INTENT ===")

    print(
        f"Intent ID: "
        f"{payment_intent['intent_id']}"
    )

    print(
        f"Status: "
        f"{payment_intent['metadata']['status']}"
    )

    print(
        f"Amount: "
        f"{payment_intent['transaction']['amount']}"
    )

    print(
        f"Source currency: "
        f"{payment_intent['transaction']['source_currency']}"
    )

    print(
        f"Destination currency: "
        f"{payment_intent['transaction']['destination_currency']}"
    )

    print(
        f"Counterparty: "
        f"{payment_intent['counterparty']['identifier']}"
    )

    print(
        "Settlement asset: "
        f"{payment_intent['settlement_preferences']['asset']}"
    )

    print(
        "Settlement network: "
        f"{payment_intent['settlement_preferences']['network']}"
    )

    print()

    print(
        "PaymentIntent → DecisionInput: PASS"
    )

    print(
        "Intent route selection: NOT PERFORMED"
    )