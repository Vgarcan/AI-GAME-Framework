# 07. Model Provider Selection

## Table of Contents

1. [Purpose of this chapter](#1-purpose-of-this-chapter)
2. [Why provider selection exists](#2-why-provider-selection-exists)
3. [Why this is not called debug mode](#3-why-this-is-not-called-debug-mode)
4. [The default provider: fake](#4-the-default-provider-fake)
5. [How `MODEL_PROVIDER` works](#5-how-model_provider-works)
6. [How `SHOW_MODEL_PROMPT` works](#6-how-show_model_prompt-works)
7. [How `.env.example` fits into provider selection](#7-how-envexample-fits-into-provider-selection)
8. [Current implementation limitation](#8-current-implementation-limitation)
9. [Recommended next implementation step](#9-recommended-next-implementation-step)
10. [Chapter summary](#10-chapter-summary)

## 1. Purpose of this chapter

This chapter explains how the template decides where a model response comes from.

Earlier versions of the guide described the template as having a fake `generate_response()` function that students would later replace.

The project has now moved toward a cleaner pattern:

```text
Keep generate_response() stable.
Change MODEL_PROVIDER when you are ready.
```

This is closer to how professional AI applications are usually structured.

## 2. Why provider selection exists

An agent needs a model response before it can choose an action.

During learning, a real model is not always useful. It can introduce uncertainty before the student understands the framework.

That is why the default provider is fake.

The fake provider returns a deterministic JSON response. This makes it easier to test:

1. Prompt construction.
2. Response parsing.
3. Action lookup.
4. Environment execution.
5. Memory updates.

Later, the same template can point to a real provider.

Possible future providers include:

```text
fake
ollama
openai
litellm
local_http
```

## 3. Why this is not called debug mode

It is tempting to call the fake response option `debug=True`.

That would be misleading.

Debug mode usually means:

```text
Show more logs.
Print more internal details.
Make troubleshooting easier.
```

Provider selection is different.

It controls where the model response comes from.

That is why the project uses:

```text
MODEL_PROVIDER=fake
```

instead of:

```text
debug=True
```

The project also has a separate setting for prompt visibility:

```text
SHOW_MODEL_PROMPT=false
```

This keeps the design clearer:

| Setting | Responsibility |
|---|---|
| `MODEL_PROVIDER` | Selects fake, Ollama, OpenAI, LiteLLM, or another provider |
| `SHOW_MODEL_PROMPT` | Controls whether the prompt is printed for inspection |

## 4. The default provider: fake

The template defaults to:

```text
MODEL_PROVIDER=fake
```

This means the student can run the template without:

1. API keys.
2. Local model servers.
3. Internet access.
4. Provider SDKs.

The fake provider is not a shortcut or a toy mistake. It is a teaching tool.

It lets the student prove that the deterministic parts of the framework work before adding a real model.

## 5. How `MODEL_PROVIDER` works

The template reads the provider from the environment:

```python
MODEL_PROVIDER = "fake"
```

If no value is configured, the default is fake.

The template then routes through `generate_response()`:

```text
MODEL_PROVIDER=fake -> generate_fake_response()
MODEL_PROVIDER=other -> generate_real_response()
```

At the moment, real providers are not implemented in the template.

That is intentional. The current learning goal is to understand the framework first.

## 6. How `SHOW_MODEL_PROMPT` works

`SHOW_MODEL_PROMPT` controls whether the full prompt is printed.

Example:

```text
SHOW_MODEL_PROMPT=true
```

This is useful when learning how goals, actions, and memory become model context.

It should not be confused with provider selection.

You can use:

```text
MODEL_PROVIDER=fake
SHOW_MODEL_PROMPT=true
```

This means:

```text
Use the fake provider, but print the prompt so I can inspect it.
```

## 7. How `.env.example` fits into provider selection

`.env.example` documents the environment variables the project expects.

Current values include:

```text
MODEL_PROVIDER=fake
SHOW_MODEL_PROMPT=false
OPENAI_API_KEY=
SERVER_URL=
MODEL_NAME=
```

Important note: the current template reads environment variables with `os.getenv()`.

That means copying `.env.example` to `.env` documents the values, but the file is not automatically loaded unless a loader such as `python-dotenv` is added later.

For now, either set environment variables in your shell or keep using the default fake provider.

## 8. Current implementation limitation

The template has a placeholder for real providers.

If a student sets:

```text
MODEL_PROVIDER=openai
```

before an OpenAI client has been implemented, the provider path is expected to fail clearly.

This is acceptable during the learning stage, but the next professional improvement is to make provider errors become structured memory entries instead of raw crashes.

The preferred long-term fix is to update the main agent loop so provider failures are captured in memory just like parsing errors.

## 9. Recommended next implementation step

The next implementation step should be:

```text
Move model-response generation inside the protected part of Agent.run().
```

That way, errors from providers such as Ollama, OpenAI, LiteLLM, or local HTTP endpoints can be stored in memory.

A future version of the loop should handle:

1. Provider not implemented.
2. Timeout.
3. Invalid provider response.
4. Unknown action.
5. Invalid action arguments.

This will make the framework safer and easier to debug.

## 10. Chapter summary

Provider selection separates learning mode from real model integration.

Use:

```text
MODEL_PROVIDER=fake
```

while learning the framework.

Use:

```text
SHOW_MODEL_PROMPT=true
```

when you want to inspect the prompt.

Do not call this debug mode, because fake provider selection and debugging are different concerns.

The current system is good for learning. The next professional step is to make provider failures become structured memory entries.
