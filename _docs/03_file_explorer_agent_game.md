# 03. Building a File Explorer Agent from the GAME Template

## Table of Contents

1. [What you will build](#1-what-you-will-build)
2. [The AI theory: models need external context](#2-the-ai-theory-models-need-external-context)
3. [How this exercise uses the template and the example folder](#3-how-this-exercise-uses-the-template-and-the-example-folder)
4. [Step 1: inspect the existing example or copy the template](#4-step-1-inspect-the-existing-example-or-copy-the-template)
5. [Step 2: rewrite the goals](#5-step-2-rewrite-the-goals)
6. [Step 3: create the real action functions](#6-step-3-create-the-real-action-functions)
7. [Step 4: register the actions](#7-step-4-register-the-actions)
8. [Step 5: keep the environment responsible for execution](#8-step-5-keep-the-environment-responsible-for-execution)
9. [Step 6: update the fake model response](#9-step-6-update-the-fake-model-response)
10. [Step 7: run the agent and inspect memory](#10-step-7-run-the-agent-and-inspect-memory)
11. [Step 8: compare your version with the repository example](#11-step-8-compare-your-version-with-the-repository-example)
12. [What this exercise teaches](#12-what-this-exercise-teaches)
13. [Common mistakes](#13-common-mistakes)
14. [Chapter summary](#14-chapter-summary)

## 1. What you will build

In this exercise, you will use `game_framework_template.py` as the starting point for a file explorer agent.

The repository also includes a completed beginner example here:

```text
examples/file_explorer_agent.py
```

That means you can study this chapter in two ways:

1. Build the exercise yourself by copying the template.
2. Inspect the existing example and compare it with the explanation.

The agent should be able to:

1. List files in a project directory.
2. Read a selected file.
3. Return the result in a structured way.
4. Stop when the user request has been answered.

The purpose is not to create a perfect filesystem assistant. The purpose is to understand one of the most important AI agent ideas: a model cannot use information it cannot see.

## 2. The AI theory: models need external context

A language model does not automatically see your filesystem.

If you ask:

```text
What files are in this project?
```

the model needs a way to obtain that information.

It can guess from general knowledge, but guessing is not agency. For an agent to work with real project state, the system must expose controlled tools such as:

```text
list_files
read_file
search_in_file
```

These tools give the model a controlled form of perception.

The model does not directly browse your computer. Instead, it selects a tool. The environment executes that tool and returns an observation. The next prompt can include that observation, which gives the model better context for the next decision.

This is the key AI lesson in this chapter:

```text
Agents extend a model by giving it controlled access to external information.
```

GAME represents this idea like this:

| AI concept | GAME component |
|---|---|
| The task purpose | Goals |
| Filesystem abilities | Actions |
| Observed file results | Memory |
| Actual file access | Environment |

## 3. How this exercise uses the template and the example folder

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

1. The `goals` list inside the builder function.
2. The action functions.
3. The `registry.register(...)` calls.
4. The fake `generate_response()` function used for testing.
5. The `user_input` inside the `__main__` block.

The `Agent.run()` method in `game/agent.py` should stay the same.

The existing example in `examples/file_explorer_agent.py` shows one clean implementation of this exercise. Treat it as a reference solution, not as the only possible answer.

## 4. Step 1: inspect the existing example or copy the template

There are two valid ways to study this chapter.

### Option A: inspect the existing example

Open:

```text
examples/file_explorer_agent.py
```

Read it from top to bottom and identify the GAME components:

1. Goals.
2. Actions.
3. Memory.
4. Environment.

Then run it:

```bash
python examples/file_explorer_agent.py
```

### Option B: build your own version

Keep the original template as a reference.

Create a new file for this exercise, for example:

```text
my_file_explorer_agent.py
```

Then copy the contents of `game_framework_template.py` into that file.

This gives you a safe place to modify the agent while preserving the base template and the reusable `game/` package.

## 5. Step 2: rewrite the goals

Find the builder function.

In the template it is called:

```text
build_template_agent()
```

In your copied file, you may rename it to something clearer, such as:

```text
build_file_explorer_agent()
```

Inside that function, replace the generic goals with goals for filesystem exploration.

A good first version is:

```text
Goal 1: Explore the current project safely.
Goal 2: Read only files that are useful for the user request.
Goal 3: Stop when the requested information has been provided.
```

These goals teach the model what kind of behavior matters.

The important idea is this: goals are not just labels. They shape the prompt that the model sees, so they influence which action the model chooses next.

## 6. Step 3: create the real action functions

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

At this stage, avoid making one function do too much.

A common beginner mistake is creating one large function that lists, reads, summarizes, and stops. That hides the agent loop instead of teaching it.

The model should learn to move step by step:

```text
Need project context -> list files.
Need file content -> read file.
Have enough information -> terminate.
```

## 7. Step 4: register the actions

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

Think of the action schema as the interface between natural language reasoning and Python execution.

The current framework also performs lightweight argument validation. It checks that required arguments exist and rejects unexpected arguments when a schema defines known properties.

## 8. Step 5: keep the environment responsible for execution

Do not put filesystem logic inside `Agent.run()`.

The loop should remain generic:

```text
model chooses action -> registry finds action -> environment executes action
```

The environment is the execution boundary. It calls the selected action and formats the result.

For this first version, the default `Environment` class is enough.

Later, you can create a stricter environment that limits which directory the agent can read.

This matters because filesystem access is real external access. Even a learning project should develop the habit of keeping execution controlled.

## 9. Step 6: update the fake model response

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

## 10. Step 7: run the agent and inspect memory

Update the `user_input` in the `__main__` block.

For example:

```text
List the files in this project.
```

Run the file from the terminal.

Watch three things:

1. The prompt sent to the model if your exercise version prints it.
2. The selected action stored in memory.
3. The environment result stored in memory.

The memory should show the user request, the model decision, and the environment result.

This is where the exercise becomes concrete: you can see how external context enters the agent through actions and becomes available for future decisions through memory.

## 11. Step 8: compare your version with the repository example

After building your own version, compare it with:

```text
examples/file_explorer_agent.py
```

Look for these differences:

1. Did you use clear goals?
2. Did your action names match your JSON responses?
3. Did your schemas match your Python function arguments?
4. Did your `terminate` action use `terminal=True`?
5. Did your file-reading action include any path safety checks?

The goal of comparing is not to make both files identical.

The goal is to understand which parts are essential to the agent pattern and which parts are implementation choices.

## 12. What this exercise teaches

This exercise teaches the first practical GAME pattern:

1. Goals tell the agent what matters.
2. Actions describe what the agent can do.
3. Memory stores what happened.
4. Environment executes the selected action.
5. The loop stays reusable.

The AI concept is controlled perception.

The model cannot see the project by itself. The agent gives it a safe way to request observations.

## 13. Common mistakes

Common mistakes in this exercise include:

1. Editing `game/agent.py` too early.
2. Forgetting to register a new action.
3. Giving `read_file` a schema that does not match the function argument.
4. Trying to test every action at once.
5. Letting the agent read arbitrary paths before adding safety rules.
6. Assuming the model knows the filesystem without tool results.
7. Forgetting to run tests after changing framework code.

Keep the first version small. Once the basic loop works, safety and extra actions become easier to add.

## 14. Chapter summary

The file explorer agent is the first full template adaptation.

You can either build it yourself from `game_framework_template.py` or inspect the existing implementation in `examples/file_explorer_agent.py`.

The reusable framework stays in `game/`.

This chapter teaches that agents are not powerful because the model magically knows everything. They become useful when the system gives the model controlled access to the right information.
