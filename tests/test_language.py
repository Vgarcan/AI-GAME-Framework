"""Tests for the JSON-based agent language layer."""

import pytest

from game import JsonAgentLanguage


def test_parse_response_accepts_valid_json() -> None:
    """The language layer should parse a valid tool invocation."""

    language = JsonAgentLanguage()
    invocation = language.parse_response(
        '{"tool": "terminate", "args": {"message": "Done"}}'
    )

    assert invocation == {"tool": "terminate", "args": {"message": "Done"}}


def test_parse_response_adds_empty_args_when_missing() -> None:
    """The language layer should default missing args to an empty object."""

    language = JsonAgentLanguage()
    invocation = language.parse_response('{"tool": "terminate"}')

    assert invocation == {"tool": "terminate", "args": {}}


def test_parse_response_rejects_invalid_json() -> None:
    """Invalid JSON should produce a clear ValueError."""

    language = JsonAgentLanguage()

    with pytest.raises(ValueError, match="valid JSON"):
        language.parse_response("not json")


def test_parse_response_rejects_non_object_args() -> None:
    """The args field must be an object, not a list or string."""

    language = JsonAgentLanguage()

    with pytest.raises(ValueError, match="args"):
        language.parse_response('{"tool": "terminate", "args": []}')
