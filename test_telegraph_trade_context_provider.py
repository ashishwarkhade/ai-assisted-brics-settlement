import json

import pytest

from telegraph_trade_context_provider import (
    load_trade_context,
)


def test_load_trade_context_returns_dictionary(
    tmp_path,
):

    payload = {
        "fear_greed": {
            "value": 71,
        },
        "funding": {
            "btc": {},
            "sol": {},
        },
        "liquidations": {},
        "positioning": {},
        "prices": {},
        "ts": 1787836306181,
    }

    file_path = (
        tmp_path
        / "trade_context.json"
    )

    file_path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )

    result = load_trade_context(
        file_path
    )

    assert isinstance(
        result,
        dict,
    )

    assert (
        result["ts"]
        == 1787836306181
    )


def test_missing_trade_context_file_fails(
    tmp_path,
):

    file_path = (
        tmp_path
        / "missing.json"
    )

    with pytest.raises(
        FileNotFoundError,
        match="not found",
    ):

        load_trade_context(
            file_path
        )


def test_non_dictionary_response_fails(
    tmp_path,
):

    file_path = (
        tmp_path
        / "invalid.json"
    )

    file_path.write_text(
        json.dumps(["invalid"]),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="JSON object",
    ):

        load_trade_context(
            file_path
        )
