"""
Memory storage for GAME agents.

This module defines the "M" in GAME. Memory is the record of what happened
during an agent run: user input, model decisions, and environment results.

Typical use:
    from game import Memory

    memory = Memory()
    memory.add_memory({"type": "user", "content": "List the files."})
    recent_entries = memory.get_memories(limit=5)

The default memory is intentionally simple for study purposes. Later, it can
be replaced with database storage, JSON files, Redis, or another persistence
layer without changing the main agent loop.
"""

from __future__ import annotations

from typing import Dict, List, Optional


class Memory:
    """
    Simple in-memory history for the agent loop.

    Memory stores the user request, model decisions, and environment
    results. This lets the model see what happened in previous steps.

    Example:
        memory = Memory()
        memory.add_memory({"type": "user", "content": "List files."})
        entries = memory.get_memories()
    """

    def __init__(self) -> None:
        self.items: List[Dict[str, str]] = []

    def add_memory(self, memory: Dict[str, str]) -> None:
        """
        Add one entry to memory.

        Args:
            memory: Dictionary with at least ``type`` and ``content`` keys.
        """
        self.items.append(memory)

    def get_memories(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Return stored memory entries.

        Args:
            limit: Optional maximum number of recent entries to return.

        Returns:
            All memory entries, or only the last ``limit`` entries.
        """
        if limit is None:
            return self.items

        return self.items[-limit:]
