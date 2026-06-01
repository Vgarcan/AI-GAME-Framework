# GAME Agent Framework Template

A small reusable Python template for building AI agents using the **GAME Framework**.

GAME stands for:

```text
G = Goals
A = Actions
M = Memory
E = Environment
```

The main idea is simple:

```text
Keep the agent loop stable.
Change the GAME components to create different agents.
```

---

## What this template includes

The file `game_framework_template_commented.py` includes:

```text
Goal
Action
ActionRegistry
Memory
Environment
AgentLanguage
JsonAgentLanguage
Agent
generate_response()
build_template_agent()
```

Each component has a clear responsibility:

| Component | Purpose |
|---|---|
| `Goal` | Defines what the agent should achieve |
| `Action` | Defines a tool the agent can use |
| `ActionRegistry` | Stores and retrieves available actions |
| `Memory` | Stores conversation and execution history |
| `Environment` | Executes actions and returns structured results |
| `AgentLanguage` | Builds prompts and parses model responses |
| `Agent` | Runs the reusable agent loop |

---

## How to run it

From the terminal:

```bash
python game_framework_template_commented.py
```

The default version does not call a real LLM yet.

Instead, `generate_response()` returns a fake terminal action so you can test that the framework works.

---

## How to adapt it

To create a new agent, usually you only need to change:

```text
1. goals
2. actions
3. action registry
4. environment
5. generate_response()
```

You normally should not need to change the `Agent.run()` loop.

---

## Example workflow

A typical loop works like this:

```text
1. User provides a task
2. Agent stores the task in memory
3. Agent builds a prompt from Goals, Actions and Memory
4. LLM chooses one action
5. Agent parses the response
6. Environment executes the action
7. Result is stored back in memory
8. Loop continues until a terminal action is selected
```

---

## Replacing the fake LLM call

Replace this function:

```python
def generate_response(prompt: str) -> str:
    ...
```

With your real model call.

For example, you could connect:

```text
Ollama
LiteLLM
OpenAI API
Anthropic
A local HTTP endpoint
A custom internal AI service
```

The function must return a JSON string like this:

```json
{
  "tool": "terminate",
  "args": {
    "message": "Task completed."
  }
}
```

---

## Creating a new action

Example:

```python
def list_files() -> list[str]:
    """Return a list of files in the current directory."""
    return os.listdir(".")
```

Then register it:

```python
registry.register(
    Action(
        name="list_files",
        function=list_files,
        description="Return a list of files in the current directory.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        terminal=False,
    )
)
```

---

## Important safety notes

For agents that can modify files, run commands, send emails, or call external APIs:

```text
Add human approval before dangerous actions.
Use max_iterations to avoid infinite loops.
Validate model arguments before executing tools.
Log all action calls and results.
Test with fake environments before using real data.
```

---

## Suggested next improvements

Possible improvements:

```text
Add JSON schema validation
Add persistent memory
Add Ollama integration
Add LiteLLM integration
Add file-system actions
Add GitHub actions
Add Django-specific actions
Add approval-required actions
Add tests
```

---

## File

Main template:

```text
game_framework_template_commented.py
```
