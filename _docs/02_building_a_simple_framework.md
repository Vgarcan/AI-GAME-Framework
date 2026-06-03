# 02. Understanding the Modular GAME Template

## Table of Contents

1. What this chapter is for
2. Why the project is modular
3. The files in the framework package
4. The role of the template file
5. What to edit when creating an agent
6. What to leave stable at first
7. How goals become prompt instructions
8. How actions become model tools
9. How memory shows the loop working
10. How to test without a real model
11. How `.env.example` fits into the project
12. How to create a new agent from the template
13. Common mistakes
14. Chapter summary

## 1. What this chapter is for

Chapter 01 explained the GAME Framework.

This chapter explains how the project is organized in code.

The important change is that the framework is now modular. The reusable classes live in the `game/` package, while `game_framework_template.py` is a small editable starter file.

That separation makes the guide easier to study because the reader can see the difference between framework code and agent-specific code.

## 2. Why the project is modular

The first version of a teaching template can live in one file.

But once the file grows too much, it becomes harder to learn from it. A student has to scroll through framework classes, example actions, fake model responses, and the runnable entry point all at once.

The modular version solves that by separating responsibilities:

1. `game/` contains the reusable framework.
2. `game_framework_template.py` shows how to assemble one agent.
3. Exercise files copy the template and change the agent-specific pieces.

This structure matches the GAME idea itself: each part has a clear responsibility.

## 3. The files in the framework package

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

## 4. The role of the template file

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
2. A fake `generate_response()` function.
3. `build_template_agent()`.
4. A small `__main__` block for running the file.

That means the template is no longer the entire framework. It is a small example agent that uses the framework.

This is exactly what the later exercises need.

## 5. What to edit when creating an agent

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
4. The fake response returned by `generate_response()`.
5. The `user_input` in the `__main__` block.

Those changes are enough to build the first version of each exercise agent.

## 6. What to leave stable at first

At the beginning, avoid changing the framework package.

In particular, leave these stable:

1. `game/agent.py`
2. `game/memory.py`
3. `game/actions.py`
4. `game/language.py`
5. `game/environment.py`

Later, you may improve them, especially when building stricter environments or more advanced memory.

But while learning the basic pattern, the point is to see how much you can achieve by changing only the copied agent file.

## 7. How goals become prompt instructions

Inside the template builder function, the agent creates a list of `Goal` objects.

Those goals are passed into `JsonAgentLanguage`.

The language layer turns them into prompt text for the model.

This means goals are not comments. They are part of the instructions the model sees.

For example:

```text
Do not edit files without approval.
```

That goal can guide the model toward `request_approval` before `apply_change`.

## 8. How actions become model tools

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

If the function exists but is not registered, the agent cannot use it.

## 9. How memory shows the loop working

Memory is the easiest way to see the agent loop working.

After a run, memory should contain:

1. The user input.
2. The model response.
3. The environment result.

The template prints final memory at the end so the student can inspect what happened.

When learning, this output matters. It shows how the agent moves from request to decision to result.

## 10. How to test without a real model

The template includes a fake `generate_response()` function.

This function returns JSON as if it came from a model.

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

When building the exercise agents, change this fake response several times to test one action at a time.

This separates framework debugging from model behavior.

## 11. How `.env.example` fits into the project

The template does not need real API credentials while you are testing fake responses.

When you are ready to connect a real provider, create a local `.env` file from the example:

```text
copy .env.example .env
```

The `.env.example` file documents the configuration values the project may need:

```text
OPENAI_API_KEY
SERVER_URL
MODEL_PROVIDER
MODEL_NAME
```

Use `.env.example` as documentation and `.env` as your private local configuration.

The real `.env` file should not be committed. It may contain secrets such as API keys.

At this stage of the guide, the most important rule is simple: get the fake `generate_response()` flow working first, then add real provider configuration.

## 12. How to create a new agent from the template

The repeatable process is:

1. Copy `game_framework_template.py` into a new file.
2. Rename the builder function if that helps readability.
3. Replace the goals.
4. Replace or add action functions.
5. Register the new actions.
6. Test fake model responses.
7. Run the file.
8. Inspect memory.
9. Copy `.env.example` to `.env` if the agent needs a real provider.
10. Only then connect a real model.

That is the workflow used by the exercises in the next chapters.

## 13. Common mistakes

Common mistakes include:

1. Editing `game/agent.py` before understanding the template.
2. Adding a function but forgetting to register it.
3. Registering an action with a schema that does not match the function.
4. Trying to connect a real model before the fake response works.
5. Ignoring memory output.
6. Treating goals as comments instead of prompt instructions.
7. Putting real API keys in `.env.example`.

Most early bugs come from mismatches between the action function, the action schema, and the JSON returned by the model.

## 14. Chapter summary

The project now has two layers.

The `game/` package contains the reusable framework.

The `game_framework_template.py` file contains a small example agent that imports and uses that framework.

The `.env.example` file documents provider configuration without exposing private values.

The next chapters copy the template into new agent files and change only the GAME components needed for each exercise.
