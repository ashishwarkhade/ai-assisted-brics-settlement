"""
Phase 10.3 — Telegraph Intelligence Adapter

Purpose:

    Convert the raw Telegraph /trade-context response
    into the provider-independent intelligence contract.

Architecture:

    Telegraph /trade-context
            |
            v
    Telegraph Intelligence Adapter
            |
            v
    intelligence_contract.py
            |
            v
    Normalized Intelligence
            |
            v
    Deterministic Decision Engine

IMPORTANT:

    This adapter ONLY transforms external intelligence.

    It does NOT:

        - determine settlement eligibility
        - determine regulatory compliance
        - select settlement routes
        - calculate settlement risk
        - recommend a route
        - override deterministic validation

Telegraph remains an intelligence provider.

The resulting evidence is provider-independent even though
the source field identifies Telegraph-derived data.
"""

from datetime import datetime, timezone

from intelligence_contract import (
    build_intelligence_evidence,
    build_route_intelligence_contract,
    build_normalized_intelligence,
)


# ============================================================
# HELPERS
# ============================================================

def unix_seconds_to_iso(timestamp):
    """
    Convert Unix timestamp in seconds to UTC ISO-8601.

    Telegraph fear/greed timestamps are expressed in seconds.
    """

    if timestamp is None:
        return None

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    ).isoformat()


def unix_milliseconds_to_iso(timestamp):
    """
    Convert Unix timestamp in milliseconds to UTC ISO-8601.

    Telegraph positioning timestamps are expressed in
    milliseconds.
    """

    if timestamp is None:
        return None

    return datetime.fromtimestamp(
        timestamp / 1000,
        tz=timezone.utc,
    ).isoformat()


def response_timestamp_to_iso(timestamp):
    """
    Convert the top-level Telegraph response timestamp.

    Telegraph /trade-context uses milliseconds for `ts`.
    """

    if timestamp is None:
        return None

    return unix_milliseconds_to_iso(timestamp)


def require_field(data, field_name):
    """
    Require a field to exist in a provider response.
    """

    if field_name not in data:
        raise ValueError(
            f"Missing required Telegraph field: {field_name}"
        )

    return data[field_name]


# ============================================================
# EVIDENCE BUILDERS
# ============================================================

def build_available_evidence(
    metric,
    value,
    unit,
    source,
    timestamp,
    measurement_type="OBSERVED",
    confidence="HIGH",
):
    """
    Build evidence for successfully received Telegraph data.
    """

    return build_intelligence_evidence(
        metric=metric,
        value=value,
        unit=unit,
        source=source,
        timestamp=timestamp,
        status="AVAILABLE",
        confidence=confidence,
        validation="VALID",
        measurement_type=measurement_type,
    )


# ============================================================
# FEAR / GREED
# ============================================================

def normalize_fear_greed(
    trade_context,
    generated_at,
):
    """
    Normalize Telegraph fear/greed intelligence.
    """

    data = require_field(
        trade_context,
        "fear_greed",
    )

    timestamp = unix_seconds_to_iso(
        data.get("timestamp")
    )

    if timestamp is None:
        timestamp = generated_at

    return [
        build_available_evidence(
            metric="market_fear_greed",
            value=data.get("value"),
            unit="index",
            source="Telegraph / alternative.me",
            timestamp=timestamp,
            measurement_type="OBSERVED",
            confidence="HIGH",
        ),
    ]


# ============================================================
# FUNDING
# ============================================================

def normalize_funding(
    trade_context,
    asset,
    generated_at,
):
    """
    Normalize funding information for one asset.
    """

    funding = require_field(
        trade_context,
        "funding",
    )

    asset_data = require_field(
        funding,
        asset,
    )

    timestamp = generated_at

    return [
        build_available_evidence(
            metric=f"{asset}_funding_rate_hourly",
            value=asset_data.get(
                "funding_rate_hourly"
            ),
            unit="rate",
            source="Telegraph / hyperliquid",
            timestamp=timestamp,
            measurement_type="OBSERVED",
            confidence="HIGH",
        ),

        build_available_evidence(
            metric=f"{asset}_funding_rate_pct_hourly",
            value=asset_data.get(
                "funding_rate_pct_hourly"
            ),
            unit="percent",
            source="Telegraph / hyperliquid",
            timestamp=timestamp,
            measurement_type="OBSERVED",
            confidence="HIGH",
        ),

        build_available_evidence(
            metric=f"{asset}_funding_rate_8h_equiv",
            value=asset_data.get(
                "funding_rate_8h_equiv"
            ),
            unit="rate",
            source="Telegraph / hyperliquid",
            timestamp=timestamp,
            measurement_type="OBSERVED",
            confidence="HIGH",
        ),

        build_available_evidence(
            metric=f"{asset}_mark_price",
            value=asset_data.get(
                "mark_price"
            ),
            unit="USD",
            source="Telegraph / hyperliquid",
            timestamp=timestamp,
            measurement_type="OBSERVED",
            confidence="HIGH",
        ),

        build_available_evidence(
            metric=f"{asset}_funding_open_interest",
            value=asset_data.get(
                "open_interest"
            ),
            unit="asset",
            source="Telegraph / hyperliquid",
            timestamp=timestamp,
            measurement_type="OBSERVED",
            confidence="HIGH",
        ),
    ]


# ============================================================
# PRICES
# ============================================================

def normalize_price(
    trade_context,
    asset,
    generated_at,
):
    """
    Normalize Coinbase price intelligence.
    """

    prices = require_field(
        trade_context,
        "prices",
    )

    asset_data = require_field(
        prices,
        asset,
    )

    timestamp = generated_at

    if asset_data.get("publish_time") is not None:
        timestamp = (
            unix_milliseconds_to_iso(
                asset_data["publish_time"]
            )
        )

    return [
        build_available_evidence(
            metric=f"{asset}_price",
            value=asset_data.get(
                "price"
            ),
            unit="USD",
            source="Telegraph / coinbase",
            timestamp=timestamp,
            measurement_type="OBSERVED",
            confidence="HIGH",
        ),
    ]


# ============================================================
# POSITIONING
# ============================================================

def normalize_positioning(
    trade_context,
    asset,
    generated_at,
):
    """
    Normalize positioning and open-interest intelligence.
    """

    positioning = require_field(
        trade_context,
        "positioning",
    )

    asset_data = require_field(
        positioning,
        asset,
    )

    evidence = []

    ratio = asset_data.get(
        "long_short_ratio"
    )

    if ratio is not None:

        timestamp = generated_at

        if ratio.get("ts") is not None:
            timestamp = (
                unix_milliseconds_to_iso(
                    ratio["ts"]
                )
            )

        evidence.extend([
            build_available_evidence(
                metric=f"{asset}_long_pct",
                value=ratio.get(
                    "long_pct"
                ),
                unit="percent",
                source="Telegraph / bybit_v5_public",
                timestamp=timestamp,
                measurement_type="OBSERVED",
                confidence="HIGH",
            ),

            build_available_evidence(
                metric=f"{asset}_short_pct",
                value=ratio.get(
                    "short_pct"
                ),
                unit="percent",
                source="Telegraph / bybit_v5_public",
                timestamp=timestamp,
                measurement_type="OBSERVED",
                confidence="HIGH",
            ),

            build_available_evidence(
                metric=f"{asset}_long_pct_prev_hour",
                value=ratio.get(
                    "long_pct_prev_hour"
                ),
                unit="percent",
                source="Telegraph / bybit_v5_public",
                timestamp=timestamp,
                measurement_type="OBSERVED",
                confidence="HIGH",
            ),
        ])

    open_interest = asset_data.get(
        "open_interest"
    )

    if open_interest is not None:

        evidence.extend([
            build_available_evidence(
                metric=f"{asset}_open_interest",
                value=open_interest.get(
                    "base"
                ),
                unit="asset",
                source="Telegraph / bybit_v5_public",
                timestamp=generated_at,
                measurement_type="OBSERVED",
                confidence="HIGH",
            ),

            build_available_evidence(
                metric=f"{asset}_open_interest_usd",
                value=open_interest.get(
                    "usd"
                ),
                unit="USD",
                source="Telegraph / bybit_v5_public",
                timestamp=generated_at,
                measurement_type="OBSERVED",
                confidence="HIGH",
            ),

            build_available_evidence(
                metric=f"{asset}_open_interest_change_1h",
                value=open_interest.get(
                    "change_1h_pct"
                ),
                unit="percent",
                source="Telegraph / bybit_v5_public",
                timestamp=generated_at,
                measurement_type="OBSERVED",
                confidence="HIGH",
            ),

            build_available_evidence(
                metric=f"{asset}_open_interest_change_24h",
                value=open_interest.get(
                    "change_24h_pct"
                ),
                unit="percent",
                source="Telegraph / bybit_v5_public",
                timestamp=generated_at,
                measurement_type="OBSERVED",
                confidence="HIGH",
            ),
        ])

    return evidence


# ============================================================
# LIQUIDATIONS
# ============================================================

def normalize_liquidations(
    trade_context,
    asset,
    generated_at,
):
    """
    Normalize liquidation totals.

    We deliberately use aggregate 1h and 24h evidence first.

    Exchange-level detail remains available in the raw
    Telegraph response and can be added later if required.
    """

    liquidations = require_field(
        trade_context,
        "liquidations",
    )

    asset_data = require_field(
        liquidations,
        asset,
    )

    evidence = []

    for period in ("1h", "24h"):

        period_data = asset_data.get(
            period
        )

        if period_data is None:
            continue

        prefix = f"{asset}_liquidations_{period}"

        evidence.extend([
            build_available_evidence(
                metric=f"{prefix}_total_usd",
                value=period_data.get(
                    "total_usd"
                ),
                unit="USD",
                source="Telegraph / multi_exchange_collector",
                timestamp=generated_at,
                measurement_type="OBSERVED",
                confidence="HIGH",
            ),

            build_available_evidence(
                metric=f"{prefix}_longs_usd",
                value=period_data.get(
                    "longs_liquidated_usd"
                ),
                unit="USD",
                source="Telegraph / multi_exchange_collector",
                timestamp=generated_at,
                measurement_type="OBSERVED",
                confidence="HIGH",
            ),

            build_available_evidence(
                metric=f"{prefix}_shorts_usd",
                value=period_data.get(
                    "shorts_liquidated_usd"
                ),
                unit="USD",
                source="Telegraph / multi_exchange_collector",
                timestamp=generated_at,
                measurement_type="OBSERVED",
                confidence="HIGH",
            ),

            build_available_evidence(
                metric=f"{prefix}_events",
                value=period_data.get(
                    "events"
                ),
                unit="events",
                source="Telegraph / multi_exchange_collector",
                timestamp=generated_at,
                measurement_type="OBSERVED",
                confidence="HIGH",
            ),
        ])

    return evidence


# ============================================================
# COMPLETE TELEGRAPH NORMALIZATION
# ============================================================

def normalize_telegraph_trade_context(
    trade_context,
    request_id="telegraph-trade-context",
):
    """
    Convert a complete Telegraph /trade-context response
    into the provider-independent intelligence contract.
    """

    if not isinstance(
        trade_context,
        dict,
    ):
        raise ValueError(
            "trade_context must be a dictionary"
        )

    raw_timestamp = trade_context.get(
        "ts"
    )

    generated_at = (
        response_timestamp_to_iso(
            raw_timestamp
        )
    )

    if generated_at is None:
        raise ValueError(
            "Telegraph trade-context timestamp missing"
        )

    # --------------------------------------------------------
    # Bitcoin route
    # --------------------------------------------------------

    btc_evidence = []

    btc_evidence.extend(
        normalize_price(
            trade_context,
            "btc",
            generated_at,
        )
    )

    btc_evidence.extend(
        normalize_funding(
            trade_context,
            "btc",
            generated_at,
        )
    )

    btc_evidence.extend(
        normalize_positioning(
            trade_context,
            "btc",
            generated_at,
        )
    )

    btc_evidence.extend(
        normalize_liquidations(
            trade_context,
            "btc",
            generated_at,
        )
    )

    btc_evidence.extend(
        normalize_fear_greed(
            trade_context,
            generated_at,
        )
    )

    btc_route = build_route_intelligence_contract(
        route_id="bitcoin",
        asset="BTC",
        network="Bitcoin",
        evidence=btc_evidence,
    )

    # --------------------------------------------------------
    # Solana route
    # --------------------------------------------------------

    sol_evidence = []

    sol_evidence.extend(
        normalize_price(
            trade_context,
            "sol",
            generated_at,
        )
    )

    sol_evidence.extend(
        normalize_funding(
            trade_context,
            "sol",
            generated_at,
        )
    )

    sol_evidence.extend(
        normalize_positioning(
            trade_context,
            "sol",
            generated_at,
        )
    )

    sol_evidence.extend(
        normalize_liquidations(
            trade_context,
            "sol",
            generated_at,
        )
    )

    sol_evidence.extend(
        normalize_fear_greed(
            trade_context,
            generated_at,
        )
    )

    sol_route = build_route_intelligence_contract(
        route_id="solana",
        asset="SOL",
        network="Solana",
        evidence=sol_evidence,
    )

    # --------------------------------------------------------
    # Complete normalized intelligence
    # --------------------------------------------------------

    return build_normalized_intelligence(
        request_id=request_id,
        generated_at=generated_at,
        routes={
            "bitcoin": btc_route,
            "solana": sol_route,
        },
    )


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    import json
    from pathlib import Path

    input_file = (
        Path("/tmp/telegraph_trade_context.txt")
    )

    print(
        "This module expects the parsed JSON response."
    )

    print(
        "Use normalize_telegraph_trade_context("
        "trade_context) from Python code."
    )
