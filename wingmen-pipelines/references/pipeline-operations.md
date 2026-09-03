# Autopilot Pipeline Operations

## Contents

- [Files](#files)
- [API Routes](#api-routes)
- [Inspecting Runs](#inspecting-runs)
- [Definition Shape](#definition-shape)
- [Code Step](#code-step)
- [Agent Step](#agent-step)
- [Loop Control Step](#loop-control-step)
- [Memory Graph Context Block](#memory-graph-context-block)
- [Creating Or Duplicating Pipelines](#creating-or-duplicating-pipelines)
- [Validation](#validation)

## Files

- Repo: locate `~/code/wm/autopilot` first; older installations may use `~/code/wingmanbefree/autopilot`
- Definitions:
  - Shared: `~/.wingmen/pipelines/shared/definitions/`
  - User: `~/.wingmen/pipelines/users/<three-word-alias>/definitions/`
- User-extensible functions:
  - Shared: `~/.wingmen/pipelines/shared/functions/`
  - User: `~/.wingmen/pipelines/users/<three-word-alias>/functions/`
- The pipeline root `~/.wingmen/pipelines/` is initialized as a Git repo for diffs, versioning, and review.
- Runtime DB: `<autopilot-repo>/data/pipelines.sqlite`
- Implementation:
  - `src/pipelines/declarative.ts`
  - `src/pipelines/function-loader.ts`
  - `src/pipelines/functions.ts`
  - `src/pipelines/pipeline-blocks.ts`
  - `src/pipelines/pipeline-loader.ts`
  - `src/pipelines/pipeline-runner.ts`
  - `src/pipelines/pipeline-store.ts`
  - `src/pipelines/pipeline-api-routes.ts`
- UI:
  - `src/ui/pipelines/api.js`
  - `src/ui/pipelines/page.js`
  - `src/ui/navigation/navigation.js`
  - `src/server.ts` asset version and SPA route wiring

## API Routes

Use browser/session auth for non-callback routes.

```text
GET  /api/pipelines/root
GET  /api/pipelines/definitions
GET  /api/pipelines/definitions/:id
GET  /api/pipelines/functions
POST /api/pipelines/definitions/:id/runs
GET  /api/pipelines/runs
GET  /api/pipelines/runs/:id
GET  /api/pipelines/runs/:id/steps
GET  /api/pipelines/runs/:id/steps/:stepId
POST /api/pipelines/runs/:id/steps/:stepId/callback
POST /api/pipelines/wizard
POST /api/pipelines/definitions/:id/wizard-edit
```

Callback routes are intentionally token-authenticated and bypass browser auth. Resolve the active Autopilot origin from `$WINGMAN_URL`; do not publish or assume a machine-specific URL.

## Inspecting Runs

```bash
cd "${AUTOPILOT_REPO:-$HOME/code/wm/autopilot}"
sqlite3 data/pipelines.sqlite ".tables"
sqlite3 data/pipelines.sqlite "select id,name,status,error,started_at,completed_at from pipeline_runs order by started_at desc limit 20;"
sqlite3 data/pipelines.sqlite "select id,step_index,name,kind,status,error,wingman_session_id from pipeline_steps where run_id='<run-id>' order by step_index;"
sqlite3 data/pipelines.sqlite "select payload_json,error,accepted,received_at from pipeline_callbacks where step_id='<step-id>' order by received_at;"
sqlite3 data/pipelines.sqlite "select type,level,message,data_json,ts from pipeline_events where run_id='<run-id>' order by ts;"
```

Archived agent sessions can be inspected in:

```bash
sqlite3 data/session-archive.db "select role,created_at,substr(content,1,4000) from archived_messages where session_id='<session-id>' order by created_at;"
```

## Definition Shape

```json
{
  "name": "example-pipeline",
  "description": "What this pipeline does.",
  "version": 1,
  "input": {
    "prompt": "..."
  },
  "steps": []
}
```

### Step Display Metadata

Use `display` on every step whose data should be understandable in the Pipelines UI:

```json
{
  "name": "hydrate-chat-context",
  "description": "Fetch the latest thread and decide whether the message should proceed.",
  "type": "code",
  "function": "dispatch.hydrateChatContext",
  "input": {
    "pick": {
      "chat": "$.chat",
      "record": "$.record"
    }
  },
  "assign": "$.chatContext",
  "display": {
    "in": [
      { "label": "Chat Message", "path": "$.chat.messageText", "format": "text" }
    ],
    "out": [
      { "label": "Thread", "path": "$.thread", "format": "messages", "limit": 6, "empty": "No thread messages" },
      { "label": "Self Authored", "path": "$.selfAuthored" },
      { "label": "Suppression Reason", "path": "$.suppressionReason", "format": "text" }
    ]
  }
}
```

Display metadata conventions:

- Display rows are human-facing summaries, not a schema dump. Show the useful business value, not routing/system fields.
- Prefer labels like `Message`, `Thread`, `Company`, `Summary`, `Approved`, `Sources`, and `Webhook Delivered`.
- Promote nested paths directly. For example, show `$.selected.company.name` as `Company` rather than showing `selected` as `8 fields`.
- Supported formats are `auto`, `text`, `count`, `messages`, `records`, `list`, and `json`.
- Use `limit` for arrays and `empty` when a missing optional value is meaningful.
- Skipped steps intentionally display no data rows in the UI. Put the reason in `description`, `when`, or status rather than relying on `display`.

Step types:

- `code`: calls a registered TypeScript function.
- `agent`: starts a Wingmen session and waits for callback JSON.
- `loop`: records loop state/history and optionally jumps to a target top-level step.
- `block`: expands into a reusable step group at runtime.

## Code Step

```json
{
  "name": "normalise",
  "type": "code",
  "function": "text.normalise",
  "input": { "pick": { "text": "$.text" } },
  "assign": "$.normalised"
}
```

Built-in functions live in `src/pipelines/functions.ts`. Add tests in `src/pipelines/functions.test.ts` when adding built-ins.

User functions are loaded from disk when a pipeline starts:

```text
~/.wingmen/pipelines/shared/functions/
~/.wingmen/pipelines/users/<three-word-alias>/functions/
```

File shape:

```ts
export const name = "user.extractOptions";
export const description = "Extract options from a prompt.";
export const version = 1;

export default async function run(input: Record<string, unknown>) {
  return {
    options: [],
    prompt: String(input.prompt ?? "")
  };
}
```

Rules:

- Functions must default-export a function.
- Functions must return a JSON object.
- `.ts`, `.js`, and `.mjs` are supported.
- If `name` is missing, a scoped name is derived from the filename.
- Built-ins cannot be overridden; duplicate names are listed as `shadowed`.
- Prefer versioned files: `extract-options.v1.ts`, `extract-options.v2.ts`.

Inspect registry:

```bash
curl -sS "$WINGMAN_URL/api/pipelines/functions"
```

## Agent Step

The `directory` example is home-relative. If the pipeline runtime does not expand `~`, use the absolute agent-home path for that machine or container.

```json
{
  "name": "analyse",
  "type": "agent",
  "agent": "codex",
  "directory": "~/wingmen/<agent-directory>",
  "timeoutMs": "$.agentTimeoutMs",
  "input": {
    "pick": {
      "prompt": "$.prompt",
      "graphContext": "$.memory.graph.graphContext"
    }
  },
  "prompt": "Use graphContext as potential long-term memory context. Return structured JSON only.",
  "assign": "$.agentRaw"
}
```

Agent callback result must be an object. Avoid asking agents to return full documents in JSON; pass references like `documentUrl` and have the agent edit/read files directly when needed.

Give every agent session an explicit completion goal. Use `nextAction: "reflect"` while work, review, or reporting remains. Use `nextAction: "stop"` only for a bounded agent step whose output and handoff are genuinely complete.

For task-backed implementation, pass a self-contained brief rather than relying on the dispatch excerpt. Include the Flight Deck task/thread references, workdir, target surface, forbidden surfaces, acceptance criteria, validation, restart permission, and callback fields. Follow the worker with a manager step that independently inspects evidence and returns required pickups; let deterministic steps own Flight Deck comments and state transitions where possible.

`timeoutMs` is optional. It can be a number of milliseconds or a JSON path such as `$.workerTimeoutMs`. If omitted, agent steps wait 10 minutes for the callback. Long implementation steps should set a longer timeout. On timeout, the pipeline marks the step/run as error and attempts to stop/archive the pipeline session; it does not send a reminder prompt.

## Loop Control Step

Use flat, visible loop-control steps rather than hiding major work inside a single container when the user needs to inspect each step.

```json
{
  "id": "loop-to-critic",
  "name": "loop-to-critic",
  "type": "loop",
  "target": "critic-pass",
  "iterations": "$.reviewIterations",
  "counter": "$.reviewLoop",
  "history": "$.reviewHistory",
  "capture": {
    "critic": "$.iteration.critic",
    "response": "$.iteration.response"
  }
}
```

Seed counter input when earlier steps need it:

```json
{
  "reviewLoop": {
    "iteration": 1,
    "index": 0,
    "completed": 0,
    "total": 5,
    "done": false
  }
}
```

## Memory Graph Context Block

Use this block when an agent needs long-term memory recall.

```json
{
  "name": "recall-graph-memory",
  "type": "block",
  "block": "memory.graphContext",
  "input": {
    "pick": {
      "prompt": "$.prompt",
      "topKPerEntity": "$.topKPerEntity",
      "maxEntities": "$.maxEntities",
      "maxMatches": "$.maxMatches",
      "maxChars": "$.graphContextMaxChars",
      "agent": "$.memoryAgent",
      "directory": "$.workingDirectory"
    }
  },
  "assign": "$.memory.graph"
}
```

Runtime expansion:

1. `extract-memory-entities` agent step
2. `search-graph-memory` code step using `memory.searchEntities`
3. `consolidate-graph-context` code step using `memory.consolidateGraphContext`

Output:

```json
{
  "graphContext": "potential context from long-term memory...",
  "graphContextSources": [],
  "graphContextEntities": [],
  "graphContextWarnings": [],
  "graphContextAvailable": true
}
```

Prompt wording for consumers:

```text
graphContext is potential context from long-term memory. Treat it as a guide, not authoritative truth. Consider it where relevant, and verify against current files, records, or user input before relying on it.
```

Graph memory config:

```text
NEO4J_HTTP_URL
NEO4J_USERNAME
NEO4J_PASSWORD
NEO4J_VECTOR_INDEX
OPENAI_API_KEY
```

Optional overrides:

```text
PIPELINE_MEMORY_NEO4J_HTTP_URL
PIPELINE_MEMORY_NEO4J_USERNAME
PIPELINE_MEMORY_NEO4J_PASSWORD
PIPELINE_MEMORY_NEO4J_VECTOR_INDEX
PIPELINE_MEMORY_NEO4J_DATABASE
PIPELINE_MEMORY_EMBEDDING_API_KEY
PIPELINE_MEMORY_EMBEDDING_BASE_URL
PIPELINE_MEMORY_EMBEDDING_MODEL
```

Without graph config, memory search returns empty matches with warnings and should not break the pipeline.

## Creating Or Duplicating Pipelines

For user definitions, prefer versioned files:

```bash
cp ~/.wingmen/pipelines/shared/definitions/demo-memory-graph-context.json \
  ~/.wingmen/pipelines/users/<alias>/definitions/my-memory-pipeline.v1.json
```

When editing an existing user pipeline, create `.v2.json`, `.v3.json`, etc. Preserve the previous file unless the user explicitly asks for an in-place edit.

## Validation

```bash
cd "${AUTOPILOT_REPO:-$HOME/code/wm/autopilot}"
bun --check src/pipelines/declarative.ts src/pipelines/function-loader.ts src/pipelines/functions.ts src/pipelines/pipeline-blocks.ts src/pipelines/pipeline-loader.ts src/pipelines/pipeline-runner.ts src/pipelines/pipeline-store.ts src/pipelines/pipeline-api-routes.ts
bun test src/pipelines/pipeline-loader.test.ts src/pipelines/pipeline-runner.test.ts src/pipelines/pipeline-blocks.test.ts src/pipelines/functions.test.ts src/pipelines/function-loader.test.ts
```

If UI/server behavior changed and the user explicitly approved a managed restart in the current conversation:

```bash
pm2 restart wm-ap --update-env
curl -sS -I "$WINGMAN_URL/pipelines" | head
```

If approval is absent, do not restart. Report these commands as pending live verification.

If UI JS changed, bump `ASSET_VERSION` in `src/server.ts`.
