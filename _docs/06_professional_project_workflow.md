# 06. Professional Project Workflow for the GAME Framework

## Table of Contents

1. [Purpose of this chapter](#1-purpose-of-this-chapter)
2. [Why the project now needs a professional workflow](#2-why-the-project-now-needs-a-professional-workflow)
3. [The difference between framework code and project support files](#3-the-difference-between-framework-code-and-project-support-files)
4. [Why dependencies are split into separate files](#4-why-dependencies-are-split-into-separate-files)
5. [How `pyproject.toml` fits into the project](#5-how-pyprojecttoml-fits-into-the-project)
6. [Why tests matter for AI agent projects](#6-why-tests-matter-for-ai-agent-projects)
7. [What the current tests check](#7-what-the-current-tests-check)
8. [How to run the project locally](#8-how-to-run-the-project-locally)
9. [How to run the tests](#9-how-to-run-the-tests)
10. [How examples fit into the learning path](#10-how-examples-fit-into-the-learning-path)
11. [How safety improved in the framework](#11-how-safety-improved-in-the-framework)
12. [How to keep the documentation aligned with the code](#12-how-to-keep-the-documentation-aligned-with-the-code)
13. [Recommended next improvements](#13-recommended-next-improvements)
14. [Chapter summary](#14-chapter-summary)

## 1. Purpose of this chapter

The first chapters explain the AI agent design idea behind the GAME Framework.

This chapter explains how to maintain the repository as a real Python project.

That matters because an AI agent project is still a software project. Even if the core idea is about models, prompts, tools, and memory, the code still needs structure, tests, dependency management, clear installation steps, and safe development habits.

The goal is not to over-engineer the project. The goal is to introduce professional habits early, while the framework is still small enough to understand.

## 2. Why the project now needs a professional workflow

At the beginning, the project only needed a guide and a simple template.

Now the repository contains more than learning text:

```text
game/                         reusable framework package
game_framework_template.py     starter agent template
examples/                      runnable example agents
tests/                         automated tests
pyproject.toml                 Python project configuration
requirements.txt               minimal runtime requirements
requirements-ai.txt            optional AI provider requirements
requirements-dev.txt           development requirements
.env.example                   local configuration example
LICENSE                        project license
```

This means the repository has become a small but real Python package.

That changes how we should think about it.

Before, the main question was:

```text
Can I understand the agent loop?
```

Now we also ask:

```text
Can I install it, test it, extend it, and avoid breaking it?
```

That is why professional project workflow belongs in the documentation.

## 3. The difference between framework code and project support files

The `game/` package is the framework itself.

It contains the reusable GAME components:

```text
game/goals.py
game/actions.py
game/memory.py
game/environment.py
game/language.py
game/agent.py
game/__init__.py
```

These files define the reusable pattern.

Project support files are different. They do not define the agent loop directly, but they make the project easier to install, test, maintain, and share.

Examples:

| File or folder | Purpose |
|---|---|
| `pyproject.toml` | Defines project metadata and tool configuration |
| `requirements-dev.txt` | Installs development tools such as pytest, ruff, and mypy |
| `requirements-ai.txt` | Installs optional AI integration packages |
| `tests/` | Protects framework behaviour with automated checks |
| `examples/` | Shows how the framework is used in practical agents |
| `.gitignore` | Prevents local files, secrets, and build output from being committed |
| `.env.example` | Documents local environment variables without exposing secrets |

A professional project separates these concerns.

The agent framework should stay focused on GAME.

The support files should make the framework easier to use safely.

## 4. Why dependencies are split into separate files

The core framework currently uses only the Python standard library.

That is useful for learning because a student can run the basic template without installing a large AI stack.

The dependency files are now split by purpose:

```text
requirements.txt
requirements-ai.txt
requirements-dev.txt
```

The purpose of this split is clarity.

### `requirements.txt`

This is the minimal runtime file.

At the moment, it does not need external packages because the base framework uses standard Python modules such as `json`, `logging`, `time`, and `pathlib`.

This keeps the beginner path simple.

### `requirements-ai.txt`

This file is for optional model provider integrations.

It includes packages that may be useful when connecting the framework to real model providers:

```text
litellm
openai
python-dotenv
requests
tiktoken
```

These packages are not required to understand the agent loop.

They become relevant when replacing the fake `generate_response()` function with a real model call.

### `requirements-dev.txt`

This file is for development tools:

```text
pytest
ruff
mypy
```

These tools help you test and maintain the project.

They are not part of the agent logic itself.

This split is professional because it avoids forcing every user to install everything.

## 5. How `pyproject.toml` fits into the project

`pyproject.toml` is the standard configuration file for modern Python projects.

In this repository, it gives the project an identity:

```text
name
version
description
Python version
package discovery
pytest configuration
ruff configuration
mypy configuration
```

The most practical benefit is editable installation.

From the repository root, you can run:

```bash
pip install -e .
```

This tells Python to treat the local project as an installed package while still using the files in your working directory.

That is useful because examples and tests can import from `game` cleanly:

```python
from game import Action, ActionRegistry, Agent, Environment, Goal, JsonAgentLanguage
```

Without a project configuration, students often fight import errors instead of learning the agent design.

## 6. Why tests matter for AI agent projects

AI projects can feel unpredictable because models do not always respond the same way.

That makes automated tests even more important.

A good habit is to separate two kinds of behaviour:

```text
Deterministic framework behaviour
Model behaviour
```

Framework behaviour should be testable.

Examples:

1. An action should execute its Python function.
2. A missing required argument should be rejected.
3. Invalid JSON should be handled clearly.
4. The environment should return structured success and error payloads.
5. The agent loop should stop when a terminal action runs.

Model behaviour can be tested later with integration tests, but the basic framework should not depend on a real model just to prove that it works.

This is why the template starts with fake model responses.

The fake response makes the loop deterministic while learning.

## 7. What the current tests check

The current test suite is organised around the main framework components.

```text
tests/test_actions.py
tests/test_language.py
tests/test_environment.py
tests/test_agent.py
```

### `tests/test_actions.py`

This checks that actions execute correctly and validate arguments.

It also checks that the registry does not silently overwrite an action with the same name.

That matters because duplicate action names can create confusing agent behaviour.

### `tests/test_language.py`

This checks JSON response parsing.

The framework expects a model response like:

```json
{
  "tool": "terminate",
  "args": {
    "message": "Done"
  }
}
```

The tests make sure invalid JSON or invalid `args` values fail clearly.

### `tests/test_environment.py`

This checks that the environment returns structured results.

A successful action should return a success payload.

A failing action should return an error payload instead of crashing without context.

### `tests/test_agent.py`

This checks the reusable loop.

It confirms that the agent stops after a terminal action and stores invalid model-response errors in memory.

This is important because memory is how we inspect what happened during a run.

## 8. How to run the project locally

Create a virtual environment:

```bash
python -m venv .venv
```

On Windows, you may prefer:

```bash
py -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project in editable mode:

```bash
pip install -e .
```

Run the base template:

```bash
python game_framework_template.py
```

Run the file explorer example:

```bash
python examples/file_explorer_agent.py
```

At this stage, no real model provider is required.

The fake `generate_response()` function is enough to prove that the framework loop can run.

## 9. How to run the tests

Install the development tools:

```bash
pip install -r requirements-dev.txt
```

Run the tests:

```bash
pytest
```

Run the linter:

```bash
ruff check .
```

Run type checking on the framework package:

```bash
mypy game
```

A useful development habit is:

```text
Change one small thing.
Run tests.
Fix errors.
Commit.
```

That habit is especially useful in AI projects, because it stops framework bugs from being confused with model behaviour.

## 10. How examples fit into the learning path

The `examples/` folder is different from the `_docs/` folder.

The documentation explains the concepts.

The examples show runnable versions of those concepts.

The current example is:

```text
examples/file_explorer_agent.py
```

It demonstrates the same GAME pattern from Chapter 03:

| GAME component | File explorer example |
|---|---|
| Goals | Explore project files safely and answer clearly |
| Actions | `list_files`, `read_file`, `terminate` |
| Memory | Default in-memory history |
| Environment | Default execution environment |

This example still uses a fake model response.

That is deliberate. A deterministic example is better for learning the framework mechanics.

Later examples can connect to Ollama, LiteLLM, or another provider.

## 11. How safety improved in the framework

The framework now includes a small amount of built-in argument validation.

When an action is registered, it includes a schema-like structure:

```python
parameters={
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"],
}
```

The `Action` class now checks two simple things:

1. Required arguments are present.
2. Unknown arguments are rejected when properties are defined.

This is not a full JSON Schema implementation.

It is a lightweight teaching version.

The professional reason is clear: the model should not be able to send arbitrary arguments into Python functions without checks.

The next step would be to use the `jsonschema` package for deeper validation, such as data types, enums, minimum lengths, and nested objects.

## 12. How to keep the documentation aligned with the code

Documentation becomes outdated when the code evolves and the guide is not updated.

A simple maintenance rule is:

```text
When a project structure changes, update README.md.
When a learning concept changes, update _docs/.
When runnable behaviour changes, update examples/ and tests/.
```

For this repository, the documentation should stay aligned with these areas:

1. Framework modules in `game/`.
2. Template behaviour in `game_framework_template.py`.
3. Example agents in `examples/`.
4. Installation commands in `README.md`.
5. Test commands and expected workflow.
6. Optional AI provider setup.
7. Safety rules around actions and environments.

This is also how professional teams work.

Documentation is not something written once at the end. It is part of the project lifecycle.

## 13. Recommended next improvements

The next improvements should be added gradually.

Good next steps are:

1. Add a GitHub Actions workflow to run tests automatically.
2. Add an Ollama integration example.
3. Add a LiteLLM integration example.
4. Add a stricter file environment that prevents unsafe paths.
5. Add persistent JSON memory.
6. Add a `CONTRIBUTING.md` file explaining how to work on the repo.
7. Add a `CHANGELOG.md` file to track important updates.

The order matters.

Before connecting real models, the framework should be stable and tested.

Before adding dangerous tools, the environment should be stricter.

Before inviting other users to contribute, the workflow should be documented.

## 14. Chapter summary

The GAME Framework is now more than a single learning script.

It is a small Python project with framework code, documentation, tests, examples, dependency separation, and project configuration.

That is a good direction because AI agents should be built with normal software engineering discipline.

The key professional habit is:

```text
Keep the agent loop simple.
Keep the project maintainable.
Keep documentation aligned with code.
Test deterministic behaviour before blaming the model.
```

This chapter connects the learning framework to real development practice.
