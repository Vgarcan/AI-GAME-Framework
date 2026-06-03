# 02. Understanding the Reusable GAME Template

## Table of Contents

1. What this chapter is for
2. The file you will edit
3. The parts of the template
4. The order of the file
5. What to change first
6. What to avoid changing at first
7. How goals become prompt instructions
8. How actions become model tools
9. How memory shows the loop working
10. How to test without a real model
11. How to create a new agent from the template
12. Common mistakes
13. Chapter summary

## 1. What this chapter is for

Chapter 01 explained the GAME Framework.

This chapter explains how that framework appears inside `game_framework_template.py`.

Before building the exercise agents, the reader should understand where each concept lives in the file and which parts are usually changed when creating a new agent.

## 2. The file you will edit

The main file is:

```text
game_framework_template.py
```

This file is both a learning tool and a reusable base.

When building an exercise agent, the safest workflow is:

1. Keep `game_framework_template.py` as the original reference.
2. Copy it into a new file for the exercise.
3. Edit the new file.
4. Run the new file.
5. Compare the result with the original template if something breaks.

For example:

```text
file_explorer_agent.py
code_reviewer_agent.py
conversation_log_agent.py
```

## 3. The parts of the template

The template contains these main parts:

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

Each one maps directly to the GAME idea:

| Template part | GAME role |
|---|---|
| `Goal` | Goals |
| `Action` and `ActionRegistry` | Actions |
| `Memory` | Memory |
| `Environment` | Environment |
| `AgentLanguage` and `JsonAgentLanguage` | Prompt and response format |
| `Agent` | Agent loop |

The lower part of the file contains the example actions, the fake model response, and the function that builds the default agent.

That lower part is where most beginner exercises will make changes.

## 4. The order of the file

The file is organized from general framework pieces to concrete example usage.

A helpful way to read it is:

1. `Goal`: how instructions are represented.
2. `Action`: how a callable tool is represented.
3. `ActionRegistry`: how tools are stored and found.
4. `Memory`: how history is stored.
5. `Environment`: how actions are executed.
6. `AgentLanguage`: how prompts and responses are handled.
7. `Agent`: how the loop runs.
8. Example functions: what the agent can actually do.
9. `generate_response()`: the fake model response.
10. `build_template_agent()`: where the example agent is assembled.
11. `__main__`: how the file runs from the terminal.

This order matters because it shows the difference between framework code and agent-specific code.

## 5. What to change first

When creating a new agent, start with the agent-specific parts.

Usually you change:

1. The `goals` list inside `build_template_agent()`.
2. The example action functions.
3. The `registry.register(...)` calls.
4. The fake response returned by `generate_response()`.
5. The `user_input` in the `__main__` block.

These changes are enough to create the first version of a new agent.

You do not need to redesign the whole framework for each exercise.

## 6. What to avoid changing at first

At the beginning, avoid changing:

1. `Agent.run()`
2. `Memory`
3. `ActionRegistry`
4. `JsonAgentLanguage.parse_response()`
5. The general shape of `Environment.execute_action()`

These parts are the reusable framework.

Later, you may improve them, but the first goal is to understand how far you can get by changing only the GAME components around the loop.

## 7. How goals become prompt instructions

Inside `build_template_agent()`, the template creates a list of `Goal` objects.

Those goals are later passed into the language layer.

`JsonAgentLanguage.construct_prompt()` turns them into text for the model.

This means the goals you write are not decorative. They become part of the model's instructions.

For example, a goal like:

```text
Do not edit files without approval.
```

can influence the model to choose `request_approval` before `apply_change`.

## 8. How actions become model tools

An action is created by wrapping a Python function in an `Action` object.

The action registration tells the model:

1. The action name.
2. What the action does.
3. Which arguments it expects.
4. Whether it ends the loop.

The registry is what connects a model response such as:

```json
{
  "tool": "read_file",
  "args": {
    "file_name": "README.md"
  }
}
```

to the actual Python function.

If the action is not registered, the agent cannot use it.

## 9. How memory shows the loop working

Memory is the easiest way to see the loop in action.

After a run, memory should contain:

1. The user input.
2. The model response.
3. The environment result.

This is why the template prints final memory at the end.

When learning, do not ignore that output. It shows how the agent moves from request to decision to result.

## 10. How to test without a real model

The template includes a fake `generate_response()` function.

This function returns JSON as if it came from a model.

That lets you test the framework before connecting OpenAI, Ollama, LiteLLM, or another provider.

For example, to test one action, return:

```json
{
  "tool": "terminate",
  "args": {
    "message": "Test complete."
  }
}
```

When building the exercise agents, change this fake response several times to test one action at a time.

This is a very useful learning habit because it separates framework debugging from model behavior.

## 11. How to create a new agent from the template

The repeatable process is:

1. Copy `game_framework_template.py` into a new file.
2. Rename `build_template_agent()` if that helps readability.
3. Replace the goals.
4. Replace or add action functions.
5. Register the new actions.
6. Test fake model responses.
7. Run the file.
8. Inspect memory.
9. Only then connect a real model.

That is the workflow used by the exercises in the next chapters.

## 12. Common mistakes

Common mistakes include:

1. Editing the loop before understanding the components.
2. Adding a function but forgetting to register it.
3. Registering an action with a schema that does not match the function.
4. Trying to connect a real model before the fake response works.
5. Ignoring memory output.
6. Treating goals as comments instead of model instructions.

Most early bugs come from mismatches between the action function, the action schema, and the JSON returned by the model.

## 13. Chapter summary

The template is the practical foundation of the guide.

It gives you a reusable loop and a clear place to define goals, actions, memory behavior, environment behavior, and model communication.

The next chapters use this same template repeatedly. Each exercise changes the GAME components while keeping the core loop familiar.
