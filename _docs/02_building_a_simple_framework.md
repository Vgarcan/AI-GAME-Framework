# 02. Understanding the Modular GAME Template

## Table of Contents

1. [What this chapter is for](#1-what-this-chapter-is-for)
2. [Why the project is modular](#2-why-the-project-is-modular)
3. [The AI reason behind each module](#3-the-ai-reason-behind-each-module)
4. [The files in the framework package](#4-the-files-in-the-framework-package)
5. [The role of the template file](#5-the-role-of-the-template-file)
6. [What to edit when creating an agent](#6-what-to-edit-when-creating-an-agent)
7. [What to leave stable at first](#7-what-to-leave-stable-at-first)
8. [How goals become prompt instructions](#8-how-goals-become-prompt-instructions)
9. [How actions become model tools](#9-how-actions-become-model-tools)
10. [How memory becomes usable context](#10-how-memory-becomes-usable-context)
11. [How language defines the response contract](#11-how-language-defines-the-response-contract)
12. [How environment protects execution](#12-how-environment-protects-execution)
13. [How model provider selection works](#13-how-model-provider-selection-works)
14. [How to test without a real model](#14-how-to-test-without-a-real-model)
15. [How `.env.example` fits into the project](#15-how-envexample-fits-into-the-project)
16. [How to create a new agent from the template](#16-how-to-create-a-new-agent-from-the-template)
17. [Common mistakes](#17-common-mistakes)
18. [Chapter summary](#18-chapter-summary)

## 1. What this chapter is for

Chapter 01 explained why AI agents need structure.

This chapter explains how that structure appears in code.

The important idea is that the framework is modular because an agent has several different responsibilities. If all of those responsibilities are mixed into one file, it becomes harder to understand what the model is doing, what the program is doing, and where safety rules should live.

The reusable classes live in the `game/` package.

The editable starter agent lives in:

```text
game_framework_template.py
```

That separation makes the guide easier to study because you can see the difference between framework code and agent-specific code.

## 2. Why the project is modular

The first version of a teaching template can live in one file.

But once the file grows too much, it becomes harder to learn from it. A student has to scroll through framework classes, example actions, fake model responses, provider configuration, and the runnable entry point all at once.

The modular version solves that by separating responsibilities:

1. `game/` contains the reusable framework.
2. `game_framework_template.py` shows how to assemble one agent.
3. `examples/` contains runnable example agents.
4. `_docs/` explains the theory and workflow.
5. `tests/` protects important framework behaviour.

This structure is not only cleaner Python. It also matches how AI agents need to be designed.

A model needs instructions, tool descriptions, memory, response format, and execution boundaries. Each module helps represent one of those needs clearly.

## 3. The AI reason behind each module

The framework modules are not arbitrary.

Each one answers a practical AI design question:

| AI design question | Module | Why it exists |
|---|---|---|
| What should the model try to achieve? | `goals.py` | Stores purpose and behaviour instructions |
| What can the model request? | `actions.py` | Defines tools and their argument schemas |
| What happened already? | `memory.py` | Stores previous requests, decisions, and results |
| How should the prompt and response be shaped? | `language.py` | Builds the model prompt and parses structured output |
| Where do actions actually run? | `environment.py` | Executes or rejects tool calls |
| How does the repeated process run? | `agent.py` | Coordinates the loop |

This is the central bridge between AI theory and the framework.

The model is not magic. It needs information arranged in a useful way. The `game/` package gives us that arrangement.

## 4. The files in the framework package

The reusable framework lives in:

```text
game/
```

The package contains:

```text
game/goals.py
game/actions.py
game/memory.py
game/environment.py
game/language.py
game/agent.py
game/__init__.py
```

Each module has one job:

| File | Purpose |
|---|---|
| `goals.py` | Defines `Goal` objects |
| `actions.py` | Defines `Action` and `ActionRegistry` |
| `memory.py` | Defines the in-memory history |
| `environment.py` | Executes actions and formats results |
| `language.py` | Builds prompts and parses model responses |
| `agent.py` | Contains the reusable agent loop |
| `__init__.py` | Re-exports the main classes for easier imports |

In the exercises, you will usually import from `game` instead of editing these files.

## 5. The role of the template file

The starter file is:

```text
game_framework_template.py
```

This file imports the reusable classes:

```python
from game import Action, ActionRegistry, Agent, Environment, Goal, JsonAgentLanguage
```

Then it defines:

1. Example action functions.
2. Provider helper functions.
3. A fake provider response.
4. A placeholder for real providers.
5. `build_template_agent()`.
6. A small `__main__` block for running the file.

That means the template is not the entire framework. It is a small example agent that uses the framework.

The current template no longer expects the student to immediately replace `generate_response()` manually. Instead, it uses provider selection:

```text
MODEL_PROVIDER=fake
```

The idea is:

```text
Keep the fake provider while learning.
Change provider only after the action flow works.
```

## 6. What to edit when creating an agent

When creating a new agent, copy `game_framework_template.py` into a new file.

For example:

```text
file_explorer_agent.py
code_reviewer_agent.py
conversation_log_agent.py
```

Then change the agent-specific parts:

1. The goals inside the builder function.
2. The action functions.
3. The `registry.register(...)` calls.
4. The fake provider response if you need a different test action.
5. The `user_input` in the `__main__` block.

Those changes are enough to build the first version of each exercise agent.

You usually should not change the reusable agent loop just to create a new agent.

## 7. What to leave stable at first

At the beginning, avoid changing the framework package.

In particular, leave these stable:

1. `game/agent.py`
2. `game/memory.py`
3. `game/actions.py`
4. `game/language.py`
5. `game/environment.py`

Later, you may improve them, especially when building stricter environments or more advanced memory.

But while learning the basic pattern, the point is to see how much you can achieve by changing only the copied agent file.

## 8. How goals become prompt instructions

Inside the template builder function, the agent creates a list of `Goal` objects.

Those goals are passed into `JsonAgentLanguage`.

The language layer turns them into prompt text for the model.

This means goals are not comments. They are part of the instructions the model sees.

For example:

```text
Do not edit files without approval.
```

That goal can guide the model toward `request_approval` before `apply_change`.

The theory behind this is simple: a model can only follow instructions that are actually present in the context it receives.

If a safety rule is not in the prompt and not enforced by the environment, the agent is more likely to behave unpredictably.

## 9. How actions become model tools

An action starts as a normal Python function.

Then it becomes a model-available tool when it is registered as an `Action`.

The registration tells the model:

1. The action name.
2. What the action does.
3. Which arguments it expects.
4. Whether it ends the loop.

The registry connects this model response:

```json
{
  "tool": "read_file",
  "args": {
    "file_name": "README.md"
  }
}
```

to the actual Python function.

The current `Action` class also performs lightweight argument validation. It checks required arguments and rejects unexpected arguments when the schema defines known properties.

This matters because an AI model cannot safely improvise access to your system. The framework must describe and validate the available tools clearly.

## 10. How memory becomes usable context

Memory is the easiest way to see the agent loop working.

After a run, memory should contain:

1. The user input.
2. The model response.
3. The environment result.

When learning, this output matters. It shows how the agent moves from request to decision to result.

Memory is also how the agent avoids acting as if every step is the first step.

For example, if the model already called `list_files`, the next prompt can include that result. Then the model can choose `read_file` instead of listing files again.

This is not the same as assuming the model remembers everything internally. The program stores useful state and shows it to the model when needed.

## 11. How language defines the response contract

The language layer builds the prompt and parses the model response.

In this project, the model is expected to return JSON:

```json
{
  "tool": "terminate",
  "args": {
    "message": "Task complete."
  }
}
```

This response contract is necessary because the program needs to understand the model's output.

If the model returns a normal paragraph, the framework may not know which action to execute.

The language layer gives the model a clear format:

```text
Choose one tool.
Return valid JSON.
Include arguments under `args`.
```

This is one of the most practical lessons in agent design: useful AI systems often depend on structured outputs, not just fluent text.

## 12. How environment protects execution

The environment is where selected actions actually run.

The model can request an action, but the environment should decide whether that action is allowed.

For a simple template, the default environment can execute registered actions directly.

For safer agents, the environment should become stricter.

Examples:

1. A file explorer environment can block paths outside the project.
2. A code reviewer environment can block edits without approval.
3. A transcript processor environment can reject empty transcripts.
4. A command-running environment can require human confirmation.

This separation is a major AI safety pattern.

The model proposes the next step.
The system controls execution.

## 13. How model provider selection works

The template uses provider selection instead of asking the student to rewrite the model function immediately.

The key setting is:

```text
MODEL_PROVIDER=fake
```

The default fake provider returns deterministic JSON. This allows you to test the agent loop without API keys, local servers, or model SDKs.

The template separates two ideas:

| Setting | Purpose |
|---|---|
| `MODEL_PROVIDER` | Selects where the model response comes from |
| `SHOW_MODEL_PROMPT` | Decides whether to print the full prompt for inspection |

This is why the setting is not called `debug`.

Debugging and provider selection are different concerns.

For more detail, read [Model Provider Selection](07_model_provider_selection.md).

## 14. How to test without a real model

The template includes a fake provider response.

This returns JSON as if it came from a model.

That lets you test the framework before connecting OpenAI, Ollama, LiteLLM, or another provider.

For example:

```json
{
  "tool": "terminate",
  "args": {
    "message": "Test complete."
  }
}
```

When building exercise agents, change the fake response several times to test one action at a time.

This separates framework debugging from model behaviour.

That separation matters because real models introduce uncertainty. If the code is already confusing before the model is connected, debugging becomes much harder.

## 15. How `.env.example` fits into the project

The template does not need real API credentials while you are testing fake responses.

The `.env.example` file documents the configuration values the project may need:

```text
MODEL_PROVIDER=fake
SHOW_MODEL_PROMPT=false
OPENAI_API_KEY
SERVER_URL
MODEL_NAME
```

Important note: the current template reads environment variables with `os.getenv()`.

That means `.env.example` documents expected values, but copying it to `.env` does not automatically load those values unless a loader such as `python-dotenv` is added later.

For now, keep `MODEL_PROVIDER=fake` while learning or set environment variables directly in your shell.

## 16. How to create a new agent from the template

The repeatable process is:

1. Copy `game_framework_template.py` into a new file.
2. Rename the builder function if that helps readability.
3. Replace the goals.
4. Replace or add action functions.
5. Register the new actions.
6. Keep `MODEL_PROVIDER=fake` while testing.
7. Run the file.
8. Inspect memory.
9. Add provider configuration only after the fake action flow works.
10. Run tests after changing framework behaviour.

That is the workflow used by the exercises in the next chapters.

## 17. Common mistakes

Common mistakes include:

1. Editing `game/agent.py` before understanding the template.
2. Adding a function but forgetting to register it.
3. Registering an action with a schema that does not match the function.
4. Trying to connect a real model before the fake provider flow works.
5. Ignoring memory output.
6. Treating goals as comments instead of prompt instructions.
7. Putting real API keys in `.env.example`.
8. Letting the model's text output be too free-form for the program to parse.
9. Confusing `MODEL_PROVIDER=fake` with debug mode.
10. Assuming `.env` is automatically loaded when no loader has been added.

Most early bugs come from mismatches between the action function, the action schema, and the JSON returned by the model.

## 18. Chapter summary

The project now has several layers.

The `game/` package contains the reusable framework.

The `game_framework_template.py` file contains a small example agent that imports and uses that framework.

The template uses `MODEL_PROVIDER=fake` by default so students can test deterministic behaviour before connecting a real model.

The modules exist because AI agents need separate pieces for instructions, tools, memory, response format, execution, and loop control.

The `.env.example` file documents provider configuration without exposing private values.

The next chapters copy the template into new agent files or inspect existing examples and change only the GAME components needed for each exercise.
