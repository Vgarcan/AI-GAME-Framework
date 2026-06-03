"""Tests for the template model provider selector."""

import json

import pytest

import game_framework_template as template


def test_get_model_provider_defaults_to_fake(monkeypatch: pytest.MonkeyPatch) -> None:
    """The template should use the fake provider when no env var is set."""

    monkeypatch.delenv("MODEL_PROVIDER", raising=False)

    assert template.get_model_provider() == "fake"


def test_get_model_provider_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """The provider should be configurable through MODEL_PROVIDER."""

    monkeypatch.setenv("MODEL_PROVIDER", " OpenAI ")

    assert template.get_model_provider() == "openai"


def test_should_show_model_prompt_defaults_to_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Prompt display should be disabled by default."""

    monkeypatch.delenv("SHOW_MODEL_PROMPT", raising=False)

    assert template.should_show_model_prompt() is False


def test_should_show_model_prompt_can_be_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Prompt display should be enabled with SHOW_MODEL_PROMPT=true."""

    monkeypatch.setenv("SHOW_MODEL_PROMPT", "true")

    assert template.should_show_model_prompt() is True


def test_generate_response_uses_fake_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    """The default provider should return a valid fake tool invocation."""

    monkeypatch.setenv("MODEL_PROVIDER", "fake")
    response = template.generate_response("test prompt")
    invocation = json.loads(response)

    assert invocation["tool"] == "terminate"
    assert "MODEL_PROVIDER=fake" in invocation["args"]["message"]


def test_generate_response_rejects_unimplemented_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A real provider should fail clearly until it is implemented."""

    monkeypatch.setenv("MODEL_PROVIDER", "openai")

    with pytest.raises(NotImplementedError, match="not implemented"):
        template.generate_response("test prompt")
