# AI Agent Study Guide with the GAME Framework

This repository is a study guide for learning how AI agents work and how to build them in Python.

The **GAME Framework** is not the main topic by itself. It is the structure used in this project to practice AI agent design in a repeatable way.

The guide teaches two things together:

1. The AI concepts behind agents.
2. The GAME structure used to turn those concepts into working code.

The material assumes basic Python knowledge only. You should be comfortable with functions, classes, dictionaries, lists, and modules. You do not need previous experience building agents.

---

## What This Guide Is Really About

Large language models do not automatically know your project, your files, your tools, or your rules.

They need useful context.
They need clear instructions.
They need a safe list of actions.
They need memory of what has already happened.
They need an environment that controls what can actually be executed.

That is why this project uses GAME.

GAME stands for:

```text
G = Goals
A = Actions
M = Memory
E = Environment
```

These four ideas map directly to the practical needs of an AI agent:

| AI need | GAME component | What it provides |
|---|---|---|
| The model needs a purpose | Goals | Clear instructions and priorities |
| The model needs controlled abilities | Actions | Named tools with descriptions and schemas |
| The model needs working context | Memory | A record of requests, decisions, and results |
| The system needs safety and execution | Environment | The boundary where actions actually run |

The main habit you will practice is:

```text
Keep the agent loop stable.
Change the GAME components to create different agents.
```

---

## Project Structure

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
| `Goal` | Defines what the agent should achieve and how it should behave |
| `Action` | Defines a tool the model is allowed to request |
| `ActionRegistry` | Stores and retrieves available actions |
| `Memory` | Stores conversation and execution history |
| `Environment` | Executes actions and returns structured results |
| `AgentLanguage` | Builds prompts and parses model responses |
| `Agent` | Runs the reusable decision loop |

The template imports those pieces and shows how to assemble one runnable agent. The chapter files under `_docs/` explain the AI theory first, then show how to edit the template step by step.

---

## Requirements

Before running anything, install Python and the project dependencies.

You will need:

1. Python installed on your machine.
2. Access to a terminal.
3. The packages listed in `requirements.txt`.

---

## Installation

From the project root, create a virtual environment:

```bash
python -m venv .venv
```

If your system uses the Windows Python launcher, use:

```bash
py -m venv .venv
```

Activate the virtual environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or activate it in Command Prompt:

```cmd
.\.venv\Scripts\activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Create your local environment file when you are ready to connect a real model provider:

```bash
copy .env.example .env
```

The example file documents values such as `OPENAI_API_KEY`, `SERVER_URL`, `MODEL_PROVIDER`, and `MODEL_NAME`.

Keep real secrets in `.env`, not in `.env.example`.

---

## How To Run The Template

From the terminal:

```bash
python game_framework_template.py
```

The default version does not call a real LLM yet.

Instead, `generate_response()` returns a fake model response. This is intentional. It lets you understand the agent loop before adding the uncertainty of a real model.

---

## How To Read The Guide

Start with the chapters in `_docs/` in numerical order.

Each chapter follows the same study pattern:

1. Explain the AI idea.
2. Explain why that idea matters for agents.
3. Show how GAME represents the idea in code.
4. Edit a copied version of the template.
5. Run the result and inspect memory.

The study flow is:

```text
1. Read the theory.
2. Identify the GAME components.
3. Copy `game_framework_template.py` into a new exercise file.
4. Modify one GAME component at a time.
5. Run the agent with fake model responses.
6. Inspect memory to understand the loop.
7. Connect a real model only after the controlled flow works.
```

---

## How AI Agents Work In This Project

A typical agent loop works like this:

```text
1. User provides a task.
2. Agent stores the task in memory.
3. Agent builds a prompt from goals, actions, and memory.
4. Model selects one action.
5. Agent parses the model response.
6. Environment executes the selected action.
7. Result is stored back in memory.
8. Loop continues until a terminal action is selected.
```

This loop is stable because it is the general pattern.

The behavior changes because each agent has different goals, actions, memory needs, and environment rules.

---

## Replacing The Fake LLM Call

The template contains this function:

```python
def generate_response(prompt: str) -> str:
    ...
```

Replace it only after the fake action flow works.

You can connect:

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

This response format matters because the model is not executing Python directly. It is choosing a structured action for the framework to execute.

---

## Important Safety Notes

Agents that can modify files, run commands, send emails, or call external APIs need extra safeguards.

Use these rules:

```text
Add human approval before dangerous actions.
Use max_iterations to avoid infinite loops.
Validate model arguments before executing tools.
Log all action calls and results.
Test with fake environments before using real data.
```

The model can request an action.
The environment decides whether the action is allowed.

That distinction is one of the most important ideas in the guide.

---

## Chapters

Read these in order:

```text
01. Introduction to AI Agents and the GAME Framework
02. Understanding the Modular GAME Template
03. Building a File Explorer Agent
04. Building a Code Reviewer Agent
05. Building a Conversation Log Generator
```

Open them here:

1. [Introduction to AI Agents and the GAME Framework](_docs/01_game_framework_introduction.md)
2. [Understanding the Modular GAME Template](_docs/02_building_a_simple_framework.md)
3. [Building a File Explorer Agent](_docs/03_file_explorer_agent_game.md)
4. [Building a Code Reviewer Agent](_docs/04_code_reviewer_agent_game.md)
5. [Building a Conversation Log Generator](_docs/05_conversation_log_generator_game.md)

The exercises are not random projects. They are different ways to practice the same AI agent concepts:

```text
File explorer: controlled tool use and external context
Code reviewer: safety, approval, and execution boundaries
Conversation log generator: relevance, memory, and structured extraction
```

---

## Main Files

Template:

```text
game_framework_template.py
```

Framework package:

```text
game/
```

Study guide:

```text
_docs/
```
