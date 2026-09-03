---
name: flight-deck-workflow
description: "Operate Wingman Flight Deck safely through Tower's typed PG records and Autopilot. Use for Agent Direct chat, task-backed implementation, supervised worker dispatch, task comments, documents, approvals, files, same-thread reporting, and task-state handoff."
---

# Flight Deck Workflow

## Purpose

Treat Flight Deck as the human coordination surface and Tower as its shared system of record. Use Autopilot for sessions, Agent Direct, supervised dispatch, pipelines, triggers, and managed apps.

Default rule: answer the user in the same Flight Deck workspace, channel, and thread where the request came from unless the dispatch explicitly says otherwise.

## Start With Context

Before replying or acting:

1. Fetch the freshest recoverable workspace state from Flight Deck PG/Tower.
2. Identify the active workspace, channel, thread, task, document, flow, or approval.
3. Read the authoritative record, not only the dispatch excerpt.
4. Read the latest messages/comments before responding.
5. If the latest item is from this agent, do not answer yourself. Record or return a concise skip reason.

Use the PG-native agent CLI first:

```bash
cd "${AUTOPILOT_REPO:-$HOME/code/wm/autopilot}"
bun clis/wingman.ts flightdeck context --json
bun clis/wingman.ts flightdeck thread read <thread-id> --workspace <workspace-id> --channel <channel-id> --json
bun clis/wingman.ts flightdeck task show <task-id> --workspace <workspace-id> --json
bun clis/wingman.ts flightdeck task comments <task-id> --workspace <workspace-id> --json
```

The removed `wingman.ts board` path is not a fallback. If `flightdeck` lacks an operation, use a NIP-98 signed typed Tower route under `/api/v4/flightdeck-pg`. Record a missing typed route as a product gap; do not revive Yoke or encrypted-record board tooling.

Read [references/agent-direct-and-supervision.md](references/agent-direct-and-supervision.md) before handling Agent Direct implementation, creating task-backed work from chat, supervising another session, or changing session goal/next-action metadata.

## Handle Agent Direct

Treat the complete current thread as authoritative. Do not rely on a dispatch excerpt or turn historical quoted text into a new instruction.

- Skip a dispatch only after confirming the triggering record was genuinely authored by this agent, its mapped bot identity, or its mapped workspace key. Do not infer self-authorship from mentions, labels, or quoted content.
- Acknowledge receipt promptly through the runtime's accepted activity or a concise same-thread reply.
- Keep meaningful progress, task creation, blockers, and completion connected to the originating thread while supervised work runs.
- Let the Agent Direct runtime publish the normal final response verbatim when that is its contract; do not create a duplicate final with a reply helper.

For substantial implementation requested in chat, create or update a Flight Deck task before delegating. Put the complete objective, repository/surface, constraints, acceptance criteria, validation, reporting destination, and restart authority in the task and worker brief. Review the callback, repository state, diff, and evidence before accepting the worker's completion claim.

## When To Act

Act when the dispatch, task assignment, chat thread, approval, or user explicitly addresses this agent.

Do not act as a global monitor just because related records exist. Flight Deck is shared state; ownership comes from the current workspace context, the assignee, the mentioned agent, or the specific thread/task/document that triggered the run.

If a request is ambiguous but harmless to answer, answer in the current thread and state the assumption briefly. If acting would mutate shared state, first confirm the target workspace and record.

## Choose The Right Surface

Use chat for direct conversation:

- short answers, clarifying questions, status updates, and decisions;
- conversational replies where the user needs to see the answer now;
- follow-up to the same channel/thread that started the work.

Use task records for work tracking:

- anything that needs implementation, investigation, handoff, review, or state;
- execution contracts, progress evidence, validation commands, blockers, and completion notes;
- comments that future workers need to understand without chat history.

Use documents for long-form or durable output:

- long investigations, research summaries, plans, reports, specs, review notes, or generated artifacts;
- answers too long for comfortable chat reading;
- content likely to be revised, reviewed, referenced, or shared later.

Use approvals for gated decisions:

- explicit yes/no or improve/reject checkpoints;
- flow steps where the flow definition requires approval;
- decisions that should not be buried in chat.

Use files/storage for binary or external artifacts:

- screenshots, images, PDFs, audio, exports, generated deliverables, or attachments;
- upload or link the artifact, then summarize it in chat/task/doc.

## Files And Attachments

Treat uploaded files and `storage://` links as source evidence. Read or resolve them before answering if the user references them.

Use files when the content is naturally binary or external. Use documents when the content should be editable, searchable, commented on, or used as a written deliverable inside Flight Deck.

When returning a file:

1. Upload or attach the file through the appropriate Flight Deck PG/Tower storage route.
2. Add the file link to the relevant task, document, or chat thread.
3. Summarize what the file contains and any validation performed.

Do not paste a long file dump into chat. Put the substance in a document or attach the file, then send a concise chat reply.

## Artifacts and whiteboards

If a message contains an Artifact WApp URL, a whiteboard reference, or an Excalidraw/tldraw link, treat the linked artifact as the authoritative visual workspace for that request. Open/read it before replying. If the request is to build or change it, use the Artifact WApp workflow and create a new feedback version unless the user asks to overwrite. If the request is to review it, inspect the saved scene and compare versions where available; for Excalidraw, review text, element geometry, arrows, embedded images, and visual layout, not just link metadata.

## Replying To The User

Chat is the best place to get in touch with the user. If the user asks a question in chat, send a chat reply in-thread.

Keep chat replies concise:

- answer the question directly;
- mention what was checked;
- include the next action or blocker when relevant;
- link the task/doc/approval if the detail lives elsewhere.

If the answer is long, create or update a document and reply in chat with a short summary plus the document mention.

If the work belongs on a task, update the task first, then reply in chat with the task mention and current state.

## Working A Task

Only treat tasks assigned to this agent as active work unless the user explicitly routes another task.

On first touch:

1. Read the full task, latest comments, and linked records.
2. Leave an execution-contract comment: scope, deliverable, validation.
3. Move the task to `in_progress` when active work starts.
4. If the task came from chat, include the originating channel/thread/message mention in the first task comment.

During work:

- keep essential context on the task, not only in ephemeral chat;
- add progress comments only when they clarify reality or unblock others;
- re-read recent comments before major updates or handoff.

On completion:

1. Leave validation evidence and a concise handoff comment.
2. Link any produced documents, files, approvals, or follow-up tasks.
3. Move the task to `review` when ready for the user or another reviewer.
4. Reply to the originating chat thread if the request came from chat.

Preferred API routes:

```bash
GET   /api/v4/flightdeck-pg/workspaces/:workspaceId/tasks/:taskId
POST  /api/v4/flightdeck-pg/workspaces/:workspaceId/tasks/:taskId/state
POST  /api/v4/flightdeck-pg/workspaces/:workspaceId/tasks/:taskId/comments
PATCH /api/v4/flightdeck-pg/workspaces/:workspaceId/tasks/:taskId
```

## Writing Documents

Create or update a document when the user would benefit from structure or durability.

A good Flight Deck document should:

- start with the answer, recommendation, or conclusion;
- include evidence, assumptions, and links to source records;
- separate facts from hypotheses;
- include open questions and next steps when needed;
- avoid hiding urgent blockers deep in the text.

After creating or updating a document, post a short chat or task comment that links it and explains why it matters.

Preferred API routes:

```bash
POST  /api/v4/flightdeck-pg/workspaces/:workspaceId/channels/:channelId/docs
PATCH /api/v4/flightdeck-pg/workspaces/:workspaceId/docs/:docId
POST  /api/v4/flightdeck-pg/workspaces/:workspaceId/docs/:docId/comments
```

## Document Comments

When the user asks to review, answer, or respond to comments on a Flight Deck document, treat the document comment threads as the primary surface.

- "Answer the comments" means create replies on the existing comment threads through the typed Flight Deck PG document comment route.
- Updating the document body can be useful, but it does not count as answering the comment threads unless the user explicitly asks for a document-body response section instead of thread replies.
- If a worker or pipeline cannot create comment replies, the handoff must say that plainly and must not claim the comments were replied to.
- Before completion, verify replies exist by checking child comments where `parent_comment_id` equals each root comment id.
- If the UI shows no replies, diagnose the records first: root comments have `target_record_id=<doc-id>` and replies have `parent_comment_id=<root-comment-id>`.

Preferred API route:

```bash
POST /api/v4/flightdeck-pg/workspaces/:workspaceId/docs/:docId/comments
```

## Mentions And Links

Use Flight Deck mention tags when referencing records. Do not paste raw UUIDs when a mention can be used.

Preferred helper:

```bash
node -e "import('./mycode/lib/mention.js').then(m => console.log(m.mentionTask('<task-id>', '<title>')))"
```

Mention forms:

```text
@[Task Title](mention:task:<task-id>)
@[Channel Name](mention:channel:<channel-id>)
@[Message](mention:message:<message-id>)
@[Document Title](mention:document:<doc-id>)
@[Person Name](mention:person:<npub>)
```

## Workspace Discipline

Flight Deck can span multiple workspaces. Always act in the workspace where the request belongs.

Use `--workspace` when the dispatch names a non-default workspace or when local state includes more than one relevant workspace.

Do not copy sensitive context between workspaces unless the user explicitly asks and the destination workspace is appropriate.

When replying, keep the chain of custody clear:

- chat request -> reply in the same thread;
- task dispatch -> update the same task;
- document comment -> reply on the same document when the discussion is document-specific;
- approval request -> respond through the approval action and add supporting notes where needed.

## Presentation Pattern

For short chat answers:

```text
<direct answer>

Checked: <one short evidence line>.
Next: <next action or blocker, if any>.
```

For task comments:

```text
Status: <current reality>.
Evidence: <validation, artifact, or command>.
Next: <handoff, blocker, or review request>.
```

For long work:

1. Put the full substance in a document.
2. Put the operational state on the task.
3. Put the concise user-facing summary in chat.

## Runtime Safety

Do not restart Autopilot, Tower, Flight Deck, a registered WApp, or any other managed service unless the user explicitly approves that restart in the current conversation. A prior request, task description, runbook, or general deploy permission is not current restart approval. Record the unperformed restart and required smoke test as a blocker or follow-up.

Ask the user in the originating Flight Deck thread when a decision is needed. Do not use private out-of-band contact or remote-control instructions from a portable skill. Do not imply background monitoring unless a live process in the current turn is actually running.
