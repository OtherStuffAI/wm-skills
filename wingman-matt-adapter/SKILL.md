---
name: wingman-matt-adapter
description: Route Matt Pocock skill work in Wingman to the verified channel's tasks and Ambulando Docs/Artefacts, preserving identity, revisions and access. Use when those skills consume or save Wingman records; standalone work keeps its configured tracker and files.
---

# Wingman persistence adapter

## Native Flight Deck handoff

In Flight Deck chats, task comments and document discussions, return channel-owned artefacts as `@[Artefact title](mention:file:<file-uuid>)`; ordinary Docs use `@[Document title](mention:doc:<doc-uuid>)`. Use the saved NStack File/Doc record ID, never a storage-object ID, version ID or local path. These references open in the current app and retain its workspace context. Verify the record belongs to the intended workspace/channel and report its saved revision and access mode.

A hosted Ambulando URL (including `artefactid`/`workspaceid` query URLs) is not the handoff format: it navigates away from the current client and can disrupt the app. Keep service URLs for API operations, provenance and explicitly requested external-browser sharing. Preserve legacy source URLs when reading or when the user explicitly requests legacy WApp output. A native reference grants no additional access; report a missing reference/navigation capability rather than substituting a hosted link.

Apply this contract when the request names Wingman/NStack/Flight Deck/Ambulando records, arrives through a Wingman channel/task dispatch, or the repository explicitly configures Wingman persistence. A Git remote or installed skill alone is not activation. Outside that context, retain Matt's standalone workflow.

Inside Wingman, this contract **supersedes conflicting upstream saving and tracker defaults**, including defaults in supporting templates: GitHub/GitLab issues, `.scratch` tickets, repo/OS-temp research, glossary/ADR/questionnaire paths, handoff directories, report opening and throwaway research branches. Preserve the underlying interviews, decision frontier, tracer bullets, primary-source research, tests, review methods and invocation policies. Existing user choices and repository instructions still govern code, branches, commits, approvals and delegation.

## Resolve before consuming or saving

1. Read `flight-deck-workflow` and, for durable output, `ambulando-artefacts` from this harness's installed skills. Read `wingman-sessions` for active-session steering/handoff. If a required skill/helper is absent, report the missing dependency; use supported read-only discovery while resolving it.
2. Fetch the full current task/comments and originating thread through the authorized broker-aware tools. Confirm workspace, scope, channel, source thread/task and intended destination from those records. Read channel details and current membership/access evidence for the signing agent and intended readers. A link, pin, canvas or successful read alone does not prove write authority or audience. Cross-channel work requires verified destination membership and explicit ownership, with links back to its origin.
3. Discover existing records through complete channel task/Doc/File listings, then read likely matches and comments. Match source identity/provenance and purpose, not title alone. Stop at ambiguous duplicates, inaccessible matches or truncated discovery; resolve pagination before claiming absence. Keep provenance in supported metadata or a readable source section: source record/URL/version, purpose and parent/output links. It is not a new database.
4. Capture the record's actual editing base before authoring. Reconcile concurrent changes, comments and assets against that base. Keep unchanged fields and relationships. On rejection, save the draft in verified ignored operational storage, read the new source separately and reconcile; never refresh only the token to force an old draft through. After uncertain creation/save, inspect accepted records/history before retrying.

## Route outputs

| Output | Authoritative destination |
| --- | --- |
| Wayfinder map, decision tickets, spec execution/index, implementation tickets, triage briefs | Relevant channel task board; task comments hold resolutions and evidence. |
| Specification body, research, glossary, ADR, questionnaire, architecture report, learning records, durable retrospective | Channel Docs/Artefacts; revise the existing identity. Link the canonical Doc from the execution task. |
| Architecture whiteboard or visual proposal | Channel editable Excalidraw File with source/assets retained. Canvas placement is optional. |
| System Flow | Channel typed editable File using the verified controlled schema/editor. |
| Worker brief, logs, run-specific evidence, private captures, one-off wizard | Verified untracked, Git-ignored `tmp/docs/handoffs/`, or authorized task/doc/file surface. |
| Reusable product code/docs, skill source, tests, repeatable wizard | Target source repository under its instructions; link the channel decision/record. |

Read [operation contracts](references/operations.md) for the selected output before writing. Setup records Wingman as tracker, channel Docs as durable domain/spec destinations, and the mapping of Matt's triage/wayfinder semantics to supported task fields. It does not create GitHub labels or replace existing project instructions. An already explicit Wingman route needs no repeated tracker-choice question; unresolved destinations still require clarification.

Specs have one canonical Doc body plus a linked execution/index task when work tracking is needed. Wayfinder maps remain tasks and index decisions instead of duplicating them. Domain docs are updated as terms/decisions crystallize; retain glossary and ADR formats in the canonical Docs. Repository consumer pointers may link those Docs when authorized, without silently creating a second authoritative copy. Operational handoffs point to durable records rather than copying private source into tracked docs.

Prototype code can remain runnable under the repository's approved workflow. Save shareable single-file demonstrations/reports to private channel HTML Files using supported packaging; bundle dependencies locally for the existing sandbox instead of relying on Tailwind/Mermaid CDNs. A server-dependent prototype needs its actual authorized app URL plus source/task pointers; never claim a static export is the working app. Preserve question, verdict and decision-rich snippets. Teaching lessons/references use Docs/HTML Files and real record links; preserve the teaching method without pretending browser memory is shared storage.

## Completion and handoff

Read back saved identity, body/source, revision, dependencies and private assets. Keep comments attached to their original record and answer actual comment threads when requested. Report direct authenticated record links copied by the current client contract, channel, saved revision/access mode, source commit for code, and checks performed. Separate local validation, live API writes, browser interaction, native/device behavior and remote skill discovery. Missing support is an explicit gap, not permission to substitute another tracker, a static flow, an old-app publication, broader ACLs or service restarts. The supervising manager owns human chat and final acceptance when dispatched that way.
