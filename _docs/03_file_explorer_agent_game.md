# 03. Building a File Explorer Agent from the GAME Template

## Table of Contents

1. What you will build
2. How this exercise uses the template
3. Step 1: copy the template as a working file
4. Step 2: rewrite the goals
5. Step 3: create the real action functions
6. Step 4: register the actions
7. Step 5: keep the environment responsible for execution
8. Step 6: update the fake model response
9. Step 7: run the agent and inspect memory
10. What this exercise teaches
11. Common mistakes
12. Chapter summary

## 1. What you will build

In this exercise, you will use `game_framework_template.py` as the starting point for a file explorer agent.

The agent should be able to:

1. List files in a project directory.
2. Read a selected file.
3. Return the result in a structured way.
4. Stop when the user request has been answered.

The purpose is not to create a perfect filesystem assistant. The purpose is to practice changing the GAME components while leaving the main agent loop stable.

## 2. How this exercise uses the template

The template imports the framework from the `game/` package:

```text
Goal
Action
ActionRegistry
Memory
Environment
AgentLanguage
Agent
```

For this exercise, you should not rewrite the framework from zero.

Instead, you adapt these parts:

1. The `goals` list inside `build_template_agent()`.
2. The example action functions near the bottom of the file.
3. The `registry.register(...)` calls.
4. The fake `generate_response()` function used for testing.
5. The `user_input` inside the `__main__` block.

The `Agent.run()` method in `game/agent.py` should stay the same.

## 3. Step 1: copy the template as a working file

Keep the original template as a reference.

Create a new file for this exercise, for example:

```text
file_explorer_agent.py
```

Then copy the contents of `game_framework_template.py` into that file.

This gives you a safe place to modify the agent while preserving the base template and the reusable `game/` package.

## 4. Step 2: rewrite the goals

Find `build_template_agent()`.

Inside that function, replace the generic goals with goals for filesystem exploration.

A good first version is:

```text
Goal 1: Explore the current project safely.
Goal 2: Read only files that are useful for the user request.
Goal 3: Stop when the requested information has been provided.
```

These goals teach the agent what kind of behavior matters.

The important idea is this: goals are not just labels. They shape the prompt that the model sees, so they influence which action the model chooses next.

## 5. Step 3: create the real action functions

The template starts with simple example functions such as `say()` and `terminate()`.

For the file explorer, add functions such as:

```text
list_files()
read_file(file_name)
terminate(message)
```

The function responsibilities should stay small:

1. `list_files()` returns file names.
2. `read_file(file_name)` returns the contents of one file.
3. `terminate(message)` returns the final message.

At this stage, avoid making one function do too much. A common beginner mistake is creating one large function that lists, reads, summarizes, and stops. That hides the agent loop instead of teaching it.

## 6. Step 4: register the actions

After the functions exist, register them in the `ActionRegistry`.

Each action registration should include:

1. `name`
2. `function`
3. `description`
4. `parameters`
5. `terminal`

For example, `list_files` does not need arguments, so its schema can have an empty `properties` object.

`read_file` does need an argument, so its schema should describe `file_name`.

This is where the model learns how to call your tools. If the schema is unclear, the model is more likely to send the wrong arguments.

## 7. Step 5: keep the environment responsible for execution

Do not put filesystem logic inside `Agent.run()`.

The loop should remain generic:

```text
model chooses action -> registry finds action -> environment executes action
```

The environment is the execution boundary. It calls the selected action and formats the result.

For this first version, the default `Environment` class is enough. Later, you can create a stricter environment that limits which directory the agent can read.

## 8. Step 6: update the fake model response

The copied agent file uses `generate_response()` as a fake model call.

This is useful while learning because you can test the framework without connecting a real LLM.

Start by making `generate_response()` return a fixed action:

```json
{
  "tool": "list_files",
  "args": {}
}
```

After that works, test `read_file` with:

```json
{
  "tool": "read_file",
  "args": {
    "file_name": "README.md"
  }
}
```

Finally, test `terminate`.

Testing one action at a time makes it much easier to understand how the registry, environment, and memory connect.

## 9. Step 7: run the agent and inspect memory

Update the `user_input` in the `__main__` block.

For example:

```text
List the files in this project.
```

Run the file from the terminal.

Watch three things:

1. The prompt sent to the model.
2. The selected action.
3. The final memory entries.

The memory should show the user request, the model decision, and the environment result. This is where the exercise becomes concrete: you can see GAME working step by step.

## 10. What this exercise teaches

This exercise teaches the first practical GAME pattern:

1. Goals tell the agent what matters.
2. Actions describe what the agent can do.
3. Memory stores what happened.
4. Environment executes the selected action.
5. The loop stays reusable.

The key lesson is that you created a new agent mostly by changing the components around the loop, not by rewriting the loop itself.

## 11. Common mistakes

Common mistakes in this exercise include:

1. Editing `game/agent.py` too early.
2. Forgetting to register a new action.
3. Giving `read_file` a schema that does not match the function argument.
4. Trying to test every action at once.
5. Letting the agent read arbitrary paths before adding safety rules.

Keep the first version small. Once the basic loop works, safety and extra actions become easier to add.

## 12. Chapter summary

The file explorer agent is the first full template adaptation.

You start with `game_framework_template.py`, copy it into a new exercise file, rewrite the goals, add filesystem action functions, register those actions, test fake model responses, and inspect memory. The reusable framework stays in `game/`.

That process is the central habit of this guide: use GAME to understand what changes and what stays stable.
