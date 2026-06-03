# 01. Introduction to AI Agents and the GAME Framework

## Table of Contents

1. [Purpose of this guide](#1-purpose-of-this-guide)
2. [What you are going to learn](#2-what-you-are-going-to-learn)
3. [How language models work at a practical level](#3-how-language-models-work-at-a-practical-level)
4. [Why context matters](#4-why-context-matters)
5. [Why a chatbot is not enough](#5-why-a-chatbot-is-not-enough)
6. [What an AI agent is](#6-what-an-ai-agent-is)
7. [Why an agent needs structure](#7-why-an-agent-needs-structure)
8. [What GAME means](#8-what-game-means)
9. [Goals: giving the model direction](#9-goals-giving-the-model-direction)
10. [Actions: giving the model controlled abilities](#10-actions-giving-the-model-controlled-abilities)
11. [Memory: giving the model working context](#11-memory-giving-the-model-working-context)
12. [Environment: controlling execution](#12-environment-controlling-execution)
13. [The agent loop](#13-the-agent-loop)
14. [What stays stable and what changes](#14-what-stays-stable-and-what-changes)
15. [How this guide uses the template](#15-how-this-guide-uses-the-template)
16. [Chapter summary](#16-chapter-summary)

## 1. Purpose of this guide

This guide teaches how to build AI agents while also explaining the AI concepts behind them.

The **GAME Framework** is the structure we use to practice those concepts. GAME is useful because it gives us a repeatable way to organize the information an AI model needs in order to behave like an agent.

This guide is written for a reader who already knows basic Python: functions, classes, lists, dictionaries, and modules. It does not assume that the reader already knows how to design agents.

The project includes a reusable framework package:

```text
game/
```

It also includes a starter file called:

```text
game_framework_template.py
```

The goal is not to memorize a framework. The goal is to understand why agents need goals, actions, memory, and environment, then use the template to practice those ideas in code.

## 2. What you are going to learn

The exercises in this guide are not separate random examples. They all follow the same learning pattern:

1. Understand the AI concept.
2. See why the concept matters for agents.
3. Identify the GAME component that represents it.
4. Copy the template into a new working file.
5. Modify one component at a time.
6. Run the agent with fake model responses.
7. Inspect memory to see what happened.
8. Connect a real model only after the controlled flow works.

By the end, you should understand not only what the code does, but why the framework is organized this way.

## 3. How language models work at a practical level

A language model receives input text and produces output text.

That sounds simple, but it has important consequences.

The model does not automatically know your current files, your project state, your private rules, your local environment, or what happened outside the text it was given.

At runtime, the model mainly depends on:

1. The instructions in the prompt.
2. The context included in the prompt.
3. The available tools described to it.
4. The previous messages or memory that are shown to it.
5. The format you ask it to use for its response.

This is why agent design is mostly context design.

If the model needs to make a good decision, we must provide the right information in a usable form.

## 4. Why context matters

Context is the information the model can use during a decision.

For example, if you ask:

```text
Which file should I edit?
```

the model cannot answer reliably unless it knows:

1. What files exist.
2. What the task is.
3. What the current code looks like.
4. What constraints it must follow.
5. What it already tried.

Humans often assume shared context. AI systems do not get that for free.

This is one of the biggest reasons agents need structure. The structure decides what information is placed in front of the model, how tools are described, and how previous results are remembered.

## 5. Why a chatbot is not enough

A normal chatbot receives a message and replies with text.

That is useful for explanation, but it is limited for tasks that require interaction with the outside world.

For example, a chatbot can say:

```text
You should inspect README.md.
```

An agent can request:

```json
{
  "tool": "read_file",
  "args": {
    "file_name": "README.md"
  }
}
```

The difference is important.

The chatbot talks about the action.
The agent participates in a controlled process where actions can be selected, executed, observed, and remembered.

## 6. What an AI agent is

An AI agent is a program that uses a model to decide what to do next.

It usually has a loop:

1. Read the task.
2. Build context for the model.
3. Ask the model for the next action.
4. Parse the model response.
5. Execute the selected action.
6. Store the result.
7. Repeat until the task is complete.

For example, if the user asks:

```text
Tell me which Python files are in this project.
```

an agent might choose `list_files`, observe the result, then choose `terminate` with a final answer.

The model does not directly execute Python. It selects an action in a structured format. The program around the model decides what to do with that selection.

## 7. Why an agent needs structure

Without structure, an agent quickly becomes difficult to understand and unsafe to extend.

It is tempting to write one large script that builds a prompt, calls a model, reads files, stores results, handles errors, and prints the answer.

That may work once, but it becomes hard to study.

The GAME Framework separates the agent into clear parts so that each part has a specific job.

This is similar to normal software design. A web application separates routes, views, models, templates, and services. An agent also benefits from separation.

In this guide, GAME is the study structure that helps you see the AI system clearly.

## 8. What GAME means

GAME stands for:

| Letter | Meaning | Main question |
|---|---|---|
| G | Goals | What should the agent achieve? |
| A | Actions | What can the agent do? |
| M | Memory | What should the agent remember? |
| E | Environment | Where are actions executed and controlled? |

These four parts surround the agent loop.

The loop keeps asking:

```text
Given the goal, available actions, and memory, what should happen next?
```

GAME works well as a teaching framework because each part corresponds to a real need of an AI model.

## 9. Goals: giving the model direction

Goals describe what the agent is trying to achieve and how it should behave.

Good goals are specific enough to guide the model.

For example:

```text
Explore the project files safely and answer the user's question.
```

That is better than:

```text
Help the user.
```

The second goal is too vague. The first tells the model what kind of work matters.

Goals are not just comments in the code. They become part of the prompt. That means the model sees them when deciding what action to select.

In the framework, goals are stored as `Goal` objects with:

```text
priority
name
description
```

In the exercises, one of the first things you will do is replace the template goals with goals for the agent you are building.

## 10. Actions: giving the model controlled abilities

Actions are the tools the model is allowed to request.

Examples:

```text
list_files
read_file
search_in_file
terminate
```

Each action has:

1. A name.
2. A Python function.
3. A description.
4. A parameter schema.
5. A flag that says whether it ends the loop.

Actions are how we turn model text into controlled behavior.

The model should not be given direct, unlimited control over the system. Instead, it receives a list of available actions and the expected arguments for each one.

This is why schemas matter. A schema tells the model what information an action expects.

For example, `read_file` might need:

```json
{
  "file_name": "README.md"
}
```

If the schema is unclear, the model may send arguments that the Python function cannot use.

## 11. Memory: giving the model working context

Memory stores what has happened so far.

A simple memory entry might record:

1. The user's original request.
2. The model's selected action.
3. The environment result.

This matters because agents usually need more than one step.

Without memory, the agent may forget what it already did, repeat the same action, or lose track of the original task.

It is important to understand that memory here is external memory. It is not the model secretly remembering everything by itself. The program stores information, then includes useful memory in the next prompt.

In this guide, memory starts as a simple list of dictionaries. That is enough for learning the loop.

Later, memory could become a database, a vector store, a file, or a more advanced state object.

## 12. Environment: controlling execution

The environment executes actions.

This distinction is essential:

```text
The model chooses an action.
The environment executes or rejects the action.
```

For example, the model may request `read_file`, but the environment is where the function is actually called.

This keeps the model away from direct uncontrolled access to the system.

In simple exercises, the default environment can execute registered actions directly.

In safer agents, such as the code reviewer, the environment should check permissions before running risky actions.

The environment is where you can enforce rules such as:

1. Do not read files outside the project.
2. Do not edit files without approval.
3. Do not run dangerous commands.
4. Return structured errors when an action is not allowed.

## 13. The agent loop

The agent loop is the repeated process that makes the agent work.

The basic flow is:

1. The user gives a task.
2. The task is stored in memory.
3. The prompt is built from goals, actions, and memory.
4. The model chooses an action.
5. The response is parsed.
6. The action is found in the registry.
7. The environment executes it.
8. The result is stored in memory.
9. The loop continues until a terminal action is selected.

This loop is already implemented in `game/agent.py`.

The exercises are designed so that you usually do not edit the loop. Instead, you change the GAME components around it.

## 14. What stays stable and what changes

This is the most important habit in the guide:

```text
The agent loop stays stable.
The GAME components change.
```

For a file explorer, you change the goals and add file actions.

For a code reviewer, you add review and approval actions.

For a conversation log generator, you add transcript-processing actions and memory for user priorities.

The structure remains familiar each time.

This is how the framework helps you learn AI agent design without starting from zero for every project.

## 15. How this guide uses the template

The guide uses `game/` as the reusable framework and `game_framework_template.py` as the starter agent.

Chapter 02 explains the modular structure and why each module exists.

Chapters 03, 04, and 05 show how to copy the template into a new exercise file and adapt it for a specific agent.

Each exercise is both conceptual and practical:

1. You learn the AI concept.
2. You identify which GAME components represent it.
3. You edit the copied agent file.
4. You run the agent.
5. You inspect the output and memory.

This repetition is what helps the concepts become natural.

## 16. Chapter summary

AI agents need structure because models need clear context, controlled actions, useful memory, and safe execution boundaries.

GAME is a way to organize those needs:

```text
Goals give direction.
Actions give controlled abilities.
Memory gives working context.
Environment controls execution.
```

The framework package gives you a reusable loop.

The exercises teach you how to keep that loop stable while changing the components around it.

Once that idea is clear, building different agents becomes easier because each new agent is no longer a new script from nothing. It is a new configuration of the same AI design pattern.
