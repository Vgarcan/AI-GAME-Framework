"""
GAME Framework Template
=======================

Reusable skeleton for building agents with the GAME Framework.

GAME:
    G = Goals / Instructions
    A = Actions / Available tools
    M = Memory / Conversation history
    E = Environment / Execution environment

This file is intended as a starting point for study projects,
proofs of concept, or small internal frameworks.
"""

from __future__ import annotations

import json
import time
import traceback
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass(frozen=True)
class Goal:
    """Represents an agent goal or instruction."""

    priority: int
    name: str
    description: str


class Action:
    """Represents a tool the agent can use."""

    def __init__(
        self,
        name: str,
        function: Callable[..., Any],
        description: str,
        parameters: Optional[Dict[str, Any]] = None,
        terminal: bool = False,
    ) -> None:
        self.name = name
        self.function = function
        self.description = description
        self.parameters = parameters or {
            "type": "object",
            "properties": {},
            "required": [],
        }
        self.terminal = terminal

    def execute(self, **args: Any) -> Any:
        """Execute the function associated with this action."""
        return self.function(**args)

    def to_prompt_schema(self) -> Dict[str, Any]:
        """Return a prompt-friendly representation of the action."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "terminal": self.terminal,
        }


class ActionRegistry:
    """Central registry of actions available to an agent."""

    def __init__(self) -> None:
        self._actions: Dict[str, Action] = {}

    def register(self, action: Action) -> None:
        """Add an action to the registry."""
        self._actions[action.name] = action

    def get_action(self, name: str) -> Optional[Action]:
        """Return an action by name."""
        return self._actions.get(name)

    def get_actions(self) -> List[Action]:
        """Return all registered actions."""
        return list(self._actions.values())


class Memory:
    """Simple memory backed by a list of messages."""

    def __init__(self) -> None:
        self.items: List[Dict[str, str]] = []

    def add_memory(self, memory: Dict[str, str]) -> None:
        """Add one entry to memory."""
        self.items.append(memory)

    def get_memories(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Return stored memories.

        If limit is set, return only the last N entries.
        """
        if limit is None:
            return self.items

        return self.items[-limit:]


class Environment:
    """Executes actions and returns structured results."""

    def execute_action(self, action: Action, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action and capture any errors."""
        try:
            result = action.execute(**args)
            return self.format_result(result)
        except Exception as exc:
            return {
                "tool_executed": False,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "timestamp": self.current_timestamp(),
            }

    def format_result(self, result: Any) -> Dict[str, Any]:
        """Format an action result."""
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": self.current_timestamp(),
        }

    def current_timestamp(self) -> str:
        """Return a timestamp string."""
        return time.strftime("%Y-%m-%dT%H:%M:%S%z")


class AgentLanguage:
    """Base class for building prompts and parsing responses."""

    def construct_prompt(
        self,
        goals: List[Goal],
        actions: List[Action],
        memory: Memory,
        environment: Environment,
    ) -> str:
        raise NotImplementedError

    def parse_response(self, response: str) -> Dict[str, Any]:
        raise NotImplementedError


class JsonAgentLanguage(AgentLanguage):
    """
    Simple language where the model responds with JSON.

    Expected format:
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
        """Convert the model JSON response into an invocation."""
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


class Agent:
    """Reusable GAME-based agent."""

    def __init__(
        self,
        goals: List[Goal],
        agent_language: AgentLanguage,
        action_registry: ActionRegistry,
        generate_response: Callable[[str], str],
        environment: Environment,
    ) -> None:
        self.goals = goals
        self.agent_language = agent_language
        self.actions = action_registry
        self.generate_response = generate_response
        self.environment = environment

    def set_current_task(self, memory: Memory, task: str) -> None:
        """Store the user's initial request."""
        memory.add_memory({
            "type": "user",
            "content": task,
        })

    def construct_prompt(self, memory: Memory) -> str:
        """Build the full prompt for the model."""
        return self.agent_language.construct_prompt(
            goals=self.goals,
            actions=self.actions.get_actions(),
            memory=memory,
            environment=self.environment,
        )

    def get_action(self, response: str) -> tuple[Action, Dict[str, Any]]:
        """Parse the response and retrieve the requested action."""
        invocation = self.agent_language.parse_response(response)
        action_name = invocation["tool"]

        action = self.actions.get_action(action_name)

        if action is None:
            raise ValueError(f"Unknown action requested by model: {action_name}")

        return action, invocation

    def update_memory(
        self,
        memory: Memory,
        response: str,
        result: Dict[str, Any],
    ) -> None:
        """Store the agent decision and the environment result."""
        memory.add_memory({
            "type": "assistant",
            "content": response,
        })

        memory.add_memory({
            "type": "environment",
            "content": json.dumps(result, ensure_ascii=False),
        })

    def run(
        self,
        user_input: str,
        memory: Optional[Memory] = None,
        max_iterations: int = 10,
    ) -> Memory:
        """Run the main agent loop."""
        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for iteration in range(1, max_iterations + 1):
            print(f"\n--- Iteration {iteration} ---")

            prompt = self.construct_prompt(memory)

            response = self.generate_response(prompt)
            print(f"Agent decision: {response}")

            action, invocation = self.get_action(response)

            result = self.environment.execute_action(
                action=action,
                args=invocation["args"],
            )
            print(f"Action result: {result}")

            self.update_memory(memory, response, result)

            if action.terminal:
                print("Terminal action executed. Stopping agent loop.")
                break

        return memory


def say(message: str) -> str:
    """Simple example action."""
    return message


def terminate(message: str) -> str:
    """Example terminal action."""
    return message


def generate_response(prompt: str) -> str:
    """
    Placeholder for connecting your AI model.

    Replace this function with a real call to Ollama, LiteLLM,
    OpenAI, Anthropic, or your own endpoint.
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
        }
    })


def build_template_agent() -> Agent:
    """Create a minimal agent using the template."""

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
