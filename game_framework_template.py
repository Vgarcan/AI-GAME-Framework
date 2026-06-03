"""
Minimal GAME agent template.

Copy this file when starting a new exercise agent. The reusable framework
classes live in the ``game`` package; this file only shows how to assemble
one agent by defining goals, actions, a model provider selector, and a
small runnable entry point.

Typical exercise workflow:
    1. Copy this file into a new agent file.
    2. Replace the goals.
    3. Replace or add action functions.
    4. Register the new actions.
    5. Keep ``MODEL_PROVIDER=fake`` while testing the action flow.
    6. Change the provider only after the fake flow works.
"""

from __future__ import annotations

import json
import os

from game import (
    Action,
    ActionRegistry,
    Agent,
    Environment,
    Goal,
    JsonAgentLanguage,
)


DEFAULT_MODEL_PROVIDER = "fake"


def get_model_provider() -> str:
    """
    Return the configured model provider.

    The template defaults to ``fake`` so students can test the agent loop
    without setting API keys or running a local model server.

    Returns:
        Lowercase provider name, such as ``fake``, ``ollama``, ``openai``,
        ``litellm``, or ``local_http``.
    """
    return os.getenv("MODEL_PROVIDER", DEFAULT_MODEL_PROVIDER).strip().lower()


def should_show_model_prompt() -> bool:
    """
    Return whether the full prompt should be printed while learning.

    This is separate from provider selection. ``MODEL_PROVIDER`` decides
    where the response comes from. ``SHOW_MODEL_PROMPT`` only controls
    whether the prompt is printed for inspection.

    Returns:
        ``True`` when ``SHOW_MODEL_PROMPT=true`` is set in the environment.
    """
    return os.getenv("SHOW_MODEL_PROMPT", "false").strip().lower() == "true"


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


def generate_fake_response(prompt: str) -> str:
    """
    Return a deterministic fake model response for learning.

    Args:
        prompt: Full prompt built by the agent language layer.

    Returns:
        JSON string representing the selected tool invocation.
    """
    if should_show_model_prompt():
        print("\nPROMPT SENT TO MODEL:")
        print(prompt)

    return json.dumps({
        "tool": "terminate",
        "args": {
            "message": (
                "Template executed successfully using MODEL_PROVIDER=fake. "
                "Change MODEL_PROVIDER only after the fake action flow works."
            )
        },
    })


def generate_real_response(prompt: str, provider: str) -> str:
    """
    Placeholder for real model provider integrations.

    Args:
        prompt: Full prompt built by the agent language layer.
        provider: Configured model provider name.

    Returns:
        JSON string representing the selected tool invocation.

    Raises:
        NotImplementedError: Always, until a real provider client is added.
    """
    raise NotImplementedError(
        f"MODEL_PROVIDER='{provider}' is not implemented in this template yet. "
        "Use MODEL_PROVIDER=fake while learning, or add a real provider client."
    )


def generate_response(prompt: str) -> str:
    """
    Generate a model response using the configured provider.

    The template uses ``MODEL_PROVIDER=fake`` by default. This keeps the
    agent loop deterministic while learning. After the fake action flow
    works, add a real provider implementation and change ``MODEL_PROVIDER``.

    Args:
        prompt: Full prompt built by the agent language layer.

    Returns:
        JSON string representing the selected tool invocation.
    """
    provider = get_model_provider()

    if provider == "fake":
        return generate_fake_response(prompt)

    return generate_real_response(prompt=prompt, provider=provider)


def build_template_agent() -> Agent:
    """
    Create a minimal runnable agent using the GAME framework.

    This is the main function to adapt in the exercises. Most beginner
    agents can be built by changing this function, adding action functions,
    and keeping ``MODEL_PROVIDER=fake`` until the local action flow works.

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
