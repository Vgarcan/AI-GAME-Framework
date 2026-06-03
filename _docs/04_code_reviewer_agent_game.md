# 04. Building a Code Reviewer Agent from the GAME Template

## Table of Contents

1. What you will build
2. How this exercise builds on the file explorer
3. Step 1: create a new working file
4. Step 2: rewrite the goals for safe review
5. Step 3: separate reading actions from editing actions
6. Step 4: add proposal and approval actions
7. Step 5: register the new actions
8. Step 6: use memory to track review state
9. Step 7: make the environment stricter
10. Step 8: test the review flow
11. What this exercise teaches
12. Common mistakes
13. Chapter summary

## 1. What you will build

In this exercise, you will adapt the GAME template into a code reviewer agent.

The agent should inspect code, propose a small improvement, and wait for approval before applying any change.

This is more advanced than the file explorer because the agent now needs a safety process. Reading a file is low risk. Editing a file is not.

## 2. How this exercise builds on the file explorer

The file explorer agent taught the basic pattern:

```text
list -> read -> observe -> remember -> stop
```

The code reviewer adds a new pattern:

```text
inspect -> propose -> wait for approval -> apply -> verify -> stop
```

You are still using the same modular structure. The reusable loop lives in `game/`, while the copied agent file defines the review-specific goals, actions, and tests.

## 3. Step 1: create a new working file

Create a separate file for this exercise, for example:

```text
code_reviewer_agent.py
```

Start from the template or from your file explorer agent.

If you start from the file explorer agent, keep the useful reading actions:

```text
list_files
read_file
search_in_file
```

Then add the review-specific behavior on top.

## 4. Step 2: rewrite the goals for safe review

Find the `goals` list inside `build_template_agent()`.

Replace the file explorer goals with review goals:

```text
Goal 1: Inspect code before proposing changes.
Goal 2: Suggest only small and understandable improvements.
Goal 3: Do not edit files without explicit approval.
Goal 4: Stop when the review task is complete.
```

This matters because the prompt will include these goals. The model needs to see that review and editing are separate phases.

Avoid vague goals such as:

```text
Improve the code.
```

That goal is too broad and gives the agent too much freedom.

## 5. Step 3: separate reading actions from editing actions

The action set should have two groups.

Read-only actions:

```text
list_files
read_file
search_in_file
```

Review and editing actions:

```text
propose_change
request_approval
apply_change
terminate
```

This separation helps the student see a core GAME idea: actions are the agent's available choices, but not all choices should have the same risk level.

The environment can allow read-only actions freely while restricting write actions.

## 6. Step 4: add proposal and approval actions

Add small functions near the bottom of the file, where the template keeps example actions.

The first useful review action is `propose_change`.

Its job is not to edit anything. Its job is to describe:

1. The file being discussed.
2. The issue found.
3. The proposed change.
4. Why the change is useful.

The next useful action is `request_approval`.

Its job is to make the approval step explicit. The agent should not treat a proposal as approval.

Finally, `apply_change` should only run after approval has been recorded.

At first, `apply_change` can be a placeholder that returns what it would change. That lets the student test the workflow before writing real file-editing logic.

## 7. Step 5: register the new actions

After creating the functions, register each one with `ActionRegistry`.

For each action, check that:

1. The action name matches what the model will call.
2. The function name is correct.
3. The description tells the model when to use the action.
4. The parameter schema matches the function arguments.
5. Only `terminate` is marked as terminal.

This is where many early bugs happen. If `apply_change` expects `file_name` but the schema calls it `path`, the model response and the function will not match.

## 8. Step 6: use memory to track review state

The reusable agent loop already stores memory entries for the user request, model response, and environment result.

For the code reviewer, pay attention to what needs to be remembered:

1. Which files have been inspected.
2. Which issue was found.
3. Which change was proposed.
4. Whether approval was requested.
5. Whether approval was granted.

The approval state is the important part.

If the agent cannot remember approval, it cannot safely decide whether `apply_change` is allowed.

In a simple first version, approval can be simulated through the fake `generate_response()` function. Later, the approval can come from real user input.

## 9. Step 7: make the environment stricter

The default `Environment` executes whatever registered action the model selects.

For a reviewer, that may be too permissive.

Create a stricter environment when you are ready. Its job is to check write actions before executing them.

For example, before running `apply_change`, the environment should verify:

1. A proposal exists.
2. The user approved the proposal.
3. The requested file is allowed.
4. The change is within the expected scope.

This teaches the difference between model decision and system permission.

The model can request an action. The environment decides whether that action is allowed.

## 10. Step 8: test the review flow

Test the agent in stages.

First, fake a model response that lists files.

Then fake a response that reads one file.

Then fake a response that proposes a change.

Then fake a response that requests approval.

Only after that should you test `apply_change`.

A good test request is:

```text
Review one Python file and suggest one small improvement.
```

A good run should show:

1. The agent inspects before proposing.
2. The agent proposes one small change.
3. The agent records the approval step.
4. The agent does not apply a change too early.
5. The agent stops cleanly.

## 11. What this exercise teaches

This exercise teaches how GAME handles risk.

The same framework package can support a simple file explorer and a more careful code reviewer because the loop is stable and the components change.

In this agent:

1. Goals define safety.
2. Actions separate reading from editing.
3. Memory tracks approval state.
4. Environment enforces permission.
5. The loop coordinates the process.

## 12. Common mistakes

Common mistakes in this exercise include:

1. Letting `apply_change` run without approval.
2. Mixing proposal and editing into one action.
3. Forgetting to update the action schema.
4. Editing `game/agent.py` instead of changing actions and environment.
5. Testing the whole workflow at once instead of one action at a time.

The safest approach is to build the workflow gradually and inspect memory after each step.

## 13. Chapter summary

The code reviewer agent is the second template adaptation.

You start with the same GAME template, keep the reusable loop from `game/`, add review-specific goals, separate read actions from write actions, register proposal and approval tools, and use memory plus environment rules to prevent unsafe edits.

This is where the framework starts to feel more powerful: the same core structure can support very different agents when the GAME components are designed carefully.
