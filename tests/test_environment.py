"""Tests for the GAME execution environment."""

from game import Action, Environment


def test_environment_returns_success_payload() -> None:
    """The environment should wrap successful action results consistently."""

    def greet(name: str) -> str:
        return f"Hello, {name}"

    action = Action(
        name="greet",
        function=greet,
        description="Greet a user.",
        parameters={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    )

    result = Environment().execute_action(action, {"name": "Victor"})

    assert result["tool_executed"] is True
    assert result["result"] == "Hello, Victor"
    assert "timestamp" in result


def test_environment_returns_error_payload() -> None:
    """The environment should catch action errors and return structured output."""

    def fail() -> None:
        raise RuntimeError("Something went wrong")

    action = Action(name="fail", function=fail, description="Always fail.")
    result = Environment().execute_action(action, {})

    assert result["tool_executed"] is False
    assert result["error"] == "Something went wrong"
    assert "traceback" in result
    assert "timestamp" in result
