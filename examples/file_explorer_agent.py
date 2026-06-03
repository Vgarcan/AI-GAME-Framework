"""
Example file explorer agent built with the GAME framework.

This example is intentionally small. It shows how to reuse the stable agent
loop while changing the GAME components around it:

G = goals focused on exploring files safely
A = list_files, read_file, terminate
M = default in-memory run history
E = default execution environment

The model response is still fake so the example remains deterministic while
learning. Replace ``generate_response`` only after the local action flow is
understood.
"""

from __future__ import annotations

import json
from pathlib import Path

from game import Action, ActionRegistry, Agent, Environment, Goal, JsonAgentLanguage

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def list_files() -> list[str]:
    """
    Return visible files in the project root.

    Returns:
        Sorted list of non-hidden file and folder names.
    """
    return sorted(
        path.name
        for path in PROJECT_ROOT.iterdir()
        if not path.name.startswith(".")
    )


def read_file(file_name: str) -> str:
    """
    Read a text file from the project root.

    Args:
        file_name: Name of the file to read. Nested paths are blocked in this
            beginner example to keep file access simple and safe.

    Returns:
        Text content from the requested file.

    Raises:
        ValueError: If a nested or absolute path is requested.
        FileNotFoundError: If the file does not exist.
    """
    requested_path = Path(file_name)

    if requested_path.is_absolute() or len(requested_path.parts) != 1:
        raise ValueError("Only root-level file names are allowed in this example.")

    file_path = PROJECT_ROOT / requested_path
    return file_path.read_text(encoding="utf-8")


def terminate(message: str) -> str:
    """
    Return the final answer and end the loop.

    Args:
        message: Final message for the user.

    Returns:
        The final message.
    """
    return message


def generate_response(prompt: str) -> str:
    """
    Fake model response for deterministic learning.

    Args:
        prompt: Full prompt built by the agent.

    Returns:
        JSON string selecting one action.
    """
    return json.dumps({
        "tool": "terminate",
        "args": {
            "message": "File explorer example is wired correctly. Replace the fake response to make it interactive."
        },
    })


def build_file_explorer_agent() -> Agent:
    """
    Build a small file explorer agent.

    Returns:
        Configured GAME Agent.
    """
    goals = [
        Goal(
            priority=1,
            name="Explore project files safely",
            description="Use only the registered file actions and avoid unsafe paths.",
        ),
        Goal(
            priority=2,
            name="Answer clearly",
            description="Use terminate when enough information has been gathered.",
        ),
    ]

    registry = ActionRegistry()
    registry.register(Action(
        name="list_files",
        function=list_files,
        description="List visible files and folders in the project root.",
        parameters={"type": "object", "properties": {}, "required": []},
    ))
    registry.register(Action(
        name="read_file",
        function=read_file,
        description="Read one root-level text file by file name.",
        parameters={
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Root-level file name to read, such as README.md.",
                }
            },
            "required": ["file_name"],
        },
    ))
    registry.register(Action(
        name="terminate",
        function=terminate,
        description="End the loop with a final answer.",
        parameters={
            "type": "object",
            "properties": {"message": {"type": "string"}},
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
    agent = build_file_explorer_agent()
    final_memory = agent.run("List the files in this project.")

    for item in final_memory.get_memories():
        print(item)
