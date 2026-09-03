# Agent Direct And Supervised Work

Use this reference for Agent Direct chat, task-backed implementation, session-to-session dispatch, and session lifecycle metadata.

## Agent Direct Intake

1. Resolve the dispatch workspace, channel, thread, trigger message, current agent identity, and originating task if present.
2. Fetch the complete current thread from Tower before deciding what to do:

```bash
cd "${AUTOPILOT_REPO:-$HOME/code/wm/autopilot}"
bun clis/wingman.ts flightdeck thread read <thread-id> \
  --workspace <workspace-id> --channel <channel-id> --json
```

3. Treat the fetched thread as authoritative context. Treat only newly eligible human messages as instructions for the current turn.
4. Skip only when the trigger author is genuinely this agent, its mapped bot identity, or its mapped workspace key. Record the skip reason when the runtime supports dispatch outcomes.
5. Ensure the user sees prompt receipt. Prefer Autopilot's `accepted` activity (`Message received`); otherwise send one concise same-thread acknowledgement.
6. Keep the same thread informed when a task is created, a blocker changes the plan, or the supervised work reaches a meaningful milestone. Avoid noisy heartbeat updates.
7. Return the final in the same thread. If Agent Direct publishes the session's normal final verbatim, make that final the user-facing update and do not call a reply helper again.

## Turn Chat Into Task-Backed Work

Create or update a Flight Deck task before starting substantial code, docs, migrations, configuration, generated artifacts, or other durable implementation.

Use `bun clis/wingman.ts flightdeck ...` only for operations exposed by the live CLI. Task creation is not currently exposed. Use an existing local NIP-98 helper, or make a signed Tower request with the Flight Deck app identity:

```text
POST /api/v4/flightdeck-pg/workspaces/<workspace-id>/channels/<channel-id>/tasks
Authorization: Nostr <NIP-98 event for the exact URL, method, and payload>
x-flightdeck-pg-app-npub: <Flight Deck app identity>
content-type: application/json
```

```json
{
  "title": "<outcome>",
  "description": "<self-contained brief>",
  "state": "in_progress",
  "thread_id": "<originating-thread-id>"
}
```

Do not publish signing keys or app identities in the task, handoff, logs, or portable skill. Prefer an existing local helper over assembling repeated signed requests by hand.

Make both the task and worker brief self-contained. Include:

- objective and user-visible outcome;
- repository, working directory, target surface, and forbidden surfaces;
- source thread/task/document mentions and required files;
- constraints, especially preservation of concurrent work and restart/deploy authority;
- acceptance criteria and exact validation expectations;
- required task comments, state transition, callback evidence, and final reporting destination.

Add an execution-contract task comment before or when work starts. Keep validation, blockers, changed files, commits, and handoff evidence on the task. Move it to `review` only after managerial review passes.

## Dispatch A Supervised Worker

Use `wingman.ts dispatch create` as the ordinary session-to-session path. Prefer a prompt file so the handoff remains reviewable and avoids shell quoting errors.

```bash
cd "${AUTOPILOT_REPO:-$HOME/code/wm/autopilot}"
bun clis/wingman.ts dispatch create \
  --agent codex \
  --directory <working-directory> \
  --name "<short worker name>" \
  --prompt-file <repo-local-handoff.md>
```

Callbacks default to the calling session through `SESSION_ID`. Use unmonitored dispatch only when the user explicitly wants it; `--callback false` removes the durable supervisor callback.

Capture the returned dispatch and worker session IDs. Give the worker explicit lifecycle metadata at the start, or require it to set its own:

```bash
bun clis/sessions.ts metadata-update <worker-session-id> \
  --goal "<concrete completion condition>" --next-action reflect
```

Use `reflect` while work, review, reporting, or handoff remains. Set `stop` only when the goal is genuinely complete and all required evidence and handoff have been delivered:

```bash
bun clis/sessions.ts metadata-update <worker-session-id> --next-action stop
```

## Review And Close The Dispatch

The callback is a durable notification, not automatic acceptance. Inspect the worker callback and the claimed evidence. For implementation, inspect the live worktree, diff, tests/build results, commit, and push state. Re-dispatch a focused pickup when required.

If no terminal callback arrives, inspect explicitly; do not assume running, failed, or complete:

```bash
bun clis/wingman.ts dispatch status <dispatch-id>
```

After reviewing the callback and updating the authoritative task/thread, acknowledge and then close the dispatch:

```bash
bun clis/wingman.ts dispatch acknowledge <dispatch-id>
bun clis/wingman.ts dispatch close <dispatch-id>
```

Use `dispatch retry <dispatch-id>` only when a terminal callback exists but delivery needs retrying. A missing terminal callback still requires `dispatch status` and direct inspection of the worker session.

## Managed Runtime Boundary

Never restart Autopilot, Tower, Flight Deck, registered WApps, or other managed services without explicit restart approval in the current conversation. Build and static asset generation do not imply restart authority. When approval is absent, report the exact pending restart and smoke test instead of claiming the running system is updated.
