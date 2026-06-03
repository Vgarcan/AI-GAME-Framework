"""
Reusable GAME Framework building blocks.

This package is the public import point for the guide. Exercise agents can
usually import from ``game`` instead of importing from each individual
module.

Typical use:
    from game import Action, ActionRegistry, Agent, Environment
    from game import Goal, JsonAgentLanguage

    registry = ActionRegistry()
    goals = [Goal(1, "Respond", "Help the user with available actions.")]

    agent = Agent(
        goals=goals,
        agent_language=JsonAgentLanguage(),
        action_registry=registry,
        generate_response=generate_response,
        environment=Environment(),
    )

The framework package should stay mostly stable during the beginner
exercises. Most changes belong in the copied agent file created from
``game_framework_template.py``.
"""

from game.actions import Action, ActionRegistry
from game.agent import Agent
from game.environment import Environment
from game.goals import Goal
from game.language import AgentLanguage, JsonAgentLanguage
from game.memory import Memory

__all__ = [
    "Action",
    "ActionRegistry",
    "Agent",
    "AgentLanguage",
    "Environment",
    "Goal",
    "JsonAgentLanguage",
    "Memory",
]
