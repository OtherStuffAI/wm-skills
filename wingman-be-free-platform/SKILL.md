---
name: wingman-be-free-platform
description: Orient and implement work across Wingman Autopilot, Tower, Flight Deck, Forgejo, WApps, pipelines, and graph memory. Use to place features, find the active repositories and supported APIs, or reason about cross-component changes.
---

# Wingman Be Free Platform

## Native Flight Deck handoff

In Flight Deck chats, task comments and document discussions, return channel-owned artefacts as `@[Artefact title](mention:file:<file-uuid>)`; ordinary Docs use `@[Document title](mention:doc:<doc-uuid>)`. Use the saved NStack File/Doc record ID, never a storage-object ID, version ID or local path. These references open in the current app and retain its workspace context. Verify the record belongs to the intended workspace/channel and report its saved revision and access mode.

A hosted Ambulando URL (including `artefactid`/`workspaceid` query URLs) is not the handoff format: it navigates away from the current client and can disrupt the app. Keep service URLs for API operations, provenance and explicitly requested external-browser sharing. Preserve legacy source URLs when reading or when the user explicitly requests legacy WApp output. A native reference grants no additional access; report a missing reference/navigation capability rather than substituting a hosted link.

Use this skill to decide where work belongs before editing. Read live code and the nearest repository instructions when they differ from this overview.

## Product boundaries

- **NStack** (historically Tower) is the reusable shared authority: NIP-98 identity, workspaces, groups, typed Flight Deck PG APIs, storage, allowlisted Nostr OIDC authentication, and graph access.
- **Flight Deck** is the human coordination UI: chat, tasks, docs, approvals, scopes, people, and WApp launchers.
- **Autopilot** runs work: sessions, Agent Direct, supervised dispatch, pipelines, triggers, apps, and WApps.
- **Forgejo** owns native accounts, organizations, teams, collaborators, repositories, permissions, OAuth credentials, Git, APIs and reviews. Tower authenticates allowlisted Nostr identities only; no Tower Git grants or reconciliation apply.
- **WApps** own business-specific UI and app data while using Tower and Autopilot through supported APIs.
- **Graph memory** is a NStack-controlled optional capability, not a raw database for agents.

Before adding an endpoint, app table, migration or shared contract, read [the pluggable application boundary](references/pluggable-app-boundary.md). Keep app domain behavior in its application namespace; extend NStack only for a demonstrated reusable capability gap. Existing typed Flight Deck contracts remain supported until a separately validated migration.

## Locate the active checkout

Current machines may use `~/code/wm`; older machines may use `~/code/wingmanbefree`. Inspect before assuming:

```bash
for root in "$HOME/code/wm" "$HOME/code/wingmanbefree"; do
  [ -d "$root" ] && printf '%s\n' "$root"
done
```

Typical current names are:

- `autopilot/`
- `tower/` (older checkout: `wingman-tower/`)
- `flightdeck/` (older checkout: `wm-fd-2/`)
- `wmapp/`

Read [references/component-map.md](references/component-map.md) when choosing a repository, API, data store, or validation path.

## Routing

- For Flight Deck chat, tasks, documents, Agent Direct, or supervised work, use `flight-deck-workflow`.
- For active-session queues, consume-on-incorporation, two-way manager/worker communication, or supervised callback inboxes, use `wingman-sessions`.
- For Tower-backed Forgejo installation, organizations, repositories, users, sharing, issues, Actions, or CI, use `forgejo-tower`.
- For declarative pipelines, use `wingmen-pipelines`.
- For WApp runtime/API work, use `wapps`.
- For live branch deployment, use `wingman-deploy`.
- For Ambulando/Tower canvases, naplets, private HTML/Excalidraw Files and canvas-linked source records, use `ambulando-canvas`.
- For Artifact WApp visual review surfaces, use `artifacts`.

## Shared invariants

- Stable actor, workspace, group, and repository UUIDs are authority keys. Readable aliases are mutable presentation.
- `group_npub` is rotating crypto identity, not a durable ACL key.
- Use existing typed NStack PG APIs for supported workspace behavior. New app features follow the pluggable application boundary; typed routes are not a reason to add app-specific server behavior. Encrypted record sync remains compatibility unless live code proves otherwise.
- Agent sessions use brokered capabilities. Never search for, expose, or persist human, bot, service, or provider secrets.
- Preserve workspace boundaries and explicit delegation. An agent signer does not silently become the human owner.
- Prefer WApps for customer-specific interfaces and local app databases.
- Prefer pipelines over legacy jobs/orchestration for new automation.
- Do not start archived runtimes.

## Change workflow

1. Identify the authoritative component and every consumer of its contract.
2. Read repository instructions, current code, OpenAPI, and deployment docs.
3. Preserve existing contracts unless the task explicitly includes migration.
4. Make cross-repository contract changes Tower-first, then update consumers in the same pass.
5. Validate with each repository's native checks and distinguish source validation from live runtime validation.
6. Report any rebuild, restart, deployment, credential, or browser smoke check that remains outstanding.

Managed runtime mutation is not implied by code-edit permission. Rebuild, restart, deploy, or alter live shared services only when the user's request includes that operation or current repository instructions make it a required in-scope validation step.
