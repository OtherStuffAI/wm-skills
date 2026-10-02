---
name: wingman-sessions
description: Inspect and acknowledge work handled during a running Wingman Autopilot session, including revision-checked prompt queues and supervised dispatch callback inboxes. Use for queued-message accumulation, duplicate follow-up turns, and manager-session supervision.
---

# Active session work

Autopilot owns session prompt queues and supervised dispatch callback inboxes. They are separate stores. Use the supported CLI/API, never direct runtime database edits. Locate the active Autopilot checkout and follow repository instructions; common current path is `~/code/wm/autopilot`.

## Ordinary queued prompts

During authorized work, inspect this session's pending queue at useful milestones, when new work is reported, and before final handoff:

```bash
bun clis/wingman.ts session queue list
```

The CLI defaults to the calling `SESSION_ID`. Read each item's complete content and retain its exact UUID and returned `revision` string. If it references a shared task/thread, fetch that authoritative source before acting. Incorporate relevant steering into the current work; keep unrelated or unfinished items pending.

After the requested work, reporting, and necessary follow-up are handled, acknowledge only that specific item and the revision you actually read:

```bash
bun clis/wingman.ts session queue acknowledge <item-id> \
  --revision <revision-from-list> \
  --reason "Handled during current turn; result reported in the originating thread"
```

The revision is a decimal string. Do not guess it or re-read a changed revision solely to make acknowledgement succeed. An edit or dispatch claim causes a conflict: inspect the current item/status and determine what remains. An identical retry is safe within the documented retained-history window. If an older item is no longer present, inspect the record and reporting evidence rather than assuming it was never handled. Successful acknowledgement removes the item from pending work and preserves actor, time and reason in handled history. It does not deliver another prompt or interrupt the current turn.

Agent queue operations use the local capability broker and are bound to the current session. Do not substitute another session ID, impersonate the human owner, export keys, or use raw-key/unsigned requests when authorization fails. An unavailable route or missing capability on an older running version is an activation/platform gap to report and fix within restart authority.

A failed HTTP response does not prove that the agent rejected a prompt. Inspect delivery state and evidence before resolving an uncertain claim; never automatically replay work that may already have been accepted.

Do not clear the queue, delete items blindly, acknowledge merely because an item was read, or mark work handled solely to prevent another turn. Acknowledge completion only after the associated action or considered response is complete. Before ending, inspect again: newly arrived work remains pending independently.

## Supervised dispatch callbacks

Inspect the durable inbox during supervision and whenever Autopilot reports an inbox wake:

```bash
bun clis/wingman.ts dispatch inbox
```

Review each worker result against supporting repository/test evidence and current task/thread context. Take required follow-up or reporting actions, then acknowledge and close only the callbacks actually handled:

```bash
bun clis/wingman.ts dispatch acknowledge <dispatch-id>
bun clis/wingman.ts dispatch close <dispatch-id>
```

A running manager can do this before a future wake turn. Do not poll the ordinary prompt queue for supervised callbacks or queue the callback body again. Newly arriving callbacks stay unresolved; recheck the inbox before final handoff. A worker's completion claim does not itself satisfy managerial review. If the callback has not arrived, inspect the specific dispatch with `dispatch status <dispatch-id>`.

Use `flight-deck-workflow` for originating task/thread reporting and supervised worker dispatch. Do not imply background monitoring unless a live process is continuing to supervise.

## Runtime activation

Installing these instructions does not activate new Autopilot server code. Distinguish source validation, installed skills and live route availability in the handoff. Respect the current session's restart authority; never restart the Autopilot process without the required explicit authorization.
