---
name: wingmen-pipelines
description: Create, run, inspect, debug, duplicate, edit, version, or explain current Autopilot declarative pipelines; add reusable blocks; wire agent steps and callbacks; inspect run state; or build task-backed worker/manager flows.
---

# Autopilot Pipelines

Use this skill for Autopilot pipeline work. Locate the active repo under `~/code/wm/autopilot` or the legacy `~/code/wingmanbefree/autopilot` path before running commands.

Do not start or fall back to archived Wingmen checkouts or legacy pipeline ports. Archived runtimes must not be used as live servers or pipeline runtimes.

## Fast Orientation

- Pipeline definitions live under `~/.wingmen/pipelines/shared/definitions/` and `~/.wingmen/pipelines/users/<three-word-alias>/definitions/`.
- Runtime history lives in `<autopilot-repo>/data/pipelines.sqlite`.
- Core implementation lives in `<autopilot-repo>/src/pipelines/`.
- UI lives in `<autopilot-repo>/src/ui/pipelines/` and is served at `/pipelines`.
- Documentation lives in `<autopilot-repo>/docs/declarative-pipelines.md`.

Read `references/pipeline-operations.md` when you need exact commands, JSON examples, schema details, or API routes.

## Default Workflow

1. Inspect the current pipeline definition and recent run history before changing behavior.
2. Prefer editing JSON definitions in `~/.wingmen/pipelines/users/<alias>/definitions/` for user-specific pipelines; shared demos are okay for built-in examples.
3. Keep every step object-in/object-out.
4. Add human display metadata while you build or edit steps; do not leave the UI to infer important fields from raw JSON.
5. For agent work, pass compact references and structured context. Do not pass whole documents through pipeline JSON unless the user explicitly asks.
6. Use `graphContext` for long-term memory recall. Treat it as potential context, not authoritative truth.
7. After code changes, run focused tests. If live UI/server verification requires a managed restart, perform it only with the user's explicit restart approval in the current conversation; otherwise report the pending restart and smoke test.

## Supervised Agent Work

- For substantial implementation originating in chat, create a self-contained Flight Deck task before starting the worker pipeline.
- Pass a compact, self-contained worker brief with the goal, workdir, target surface, constraints, acceptance criteria, validation, and reporting context.
- Give agent sessions explicit goal metadata. Keep `nextAction=reflect` while implementation, review, or reporting remains; use `stop` only when genuinely complete.
- Require the manager step to inspect callback fields and independent repository/evidence state. Never treat a worker's completion claim as automatic acceptance.
- Keep deterministic pipeline steps responsible for task comments, state changes, and chat handoff when the definition assigns them that role.
- Use ordinary `wingman.ts dispatch create/status/acknowledge/close` outside a declarative agent step. If its terminal callback is missing, inspect dispatch status explicitly.

## Pipeline Building Rules

- Use `code` steps for deterministic TypeScript functions from `builtinPipelineFunctions`.
- Use `agent` steps for judgement, extraction, critique, transformation, or decisions that benefit from an AI session.
- Use `loop` control steps for visible branches back to a prior top-level step.
- Use `block` steps for reusable multi-step patterns, such as `memory.graphContext`.
- Use `assign` paths to keep the running object readable, e.g. `$.memory.graph`, `$.iteration.critic`, `$.reviewHistory`.
- When duplicating or editing user pipelines, create a new versioned JSON file instead of overwriting unless the user explicitly asks.

## Display Metadata Rules

Every non-trivial step should include a short `description` and `display` metadata for the Pipelines UI. The display rows are the human debugging contract: they should show the domain payload in and out, not routing scaffolding.

- Add `display.in` and `display.out` to code, agent, loop, and block steps where a human needs to understand what happened.
- Use human labels such as `Chat Message`, `Thread`, `Company`, `Summary`, `Approved`, `Sources`, or `Webhook Delivered`; avoid raw container labels like `chat`, `record`, `runtime`, `dispatch`, or `routing`.
- Point display paths at the meaningful nested value, even when it lives deep in JSON. Promote that value into a first-class row rather than showing the parent object as `5 fields`.
- Use `format: "text"` for prose, `format: "messages"` for chat/thread arrays, `format: "records"` for record arrays, `format: "list"` for short arrays, and `format: "count"` when the item count is what matters.
- Keep display rows small: usually 1-3 inputs and 2-5 outputs. Use `limit` and `empty` for arrays or optional values.
- Treat skipped steps as control-flow explanation only. The UI intentionally shows no data rows for skipped steps, so put the reason in the step `description` or `when` condition rather than relying on display rows.
- The generic fallback hides known plumbing, but do not depend on fallback for important pipelines. Explicit display metadata should be the default for new or edited definitions.

## Validation

Run the smallest useful validation first:

```bash
cd "${AUTOPILOT_REPO:-$HOME/code/wm/autopilot}"
bun --check src/pipelines/*.ts
bun test src/pipelines/pipeline-loader.test.ts src/pipelines/pipeline-runner.test.ts src/pipelines/pipeline-blocks.test.ts src/pipelines/functions.test.ts
```

When UI or server assets change and the user has explicitly approved the managed restart in the current conversation:

```bash
pm2 restart wm-ap --update-env
```

Without that approval, do not restart. Record the exact restart and `/pipelines` smoke test still required.
