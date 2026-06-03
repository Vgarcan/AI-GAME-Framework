# GAME Agent Framework Template

This repository is a study guide for learning how to design AI agents with the **GAME Framework**.

The material assumes basic Python knowledge only. You do not need to know the framework in advance.

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

## Project structure

The reusable framework lives in the `game/` package:

```text
game/
  goals.py
  actions.py
  memory.py
  environment.py
  language.py
  agent.py
```

The editable starter file is:

```text
game_framework_template.py
```

The framework modules provide the reusable GAME pieces:

| Component | Purpose |
|---|---|
| `Goal` | Defines what the agent should achieve |
| `Action` | Defines a tool the agent can use |
| `ActionRegistry` | Stores and retrieves available actions |
| `Memory` | Stores conversation and execution history |
| `Environment` | Executes actions and returns structured results |
| `AgentLanguage` | Builds prompts and parses model responses |
| `Agent` | Runs the reusable agent loop |

The template imports those pieces and shows how to assemble one runnable agent. The chapter files under `_docs/` are guided builds. They show how to copy and edit the template step by step to create each agent.

---

## Requirements

Before running anything, install Python and the project dependencies.

You will need:

- Python installed on your machine
- Access to a terminal
- The packages listed in `requirements.txt`

---

## Installation

From the project root:

```bash
python -m venv .venv
```
Or:

```bash
py -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```
Or:

```cmd
.\.venv\Scripts\activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

If your system uses `py` instead of `python`, replace the command accordingly.

Create your local environment file when you are ready to connect a real model provider:

```bash
copy .env.example .env
```

The example file documents values such as `OPENAI_API_KEY`, `SERVER_URL`, `MODEL_PROVIDER`, and `MODEL_NAME`. Keep real secrets in `.env`, not in `.env.example`.

---

## How to run it

From the terminal:

```bash
python game_framework_template.py
```

The default version does not call a real LLM yet. Instead, `generate_response()` returns a fake terminal action so you can test the framework safely before connecting a model.

---

## How to read the guide

Start with the chapters in `_docs/` in numerical order. Each chapter explains one part of the framework and uses the previous chapter as context.

The study flow is:

```text
1. Read the chapter
2. Study the example
3. Copy `game_framework_template.py` into a new exercise file
4. Modify one GAME component at a time in that exercise file
5. Run the agent and inspect the output
6. Observe memory to understand the loop
```

---

## How to adapt it

To create a new agent, you usually only need to change:

```text
1. goals
2. actions
3. action registry
4. environment
5. generate_response()
```

You normally should not need to change the `Agent.run()` loop.

In the modular version, `Agent.run()` lives in `game/agent.py`. Most exercises should leave it alone and work in the copied agent file instead.

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

## Exercises to try next

Once the first run works, try these study exercises:

```text
Add JSON schema validation
Add persistent memory
Connect a real model provider
Add file-system actions
Add GitHub actions
Add Django-specific actions
Add approval-required actions
Add tests
Study the conversation log generator guide
```

---

## File

Main template:

```text
game_framework_template.py
```

Framework package:

```text
game/
```
