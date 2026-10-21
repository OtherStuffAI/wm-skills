---
name: wingman-sessions
description: Inspect and consume steering incorporated during a running Wingman Autopilot session, recover uncertain deliveries, and manage revision-checked prompt queues and supervised dispatch callback inboxes. Use for queued-message accumulation, duplicate follow-up turns, and manager-session supervision.
---

# Active session work

Autopilot owns session prompt queues and supervised dispatch callback inboxes. They are separate stores. Use the supported CLI/API, never direct runtime database edits. Locate the active Autopilot checkout and follow repository instructions; common current path is `~/code/wm/autopilot`.

## Ordinary queued prompts

During authorized work, inspect this session's pending queue at useful milestones, when new work is reported, and before final handoff:

```bash
bun clis/wingman.ts session queue list
```

The CLI defaults to the calling `SESSION_ID`. Read each item's complete content and retain its exact UUID and returned `revision` string. If it references a shared task/thread, fetch that authoritative source before acting. Incorporate relevant steering into the current work; keep unrelated or unincorporated items pending.

Immediately after incorporating an item into context or the active plan, consume only that item and the revision actually read. Consumption is not task completion: retain unfinished actions, decisions, reporting and follow-up on the task/plan; do not leave an incorporated prompt pending until completion:

```bash
bun clis/wingman.ts session queue consume <item-id> \
  --revision <revision-from-list> \
  --reason "Incorporated steering into the active plan; outstanding actions tracked on task"
```

The revision is a decimal string. Do not guess it or re-read a changed revision solely to make consumption succeed. An edit or dispatch claim causes a conflict: inspect the current item/status and determine what remains. An identical retry is safe within the documented retained-history window. If an older item is no longer present, inspect the record and reporting evidence rather than assuming it was never handled. Successful consumption removes the item from pending work and preserves actor, time and reason in handled history. It does not deliver another prompt or interrupt the current turn.

Own queue list/consume/reconcile operations use the local capability broker and are bound to the current session. This scope does not grant writes to another session’s queue. Do not substitute another session ID, impersonate the human owner, export keys, or use raw-key/unsigned requests when authorization fails. An unavailable route or missing capability on an older running version is an activation/platform gap to report and fix within restart authority.

If `consume` is unavailable or denied, do not claim success. Inspect the supported `acknowledge` endpoint semantics: where it records the same exact revision in handled history without declaring task completion, it can record incorporation with an explicit reason and outstanding task/plan obligations:

```bash
bun clis/wingman.ts session queue acknowledge <item-id> \
  --revision <revision-from-list> \
  --reason "Incorporated steering; consume unavailable; outstanding work remains on task"
```

Report this as compatibility acknowledgement, not successful consume-route validation. If semantics or authority cannot be verified, leave the item pending and report the gap. Neither endpoint's handled state completes a Flight Deck task. Do not modify runtime or restart to make cleanup succeed without separate authorization.

A failed HTTP response does not prove that the agent rejected a prompt. Inspect delivery state and evidence before resolving an uncertain claim; never automatically replay work that may already have been accepted.

Do not clear the queue, delete items blindly, consume merely because an item was listed/read, or consume solely to suppress a follow-up turn. Record what was incorporated in the reason. Before ending, inspect again: newly arrived work remains pending independently.

## Active manager/worker communication

Every supervised brief must identify the manager session, Autopilot checkout/URL or connection context when needed, task and report destination. Workers ask the manager questions instead of silently guessing a consequential decision. Include worker session/task, decision needed, recommendation and blocking status. Continue independent work while waiting; pause dependent actions.

From the identified Autopilot checkout, verify the live CLI and broker authority before sending. For the current broker scope, use authorized session messaging:

```bash
bun clis/sessions.ts send <manager-session-id> "<question and routing context>" --bot-crypto --json
```

Prefer queue-add only when that exact destination is specifically authorized; exact-session queue capability commonly denies cross-session queue-add:

```bash
bun clis/sessions.ts queue-add <manager-session-id> "<question and routing context>" --bot-crypto --json
```

Use `--url <autopilot-url>` only for the connection named in the brief; remote access needs its own authorized broker/delegation. Send queues while the target is busy and may start a turn when idle; inspect the actual response. Queue-add is queued work, not an immediate interrupt. Neither command promises that a busy manager has read the question. Do not use interrupt/queue-next as a messaging workaround.

Own-queue authority and authorized messaging to a specific manager/worker are distinct. Never change SESSION_ID to consume another session’s work, export keys, impersonate an owner, or bypass a denial. If both supported paths fail, record the gap on the task and hand back to the manager; no runtime change or restart is implied. Do not send to unrelated live human sessions.

The manager retains dispatch and worker session IDs, actively checks its own queue and worker progress at meaningful milestones, consumes incorporated questions in its own queue, and sends answers through the authorized send path to the exact worker. Both sides regularly inspect their own queues during active work, at decisions/validation and before handoff, and immediately consume exact incorporated revisions. This is active-turn supervision, not background polling. Completion uses the normal supervised callback, not a duplicate queued final. Callback review/acknowledge/close remains separate.

## Resolving uncertain delivery

If `deliveryActive` is true, the item is still Dispatching and reconciliation is refused. After a delivery attempt finishes, an uncertain claim is shown as unresolved. A claimed item may have crossed the send boundary even when no HTTP response arrived. Wait until the delivery attempt has finished, inspect its `deliveryId`, claim state and supporting output, then resolve the exact claim with the revision and claim token returned by list:

```bash
bun clis/wingman.ts session queue reconcile <item-id> \
  --revision <revision-from-list> \
  --claim-token <claim-token-from-list> \
  --resolution accepted \
  --reason "Confirmed this delivery was accepted; matching result inspected"
```

`accepted` records verified acceptance without sending again. `--resolution retry` explicitly permits another delivery and may duplicate an earlier accepted attempt. Choose it only after considering the evidence, duplicate consequences and task authority; explain the decision in the reason. Neither a lost response nor elapsed time proves rejection. Do not reconcile a delivery that is still active, guess its token, or refresh a changed revision merely to bypass a conflict. Unresolved delivery remains visible and is never automatically replayed after a timeout.

Queue history is bounded: the API/UI retains at most 100 recent full handled events, with terminal retry metadata retained for up to seven days and the most recent 1,000 terminal records per session. Older records may have compacted content; beyond the retained retry window, a missing item is not proof that it was never handled. Pending and unresolved claims are not pruned.

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

## Final supervision report

When substantial supervised work reaches handoff, synthesize worker reports into a human-friendly final overview using `flight-deck-workflow`'s final-update guidance. Lead with what users can now do and the actual delivery status, summarize meaningful verification, state remaining issues or untested cases, and give the review owner/next step with an accessible evidence link. Keep worker IDs, commits and raw technical evidence on tasks or handoffs unless needed for a decision. An acknowledged callback alone does not establish live completion.

## Runtime activation

Installing these instructions does not activate new Autopilot server code. Distinguish source validation, installed skills and live route availability in the handoff. Respect the current session's restart authority; never restart the Autopilot process without the required explicit authorization.
