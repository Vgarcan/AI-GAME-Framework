"""Tests for GAME actions and action registries."""

import pytest

from game import Action, ActionRegistry


def test_action_executes_wrapped_function() -> None:
    """An Action should call its wrapped Python function with valid args."""

    def echo(message: str) -> str:
        return message

    action = Action(
        name="echo",
        function=echo,
        description="Return a message.",
        parameters={
            "type": "object",
            "properties": {"message": {"type": "string"}},
            "required": ["message"],
        },
    )

    assert action.execute(message="hello") == "hello"


def test_action_rejects_missing_required_arguments() -> None:
    """An Action should fail clearly when a required argument is missing."""

    def echo(message: str) -> str:
        return message

    action = Action(
        name="echo",
        function=echo,
        description="Return a message.",
        parameters={
            "type": "object",
            "properties": {"message": {"type": "string"}},
            "required": ["message"],
        },
    )

    with pytest.raises(ValueError, match="Missing required argument"):
        action.execute()


def test_action_rejects_unknown_arguments() -> None:
    """An Action should fail clearly when the model sends unknown args."""

    def echo(message: str) -> str:
        return message

    action = Action(
        name="echo",
        function=echo,
        description="Return a message.",
        parameters={
            "type": "object",
            "properties": {"message": {"type": "string"}},
            "required": ["message"],
        },
    )

    with pytest.raises(ValueError, match="Unknown argument"):
        action.execute(message="hello", extra="not allowed")


def test_registry_rejects_duplicate_action_names() -> None:
    """The registry should not silently overwrite an existing action."""

    def noop() -> None:
        return None

    registry = ActionRegistry()
    action = Action(name="noop", function=noop, description="Do nothing.")

    registry.register(action)

    with pytest.raises(ValueError, match="Action already registered"):
        registry.register(action)
