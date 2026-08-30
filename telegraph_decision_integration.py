import json
from pathlib import Path

from decision_input import build_decision_input
from telegraph_intelligence_adapter import (
    normalize_telegraph_trade_context,
)


def load_telegraph_trade_context(
    input_file="/tmp/telegraph_trade_context.txt",
):
    """
    Load the successful Telegraph /trade-context response.

    The Telegraph test output may contain terminal/log text
    around the JSON payload, so locate the JSON object rather
    than assuming the entire file is JSON.
    """

    path = Path(input_file)

    if not path.exists():
        raise FileNotFoundError(
            f"Telegraph trade-context file not found: {input_file}"
        )

    text = path.read_text(
        encoding="utf-8",
    ).strip()

    start = text.find("{")

    if start == -1:
        raise ValueError(
            "No JSON object found in Telegraph response"
        )

    decoder = json.JSONDecoder()

    try:
        trade_context, _ = decoder.raw_decode(
            text[start:]
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Unable to parse Telegraph trade-context JSON"
        ) from exc

    if not isinstance(trade_context, dict):
        raise ValueError(
            "Telegraph trade-context must be a dictionary"
        )

    return trade_context


def build_telegraph_decision_input(
    intelligence,
    regulatory_evidence=None,
    payment_intent=None,
    input_file="/tmp/telegraph_trade_context.txt",
    request_id="phase-10.5-telegraph",
):
    """
    Connect Telegraph intelligence to the existing
    provider-independent decision-input contract.

    Telegraph remains an intelligence provider.

    PaymentIntent describes the user request and is
    passed through to the provider-independent
    decision-input contract.

    This function does NOT:
        - make settlement decisions
        - determine eligibility
        - rank routes
        - recommend a route
        - determine regulatory compliance
        - override deterministic validation
    """

    trade_context = load_telegraph_trade_context(
        input_file
    )

    telegraph_intelligence = (
        normalize_telegraph_trade_context(
            trade_context,
            request_id=request_id,
        )
    )

    return build_decision_input(
        intelligence=intelligence,
        regulatory_evidence=regulatory_evidence,
        telegraph_intelligence=telegraph_intelligence,
        payment_intent=payment_intent,
    )


if __name__ == "__main__":

    from economic_intelligence import (
        build_economic_intelligence,
    )

    from payment_intent import (
        build_payment_intent,
        validate_payment_intent,
    )

    # --------------------------------------------------------
    # REAL ECONOMIC INTELLIGENCE
    # --------------------------------------------------------

    economic = build_economic_intelligence()

    # --------------------------------------------------------
    # PHASE E.3 — BUILD PAYMENT INTENT
    # --------------------------------------------------------

    payment_intent = build_payment_intent(
        amount=50000,
        source_currency="USD",
        destination_currency="USD",
        counterparty="counterparty-A",
    )

    payment_intent = validate_payment_intent(
        payment_intent
    )

    if (
        payment_intent["metadata"]["status"]
        != "VALIDATED"
    ):

        raise ValueError(
            "PaymentIntent validation failed"
        )

    # --------------------------------------------------------
    # BUILD TELEGRAPH DECISION INPUT
    # --------------------------------------------------------

    decision_input = build_telegraph_decision_input(
        intelligence={
            "asset": "ETH",
            "network": "Base",
            "chain_id": 8453,
            "status": economic["status"],
            "confidence": economic["confidence"],
            "value_usd": economic[
                "transaction_value_usd"
            ],
            "network_cost_usd": economic[
                "network_cost_usd"
            ],
            "market_price_usd": economic[
                "eth_price_usd"
            ],
        },
        payment_intent=payment_intent,
    )

    # --------------------------------------------------------
    # VERIFY PAYMENT INTENT PRESERVATION
    # --------------------------------------------------------

    if (
        "payment_intent"
        not in decision_input
    ):

        raise ValueError(
            "PaymentIntent was not preserved "
            "in Telegraph DecisionInput"
        )

    if (
        decision_input["payment_intent"]
        is not payment_intent
    ):

        raise ValueError(
            "Telegraph integration did not preserve "
            "the canonical PaymentIntent"
        )

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    print(
        "=== TELEGRAPH DECISION INPUT INTEGRATION ==="
    )

    print(
        f"Intent ID: "
        f"{decision_input['payment_intent']['intent_id']}"
    )

    print(
        f"Intent status: "
        f"{decision_input['payment_intent']['metadata']['status']}"
    )

    print(
        f"Request ID: "
        f"{decision_input['telegraph_intelligence']['request_id']}"
    )

    print(
        f"Generated at: "
        f"{decision_input['telegraph_intelligence']['generated_at']}"
    )

    print(
        f"Routes: "
        f"{list(decision_input['telegraph_intelligence']['routes'].keys())}"
    )

    print()

    for route_id, route in (
        decision_input[
            "telegraph_intelligence"
        ]["routes"].items()
    ):

        print(
            f"{route_id}: "
            f"{route['asset']} / "
            f"{route['network']} | "
            f"evidence={len(route['evidence'])}"
        )

    print()

    print(
        "PaymentIntent → Telegraph DecisionInput: PASS"
    )

    print(
        "Settlement decision: NOT MADE"
    )