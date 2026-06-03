# 05. Building a Conversation Log Generator from the GAME Template

## Table of Contents

1. [What you will build](#1-what-you-will-build)
2. [The AI theory: summarization is not the same as structured extraction](#2-the-ai-theory-summarization-is-not-the-same-as-structured-extraction)
3. [Why this agent is more open-ended](#3-why-this-agent-is-more-open-ended)
4. [Step 1: create a new working file](#4-step-1-create-a-new-working-file)
5. [Step 2: rewrite the goals for transcript processing](#5-step-2-rewrite-the-goals-for-transcript-processing)
6. [Step 3: define the transcript actions](#6-step-3-define-the-transcript-actions)
7. [Step 4: design memory for user priorities](#7-step-4-design-memory-for-user-priorities)
8. [Step 5: decide what the environment handles](#8-step-5-decide-what-the-environment-handles)
9. [Step 6: design the log structure](#9-step-6-design-the-log-structure)
10. [Step 7: test the process in stages](#10-step-7-test-the-process-in-stages)
11. [How the agent decides what matters](#11-how-the-agent-decides-what-matters)
12. [Working with long transcripts](#12-working-with-long-transcripts)
13. [What this exercise teaches](#13-what-this-exercise-teaches)
14. [Common mistakes](#14-common-mistakes)
15. [Chapter summary](#15-chapter-summary)

## 1. What you will build

In this final project, you will adapt the GAME template into a conversation log generator.

The agent receives transcript-like input and creates a structured log. The log should reflect what the user considers important, such as decisions, tasks, risks, open questions, or follow-up items.

This is not just a summarizer. A summarizer compresses text. A log generator organizes a conversation around a purpose.

## 2. The AI theory: summarization is not the same as structured extraction

When people first use language models with transcripts, they often ask for a summary.

That can be useful, but it is not always enough.

A summary usually asks:

```text
What is the shorter version of this text?
```

A conversation log asks:

```text
Which parts of this conversation matter for a specific purpose?
```

That difference changes the agent design.

The model needs to know what to extract, not just what to shorten.

For example, the same transcript can produce different logs:

| User priority | What the agent should preserve |
|---|---|
| Decisions | Agreements, tradeoffs, reasons |
| Action items | Tasks, owners, deadlines |
| Risks | Blockers, uncertainty, warnings |
| Open questions | Unresolved points, missing information |
| Research insights | Themes, observations, repeated signals |

This is why user priorities must be part of the prompt and memory.

GAME represents this idea like this:

| AI concept | GAME component |
|---|---|
| Purpose of the log | Goals |
| Transcript processing steps | Actions |
| User priorities and extracted points | Memory |
| Loading, chunking, and saving text | Environment |

## 3. Why this agent is more open-ended

The previous agents had clearer workflows.

The file explorer lists and reads files.
The code reviewer inspects, proposes, waits for approval, and edits only when allowed.

The conversation log generator is more flexible because the user defines the criteria for the log.

That means the agent must handle two inputs:

1. The transcript content.
2. The user's priorities for the final log.

This makes memory and prompt design more important than in the earlier exercises.

The agent should not assume that every user wants the same kind of log.

## 4. Step 1: create a new working file

Create a new file for this project, for example:

```text
conversation_log_agent.py
```

Copy the contents of `game_framework_template.py` into the new file.

You will adapt the same parts as before:

1. The `goals` list.
2. The action functions.
3. The `registry.register(...)` calls.
4. The fake `generate_response()` function.
5. The initial `user_input`.

The `Agent.run()` loop from `game/agent.py` should still remain stable.

## 5. Step 2: rewrite the goals for transcript processing

Find `build_template_agent()`.

Replace the template goals with goals for transcript logging:

```text
Goal 1: Turn transcript material into a structured conversation log.
Goal 2: Prioritize the topics the user says are important.
Goal 3: Preserve important context while removing low-value repetition.
Goal 4: Stop when the log is complete and readable.
```

These goals matter because this agent must judge relevance. It should not treat every sentence in the transcript as equally important.

The goals also remind the model that the output is a log, not a generic summary.

## 6. Step 3: define the transcript actions

A useful first action set is:

```text
load_transcript
extract_relevant_points
draft_log
revise_log
finalize_log
terminate
```

Each action should have one clear job:

1. `load_transcript` receives or loads the transcript text.
2. `extract_relevant_points` selects material based on user priorities.
3. `draft_log` organizes the selected points into sections.
4. `revise_log` adjusts the draft if priorities change.
5. `finalize_log` prepares the final output.
6. `terminate` ends the loop with a final message.

Do not make one action do the entire job.

This project is useful because it shows a multi-step information workflow. Breaking the work into actions makes it possible to inspect and improve each step.

## 7. Step 4: design memory for user priorities

This agent needs to remember more than raw transcript text.

Useful memory entries include:

1. The transcript or transcript chunk being processed.
2. The user's chosen focus points.
3. Extracted relevant points.
4. Draft log sections.
5. Revision notes.

The user's priorities are the most important memory item.

For example, if the user says they care about decisions and follow-up tasks, the agent should keep using that preference throughout the run.

Without memory, the agent may drift back into generic summarization.

This is a real AI design issue: models are sensitive to the context they receive. If the user's priorities disappear from the prompt, the model may stop optimizing for them.

## 8. Step 5: decide what the environment handles

The environment should handle practical operations, not reasoning.

For this project, the environment may:

1. Read transcript text from a file.
2. Split long transcripts into chunks.
3. Save intermediate drafts.
4. Save the final log as Markdown or plain text.
5. Return structured errors when input is missing.

The model decides which action to request.
The environment performs the real operation and returns the result.

That separation keeps the workflow understandable.

It also prevents the prompt from carrying unnecessary operational details. The model should reason about the content and structure of the log. The environment should handle file and text operations.

## 9. Step 6: design the log structure

The log structure should match the user's priorities.

A useful default structure is:

```text
Context
Key decisions
Action items
Open questions
Risks or blockers
Follow-up notes
```

The structure should be readable and easy to scan.

If the user cares about accountability, include owners or responsible people.

If the user cares about research insights, include themes and observations.

If the user cares about project management, include tasks, deadlines, and blockers.

This is where the agent becomes flexible without becoming vague.

The model should not invent a structure randomly. The structure should come from the user's priorities, the goals, and the action descriptions.

## 10. Step 7: test the process in stages

Use the fake `generate_response()` function to test one action at a time.

First, test `load_transcript`.

Then test `extract_relevant_points`.

Then test `draft_log`.

Then test `finalize_log`.

Only after the flow works with fake responses should you connect a real model. When that moment comes, copy `.env.example` to `.env` and fill in the provider settings you need.

A good first user input is:

```text
Create a conversation log from this transcript. Focus on decisions, action items, and open questions.
```

Inspect memory after each run. You should be able to see the transcript input, the focus points, the extracted material, and the draft result.

## 11. How the agent decides what matters

The most important design choice is how the agent judges relevance.

The agent should not ask:

```text
What is the shortest summary?
```

It should ask:

```text
Which parts of this transcript match the user's priorities?
```

For example:

1. If the priority is decisions, keep final agreements and the reasons behind them.
2. If the priority is action items, keep tasks, owners, and deadlines.
3. If the priority is risks, keep blockers, uncertainty, and warnings.
4. If the priority is open questions, keep unresolved points and missing information.

This is why the user's priorities must be visible in the prompt and preserved in memory.

## 12. Working with long transcripts

Long transcripts introduce another AI concept: context limits.

A model can only process a limited amount of text at once. Even when the limit is large, too much irrelevant text can reduce the quality of the result.

A practical workflow is:

1. Load the transcript.
2. Split it into manageable chunks.
3. Extract relevant points from each chunk.
4. Merge extracted points.
5. Draft the final log from the merged material.
6. Revise the log against the user's priorities.

This is why chunking can belong in the environment while relevance decisions belong in the model-facing workflow.

The agent should not simply throw a huge transcript into one prompt and hope for the best.

## 13. What this exercise teaches

This final project teaches how to use GAME for a less rigid workflow.

In this agent:

1. Goals define the purpose of the log.
2. Actions break transcript processing into steps.
3. Memory preserves user priorities across the process.
4. Environment handles loading, chunking, and saving.
5. The loop coordinates extraction, drafting, revision, and finalization.

The AI concept is relevance management.

The model needs explicit criteria for what matters, and the system needs to preserve those criteria across the workflow.

## 14. Common mistakes

Common mistakes in this project include:

1. Treating the task as generic summarization.
2. Forgetting to store the user's priorities.
3. Trying to process a very long transcript in one step.
4. Creating one oversized action that does everything.
5. Producing a log structure that does not match the user's request.
6. Connecting a real model before the fake action flow is clear.
7. Letting chunk summaries lose the user's original priorities.

The best approach is to build the process one action at a time.

## 15. Chapter summary

The conversation log generator is the final template adaptation.

You start with the same `game_framework_template.py`, create a new working file, rewrite the goals, define transcript-specific actions, store user priorities in memory, let the environment handle practical text operations, and test the process in stages.

This chapter shows the full value of GAME: the `game/` package gives you structure, but the agent's behavior comes from how you design the goals, actions, memory, and environment in the copied agent file.

It also shows that good AI work is not only about asking for output. It is about giving the model the right purpose, the right context, and the right process.
