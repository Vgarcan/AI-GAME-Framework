"""Tests for the reusable GAME agent loop."""

import json

from game import Action, ActionRegistry, Agent, Environment, Goal, JsonAgentLanguage


def build_registry() -> ActionRegistry:
    """Create a small registry used by the agent tests."""

    def terminate(message: str) -> str:
        return message

    registry = ActionRegistry()
    registry.register(Action(
        name="terminate",
        function=terminate,
        description="End the loop.",
        parameters={
            "type": "object",
            "properties": {"message": {"type": "string"}},
            "required": ["message"],
        },
        terminal=True,
    ))
    return registry


def test_agent_stops_after_terminal_action() -> None:
    """The agent should stop when a terminal action is selected."""

    def fake_model_response(prompt: str) -> str:
        return json.dumps({
            "tool": "terminate",
            "args": {"message": "Done"},
        })

    agent = Agent(
        goals=[Goal(1, "Finish", "Complete the task.")],
        agent_language=JsonAgentLanguage(),
        action_registry=build_registry(),
        generate_response=fake_model_response,
        environment=Environment(),
    )

    memory = agent.run("Test the loop", max_iterations=5)
    memories = memory.get_memories()

    assert len(memories) == 3
    assert memories[0]["type"] == "user"
    assert memories[-1]["type"] == "environment"
    assert "Done" in memories[-1]["content"]


def test_agent_stores_response_error_in_memory() -> None:
    """Invalid model output should be captured in memory instead of crashing."""

    def bad_model_response(prompt: str) -> str:
        return "not json"

    agent = Agent(
        goals=[Goal(1, "Finish", "Complete the task.")],
        agent_language=JsonAgentLanguage(),
        action_registry=build_registry(),
        generate_response=bad_model_response,
        environment=Environment(),
    )

    memory = agent.run("Test bad output", max_iterations=5)
    memories = memory.get_memories()

    assert len(memories) == 3
    assert memories[-1]["type"] == "environment"
    assert "ValueError" in memories[-1]["content"]
    assert "valid JSON" in memories[-1]["content"]
