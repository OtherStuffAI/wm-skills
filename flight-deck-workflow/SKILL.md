---
name: flight-deck-workflow
description: "Operate Wingman Flight Deck safely through Tower's typed PG records and Autopilot. Use for Agent Direct chat, task-backed implementation, supervised worker dispatch, task comments, documents, approvals, files, same-thread reporting, and task-state handoff."
---

# Flight Deck Workflow

## Same-thread progress updates

For substantial work requested in Flight Deck chat, post a brief acknowledgement into the originating workspace/channel/thread before continuing. Use the broker-aware Flight Deck chat tool or supported CLI; runtime activity, session commentary, task comments and worker logs do not substitute for a persisted chat message. Confirm the write succeeded; if it fails, report the delivery failure plainly.

While work is active, post concise same-thread updates when the implementation path is established, a blocker or scope changes, the main change is ready, and validation or activation finishes. Keep technical evidence on the task and link it from chat. Do not flood the thread with heartbeat messages or raw worker output. The manager owns these updates even when Claude or another worker does the implementation.

Keep internal coordination addressed to the worker or manager session and on the task; translate it into a user-readable status before posting to the human thread. Do not tell the user “you own activation” when the intended recipient is another agent.

Let Agent Direct publish the normal final response once when that is its contract. Do not also send that final with a reply helper. The final must explain the delivered experience, verification, limitations and next owner; include the verified build number when the app changed. Never imply continued monitoring without an active process.

## Operational handoff storage

Keep worker briefs, handoffs, run-specific evidence and private device records in Git-ignored `tmp/docs/handoffs/`, or on the authorized task/doc/file surface. Verify `git check-ignore` and that the destination is untracked before writing. Preserve and untrack accidentally tracked operational files; ignore rules do not remove historical exposure. Keep reusable product docs and code tracked.

## Readable task descriptions and updates

Apply this standard to task descriptions, task comments, and final responses that the runtime publishes as task comments. Tasks serve both users and future agents: retain the technical history and make its meaning easy to read.

- Start with a short plain-language paragraph that a user can understand on its own. For descriptions, explain the problem and intended outcome. For updates, explain what happened or was learned, the current status, and any next action or blocker. Avoid leading with internal identifiers, hashes, commands, or unexplained jargon.
- Keep useful technical detail after the opening paragraph: diagnosis, implementation constraints, decisions, validation commands and results, versions, and evidence needed for another agent to resume. Do not replace a self-contained task brief with an oversimplified summary.
- Use real paragraph breaks and Markdown to organize the detail. Use bullets for parallel findings, numbered lists for sequences, short headings for longer updates, inline code for identifiers, and fenced code blocks with a language label where useful for commands, code, or log excerpts. Leave blank lines around lists and code blocks. Avoid packing unrelated findings into one long sentence or paragraph.
- Distinguish planned work, implemented changes, validation, and live verification. A readable summary must preserve limitations and uncertainty.
- Use readable record links or mention tags; keep machine routing identifiers out of the opening paragraph. Put long logs or evidence in a linked document or authorized handoff when appropriate, preserving essential context on the task.
- Before posting, read the opening paragraph alone: does it tell the user what this task or update means? Then check that the detail is easy to scan and sufficient for another agent. Preserve actual newlines through the write tool, and read back substantial writes to verify formatting.

Example progress comment (illustrative, not a completion claim):

> The request included both the timeline and tweet count, but a later check rejected it and asked for information already supplied. The cause is identified; the fix still needs implementation and a live check.
>
> **Technical findings**
>
> - Extraction recognized Following and count `20`.
> - The support check rejected the request before retrieval ran.
> - The displayed clarification concealed that rejection.
>
> **Next step**
>
> Correct the rejection handling, then verify that the original request retrieves 20 Following tweets.

Scale formatting to the amount of information; a short update does not need a fixed set of headings.

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

## Work arriving during an active turn

Read the `wingman-sessions` skill when managing a working session's queue or supervised callback inbox. Inspect pending work at useful milestones and before final handoff. Read the authoritative referenced thread/task before acting, then immediately consume only the exact queue revision incorporated into context/plan. Consumption is not completion: retain outstanding actions on the task/plan. Dispatch callbacks use their own inbox and acknowledge/close operations. Keep unincorporated or unrelated work pending; do not clear the queue to suppress future turns.

## Handle Agent Direct

Treat the complete current thread as authoritative. Do not rely on a dispatch excerpt or turn historical quoted text into a new instruction.

- Skip a dispatch only after confirming the triggering record was genuinely authored by this agent, its mapped bot identity, or its mapped workspace key. Do not infer self-authorship from mentions, labels, or quoted content.
- For substantial work, acknowledge receipt promptly with a persisted same-thread chat reply; runtime activity alone is insufficient.
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

For explicit anonymous publishing of an existing chat image/file attachment or file version, read
[Blossom publication](references/blossom-publication.md). This covers the Files
panel, supported CLI, permissions, version selection and unpublish consequences.

Treat uploaded files and `storage://` links as source evidence. Read or resolve them before answering if the user references them.

Use files when the content is naturally binary or external. Use documents when the content should be editable, searchable, commented on, or used as a written deliverable inside Flight Deck.

When returning a file:

1. Upload or attach the file through the appropriate Flight Deck PG/Tower storage route.
2. Add the file link to the relevant task, document, or chat thread.
3. Summarize what the file contains and any validation performed.

Do not paste a long file dump into chat. Put the substance in a document or attach the file, then send a concise chat reply.

## Artifacts and whiteboards

For explicit Ambulando/Tower Canvas or naplet links/output, use `ambulando-canvas`: its HTML and Excalidraw are private Tower Files, and its tasks/docs/chats remain real source records. Do not route those requests to the legacy Artifact WApp. The Artifact WApp workflow below still applies to its own links and requested outputs.

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

## Human-friendly final updates for substantial work

For Pete-facing handoffs, explain the delivered experience in plain language (Pete's preference, 2026-10-14). After long-running or delegated work, give a self-contained final overview without waiting for Pete to ask what was implemented.

- Lead with what is now available and whether it is live, ready for review, source-only, partially delivered or blocked. Use only the status supported by evidence.
- Describe what Pete or a user can now do and see. Use a short list when several behaviors are easier to scan; explain reusable platform functionality separately when relevant.
- Summarize meaningful verification in everyday terms: what real actions were tried and what was preserved. Distinguish live checks from local or simulated tests.
- State known issues, remaining limitations and their practical impact plainly. Do not turn an untested case into a success claim; say “no known blocker in the tested experience” only when supported.
- End with review ownership or the concrete next step, plus an accessible Flight Deck task/document or hosted app link when useful.

Keep commit hashes, UUIDs, worker/dispatch identifiers, assertion counts, internal filenames and detailed technical chronology in task comments, evidence documents or ignored handoffs unless Pete needs them to act. Technical milestone reports from workers are inputs to the manager's overview, not a substitute for it. Do not present source completion as live completion. Scale the length to the work; a concise, connected explanation is better than a raw status dump. For blocked work, explain what already works, what prevents completion and the next action.

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

Use Flight Deck mention tags when referencing records. Do not paste raw UUIDs when a mention can be used. Agent-directed writes require both the visible canonical `@[Label](mention:agent:<npub>)` tag and a matching structured `mentions` entry with that exact agent npub. Derive both from one `{ npub, label }` value; visible body text alone is not routing authority. Use a broker-aware helper specified by local agent instructions when available.

```json
{
  "body": "@[Agent](mention:agent:<npub>) Continue the task.",
  "mentions": [{ "type": "agent", "npub": "<npub>", "label": "Agent" }]
}
```

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
@[Agent Name](mention:agent:<npub>)
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
