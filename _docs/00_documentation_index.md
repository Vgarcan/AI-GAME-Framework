# 00. Documentation Index

## Table of Contents

1. [Purpose of this index](#1-purpose-of-this-index)
2. [Recommended reading order](#2-recommended-reading-order)
3. [How the documentation is organised](#3-how-the-documentation-is-organised)
4. [How to use the code while reading](#4-how-to-use-the-code-while-reading)
5. [When to update the documentation](#5-when-to-update-the-documentation)

## 1. Purpose of this index

This file is the navigation point for the study guide.

The repository has grown from a simple learning template into a small Python project with framework code, examples, tests, dependency files, and project configuration.

Because of that, the documentation now has two jobs:

1. Teach AI agent concepts using the GAME Framework.
2. Explain how to maintain the repository as a professional Python project.

## 2. Recommended reading order

Read the chapters in this order:

1. [Introduction to AI Agents and the GAME Framework](01_game_framework_introduction.md)
2. [Understanding the Modular GAME Template](02_building_a_simple_framework.md)
3. [Building a File Explorer Agent](03_file_explorer_agent_game.md)
4. [Building a Code Reviewer Agent](04_code_reviewer_agent_game.md)
5. [Building a Conversation Log Generator](05_conversation_log_generator_game.md)
6. [Professional Project Workflow for the GAME Framework](06_professional_project_workflow.md)

## 3. How the documentation is organised

The first five chapters focus on agent design.

They explain how the GAME components work:

| GAME component | Main question |
|---|---|
| Goals | What should the agent achieve? |
| Actions | What can the agent do? |
| Memory | What should the agent remember? |
| Environment | Where are actions executed and controlled? |

Chapter 06 focuses on project maintenance.

It explains:

1. Dependency separation.
2. `pyproject.toml`.
3. Tests.
4. Examples.
5. Code quality tools.
6. Documentation alignment.
7. Safe next improvements.

## 4. How to use the code while reading

The recommended learning flow is:

```text
Read the theory.
Inspect the related framework module.
Run the template or example.
Inspect memory output.
Run tests after changing code.
Only then connect a real model provider.
```

Useful commands:

```bash
pip install -e .
pip install -r requirements-dev.txt
python game_framework_template.py
python examples/file_explorer_agent.py
pytest
```

The core learning flow uses fake model responses first. That is intentional because deterministic behaviour is easier to debug.

## 5. When to update the documentation

Update the documentation whenever the project structure or learning flow changes.

Use this rule:

```text
If the code changes how students use the project, update README.md or _docs/.
If the framework behaviour changes, update tests and the relevant chapter.
If a new example is added, link it from this index and explain its learning purpose.
```

This keeps the guide useful as the framework grows.
