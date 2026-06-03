"""
Execution environment for GAME agents.

This module defines the "E" in GAME. The model can request an action, but
the environment is responsible for executing that action and returning a
structured result.

Typical use:
    from game import Environment

    environment = Environment()
    result = environment.execute_action(action, {"message": "hello"})

For simple exercises, the default environment is enough. For safer agents,
such as a code reviewer, create a stricter environment that checks paths,
permissions, approval state, or other rules before executing risky actions.
"""

from __future__ import annotations

import time
import traceback
from typing import Any, Dict

from game.actions import Action


class Environment:
    """
    Executes actions and returns structured results.

    The model chooses an action, but the environment calls the Python
    function and catches errors. Safer agents can subclass or replace this
    class to enforce permissions.
    """

    def execute_action(self, action: Action, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an action and capture any errors.

        Args:
            action: The action selected by the model.
            args: Arguments parsed from the model response.

        Returns:
            A structured dictionary with execution status, result or error,
            and timestamp.
        """
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
        """
        Format a successful action result.

        Args:
            result: Value returned by the executed action.

        Returns:
            A structured success payload.
        """
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": self.current_timestamp(),
        }

    def current_timestamp(self) -> str:
        """
        Return a timestamp string for environment results.

        Returns:
            Current local time formatted as ``YYYY-MM-DDTHH:MM:SS+offset``.
        """
        return time.strftime("%Y-%m-%dT%H:%M:%S%z")
