"""
Prompt construction and response parsing for GAME agents.

This module controls how the agent talks to the model. It turns goals,
actions, and memory into a prompt, then parses the model response back into
an action invocation.

Typical use:
    from game import JsonAgentLanguage

    language = JsonAgentLanguage()
    prompt = language.construct_prompt(goals, actions, memory, environment)
    invocation = language.parse_response('{"tool": "terminate", "args": {}}')

The default ``JsonAgentLanguage`` is intentionally simple. It expects the
model to return JSON with ``tool`` and ``args``. More advanced projects can
replace it with function calling, tool calling, or provider-specific logic.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from game.actions import Action
from game.environment import Environment
from game.goals import Goal
from game.memory import Memory


class AgentLanguage:
    """
    Base class for prompt construction and response parsing.

    Different model providers may use different formats. This interface
    lets the agent loop stay the same while the language layer changes.
    """

    def construct_prompt(
        self,
        goals: List[Goal],
        actions: List[Action],
        memory: Memory,
        environment: Environment,
    ) -> str:
        """
        Build the prompt sent to the model.

        Args:
            goals: Goals that should guide the model.
            actions: Actions available to the model.
            memory: Current agent memory.
            environment: Execution environment, included for extensibility.

        Returns:
            Prompt string to send to the model.
        """
        raise NotImplementedError

    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse a model response into an action invocation.

        Args:
            response: Raw model response.

        Returns:
            Dictionary containing at least ``tool`` and ``args``.
        """
        raise NotImplementedError


class JsonAgentLanguage(AgentLanguage):
    """
    Simple language where the model responds with JSON.

    Expected model format:
        {
            "tool": "action_name",
            "args": {}
        }
    """

    def construct_prompt(
        self,
        goals: List[Goal],
        actions: List[Action],
        memory: Memory,
        environment: Environment,
    ) -> str:
        """
        Build a JSON-oriented prompt for the model.

        Args:
            goals: Goals sorted by priority before being shown.
            actions: Registered actions exposed as tool schemas.
            memory: Recent memory entries included as context.
            environment: Execution environment, unused in this simple
                implementation but part of the shared interface.

        Returns:
            Prompt instructing the model to choose exactly one action and
            respond only with valid JSON.
        """
        sorted_goals = sorted(goals, key=lambda goal: goal.priority)

        goals_text = "\n".join(
            f"{goal.priority}. {goal.name}: {goal.description}"
            for goal in sorted_goals
        )

        actions_text = json.dumps(
            [action.to_prompt_schema() for action in actions],
            indent=2,
            ensure_ascii=False,
        )

        memory_text = json.dumps(
            memory.get_memories(limit=20),
            indent=2,
            ensure_ascii=False,
        )

        return f"""
You are an AI agent using the GAME Framework.

GOALS:
{goals_text}

AVAILABLE ACTIONS:
{actions_text}

MEMORY:
{memory_text}

RESPONSE FORMAT:
You must respond only with valid JSON using this schema:

{{
  "tool": "action_name",
  "args": {{}}
}}

Choose exactly one action.
Do not include markdown.
Do not include explanations outside the JSON.
""".strip()

    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Convert the model JSON response into an invocation.

        Args:
            response: Raw response expected to be valid JSON.

        Returns:
            Dictionary with ``tool`` and ``args`` keys.

        Raises:
            ValueError: If the response is not valid JSON, has no ``tool``,
                or contains non-object ``args``.
        """
        try:
            invocation = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"The model did not return valid JSON. Raw response: {response}"
            ) from exc

        if "tool" not in invocation:
            raise ValueError("The response must include a 'tool' field.")

        if "args" not in invocation:
            invocation["args"] = {}

        if not isinstance(invocation["args"], dict):
            raise ValueError("The 'args' field must be an object.")

        return invocation
