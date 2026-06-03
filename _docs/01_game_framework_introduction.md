# 01. Introduction to the GAME Framework

## Table of Contents

1. Purpose of this guide
2. What you are going to practice
3. What an AI agent is
4. Why an agent needs structure
5. What GAME means
6. Goals
7. Actions
8. Memory
9. Environment
10. The agent loop
11. What stays stable and what changes
12. How this guide uses the template
13. Chapter summary

## 1. Purpose of this guide

This guide teaches how to build simple AI agents using the **GAME Framework**.

It is written for a reader who already knows basic Python: functions, classes, lists, dictionaries, and modules. It does not assume that the reader already knows how to design agents.

The project includes a reusable framework package:

```text
game/
```

It also includes a starter file called:

```text
game_framework_template.py
```

The goal of the guide is to help you understand the framework package, then copy and modify the template step by step to build different agents.

At first, the examples use fake model responses. Later, when you connect a real provider, the project uses `.env.example` as the safe starting point for local configuration.

## 2. What you are going to practice

The exercises in this guide are not separate random examples. They all follow the same learning pattern:

1. Start from the template.
2. Identify the GAME components.
3. Change the goals.
4. Add or replace actions.
5. Decide what the agent should remember.
6. Let the environment execute actions.
7. Run the loop and inspect the result.
8. Connect a real model only after the fake response flow works.

This repeated process is the point of the guide.

By the end, the reader should understand not only what the code does, but why the framework is organized this way.

## 3. What an AI agent is

An AI agent is a program that uses a model to decide what to do next.

A normal chatbot usually receives a message and returns a response.

An agent does more than that. It can:

1. Read the task.
2. Decide which action to take.
3. Use a tool.
4. Observe the result.
5. Store what happened.
6. Decide the next step.
7. Stop when the task is complete.

For example, if the user asks:

```text
Tell me which Python files are in this project.
```

An agent might first choose `list_files`, then inspect the result, then return a final answer.

## 4. Why an agent needs structure

Without structure, an agent quickly becomes hard to understand.

It is tempting to write one big script that builds a prompt, calls a model, reads files, stores results, handles errors, and prints the answer.

That may work once, but it becomes difficult to extend.

The GAME Framework separates the agent into clear parts so that each part has a specific job.

This is similar to normal software design. A web application usually separates models, views, routes, templates, and services. An agent also benefits from separation.

## 5. What GAME means

GAME stands for:

| Letter | Meaning | Main question |
|---|---|---|
| G | Goals | What should the agent achieve? |
| A | Actions | What can the agent do? |
| M | Memory | What should the agent remember? |
| E | Environment | Where are actions executed? |

These four parts surround the agent loop.

The loop is the process that keeps asking:

```text
Given the goal, available actions, and memory, what should happen next?
```

## 6. Goals

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

The second goal is too vague. The first one tells the agent what kind of work it should do.

In the framework, goals are stored as `Goal` objects with:

```text
priority
name
description
```

In the exercises, one of the first things you will do is replace the template goals with goals for the agent you are building.

## 7. Actions

Actions are the tools the agent can choose.

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

Actions are important because they control what the agent is allowed to attempt.

In the exercises, you will create new Python functions in the copied agent file and register them as actions.

## 8. Memory

Memory stores what has happened so far.

A simple memory entry might record:

1. The user's original request.
2. The model's selected action.
3. The environment result.

Memory matters because agents often need more than one step.

Without memory, the agent may forget what it already did, repeat the same action, or lose track of the original task.

In this guide, memory starts as a simple list of dictionaries. That is enough for learning the loop.

## 9. Environment

The environment executes actions.

This distinction is important:

```text
The model chooses an action.
The environment executes the action.
```

For example, the model may choose `read_file`, but the environment is where the function is actually called.

This keeps the model away from direct uncontrolled access to the system.

In simple exercises, the default environment can execute registered actions directly.

In safer agents, such as the code reviewer, the environment should become stricter and check permissions before running risky actions.

## 10. The agent loop

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

## 11. What stays stable and what changes

This is the most important idea in the guide:

```text
The agent loop stays stable.
The GAME components change.
```

For a file explorer, you change the goals and add file actions.

For a code reviewer, you add review and approval actions.

For a conversation log generator, you add transcript-processing actions and memory for user priorities.

The structure remains familiar each time.

## 12. How this guide uses the template

The guide uses `game/` as the reusable framework and `game_framework_template.py` as the starter agent.

Chapter 02 explains the modular structure.

Chapters 03, 04, and 05 show how to copy the template into a new exercise file and adapt it for a specific agent.

That means each exercise is both conceptual and practical:

1. You learn what the agent should do.
2. You identify which GAME components need to change.
3. You edit the copied agent file.
4. You run the agent.
5. You inspect the output and memory.

This repetition is what helps the concepts become natural.

## 13. Chapter summary

GAME is a way to build agents by separating goals, actions, memory, and environment.

The framework package gives you a reusable loop.

The exercises teach you how to keep that loop stable while changing the components around it.

Once that idea is clear, building different agents becomes much easier because each new agent is no longer a new script from nothing. It is a new configuration of the same framework.
