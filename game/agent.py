"""
Reusable GAME agent loop.

This module contains the central loop shared by every exercise agent. The
loop receives a user task, builds a prompt, asks the model for an action,
executes that action through the environment, stores the result in memory,
and repeats until a terminal action is selected.

Typical use:
    from game import Agent, Environment, JsonAgentLanguage

    agent = Agent(
        goals=goals,
        agent_language=JsonAgentLanguage(),
        action_registry=registry,
        generate_response=generate_response,
        environment=Environment(),
    )

    memory = agent.run("List the project files.")

In most exercises, you should not edit this file. Instead, create a copied
agent file from ``game_framework_template.py`` and change the goals, actions,
environment, or model response function there.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Callable, Dict, List, Optional

from game.actions import Action, ActionRegistry
from game.environment import Environment
from game.goals import Goal
from game.language import AgentLanguage
from game.memory import Memory

logger = logging.getLogger(__name__)


class Agent:
    """
    Reusable GAME-based agent loop.

    The agent coordinates goals, actions, memory, language, and
    environment. For most exercises, keep this class unchanged and adapt
    the components passed into it.
    """

    def __init__(
        self,
        goals: List[Goal],
        agent_language: AgentLanguage,
        action_registry: ActionRegistry,
        generate_response: Callable[[str], str],
        environment: Environment,
    ) -> None:
        """
        Create an agent.

        Args:
            goals: Goals used to guide model decisions.
            agent_language: Prompt builder and response parser.
            action_registry: Registered tools available to the model.
            generate_response: Callable that receives a prompt and returns
                a raw model response string.
            environment: Object responsible for executing actions.
        """
        self.goals = goals
        self.agent_language = agent_language
        self.actions = action_registry
        self.generate_response = generate_response
        self.environment = environment

    def set_current_task(self, memory: Memory, task: str) -> None:
        """
        Store the user's initial request in memory.

        Args:
            memory: Memory object for this run.
            task: User request passed into ``run``.
        """
        memory.add_memory({
            "type": "user",
            "content": task,
        })

    def construct_prompt(self, memory: Memory) -> str:
        """
        Build the full prompt for the model.

        Args:
            memory: Current memory state.

        Returns:
            Prompt created by the configured ``AgentLanguage``.
        """
        return self.agent_language.construct_prompt(
            goals=self.goals,
            actions=self.actions.get_actions(),
            memory=memory,
            environment=self.environment,
        )

    def get_action(self, response: str) -> tuple[Action, Dict[str, Any]]:
        """
        Parse the response and retrieve the requested action.

        Args:
            response: Raw model response.

        Returns:
            Tuple of the selected ``Action`` and parsed invocation.

        Raises:
            ValueError: If the model requested an unknown action.
        """
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
        """
        Store the model decision and environment result.

        Args:
            memory: Memory object for this run.
            response: Raw model response.
            result: Structured environment result.
        """
        memory.add_memory({
            "type": "assistant",
            "content": response,
        })

        memory.add_memory({
            "type": "environment",
            "content": json.dumps(result, ensure_ascii=False),
        })

    def update_error_memory(
        self,
        memory: Memory,
        response: str,
        error: Exception,
    ) -> None:
        """
        Store a parsing or action-selection error in memory.

        Args:
            memory: Memory object for this run.
            response: Raw model response that caused the error.
            error: Exception raised while parsing or selecting the action.
        """
        self.update_memory(
            memory=memory,
            response=response,
            result={
                "tool_executed": False,
                "error": str(error),
                "error_type": error.__class__.__name__,
            },
        )

    def run(
        self,
        user_input: str,
        memory: Optional[Memory] = None,
        max_iterations: int = 10,
    ) -> Memory:
        """
        Run the main agent loop.

        Args:
            user_input: Task or request from the user.
            memory: Optional existing memory. If omitted, a new one is
                created for this run.
            max_iterations: Safety limit to avoid infinite loops.

        Returns:
            Final memory after the loop stops.
        """
        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for iteration in range(1, max_iterations + 1):
            logger.info("Starting agent iteration %s", iteration)

            prompt = self.construct_prompt(memory)
            response = self.generate_response(prompt)

            try:
                action, invocation = self.get_action(response)
            except ValueError as exc:
                logger.warning("Agent response could not be executed: %s", exc)
                self.update_error_memory(memory, response, exc)
                break

            result = self.environment.execute_action(
                action=action,
                args=invocation["args"],
            )

            self.update_memory(memory, response, result)

            if action.terminal:
                logger.info("Terminal action executed. Stopping agent loop.")
                break

        return memory
