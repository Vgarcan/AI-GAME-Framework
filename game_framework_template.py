"""
Minimal GAME agent template.

Copy this file when starting a new exercise agent. The reusable framework
classes live in the ``game`` package; this file only shows how to assemble
one agent by defining goals, actions, a model response function, and a
small runnable entry point.

Typical exercise workflow:
    1. Copy this file into a new agent file.
    2. Replace the goals.
    3. Replace or add action functions.
    4. Register the new actions.
    5. Test with fake JSON responses in ``generate_response``.
    6. Connect a real model only after the fake flow works.
"""

from __future__ import annotations

import json

from game import (
    Action,
    ActionRegistry,
    Agent,
    Environment,
    Goal,
    JsonAgentLanguage,
)


def say(message: str) -> str:
    """
    Return a message unchanged.

    Args:
        message: Text to return to the user.

    Returns:
        The same message.

    Example:
        message = say("hello")
    """
    return message


def terminate(message: str) -> str:
    """
    Return the final message for a terminal action.

    Args:
        message: Final text to return.

    Returns:
        The final message.

    Example:
        final_message = terminate("Task complete.")
    """
    return message


def generate_response(prompt: str) -> str:
    """
    Fake model response used while learning the framework.

    Args:
        prompt: Full prompt built by the agent language layer.

    Returns:
        JSON string representing the selected tool invocation.

    Replace this function with a real call to Ollama, LiteLLM, OpenAI,
    Anthropic, or your own endpoint when the local flow works.

    Example:
        A real implementation still needs to return a JSON string like:
        ``{"tool": "terminate", "args": {"message": "Done."}}``
    """
    print("\nPROMPT SENT TO MODEL:")
    print(prompt)

    return json.dumps({
        "tool": "terminate",
        "args": {
            "message": (
                "Template executed successfully. Replace generate_response "
                "with your LLM client."
            )
        },
    })


def build_template_agent() -> Agent:
    """
    Create a minimal runnable agent using the GAME framework.

    This is the main function to adapt in the exercises. Most beginner
    agents can be built by changing this function, adding action
    functions, and editing ``generate_response`` for testing.

    Returns:
        Configured ``Agent`` instance.

    Example:
        agent = build_template_agent()
    """
    goals = [
        Goal(
            priority=1,
            name="Respond to the user",
            description="Help the user using the available actions.",
        ),
        Goal(
            priority=2,
            name="Terminate correctly",
            description="Use the terminate action when the task is complete.",
        ),
    ]

    registry = ActionRegistry()

    registry.register(Action(
        name="say",
        function=say,
        description="Return a message to the user.",
        parameters={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message that will be returned to the user.",
                }
            },
            "required": ["message"],
        },
        terminal=False,
    ))

    registry.register(Action(
        name="terminate",
        function=terminate,
        description="End the agent loop with a final message.",
        parameters={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Final message for the user.",
                }
            },
            "required": ["message"],
        },
        terminal=True,
    ))

    return Agent(
        goals=goals,
        agent_language=JsonAgentLanguage(),
        action_registry=registry,
        generate_response=generate_response,
        environment=Environment(),
    )


if __name__ == "__main__":
    agent = build_template_agent()
    final_memory = agent.run(
        user_input="Test the agent using the GAME template.",
        max_iterations=5,
    )

    print("\nFINAL MEMORY:")
    for item in final_memory.get_memories():
        print(item)
