---
name: wingman-be-free-platform
description: Orient and implement work across Wingman Autopilot, Tower, Flight Deck, Forgejo, WApps, pipelines, and graph memory. Use to place features, find the active repositories and supported APIs, or reason about cross-component changes.
---

# Wingman Be Free Platform

Use this skill to decide where work belongs before editing. Read live code and the nearest repository instructions when they differ from this overview.

## Product boundaries

- **Tower** is the shared authority: NIP-98 identity, workspaces, groups, typed Flight Deck PG APIs, storage, Git authority, and graph access.
- **Flight Deck** is the human coordination UI: chat, tasks, docs, approvals, scopes, people, and WApp launchers.
- **Autopilot** runs work: sessions, Agent Direct, supervised dispatch, pipelines, triggers, apps, and WApps.
- **Forgejo** is Tower's private Git/PR/review enforcement replica. Tower remains authoritative for repository identity and access.
- **WApps** own business-specific UI and app data while using Tower and Autopilot through supported APIs.
- **Graph memory** is a Tower-controlled optional capability, not a raw database for agents.

Do not move app-specific behavior into Tower, redefine Tower contracts in Autopilot, or make Flightlog mandatory for normal workspace work.

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
- For Tower-backed Forgejo installation, organizations, repositories, users, sharing, issues, Actions, or CI, use `forgejo-tower`.
- For declarative pipelines, use `wingmen-pipelines`.
- For WApp runtime/API work, use `wapps`.
- For live branch deployment, use `wingman-deploy`.
- For visual review surfaces, use `artifacts`.

## Shared invariants

- Stable actor, workspace, group, and repository UUIDs are authority keys. Readable aliases are mutable presentation.
- `group_npub` is rotating crypto identity, not a durable ACL key.
- Prefer typed Tower PG APIs for new shared workspace behavior. Encrypted generic record sync is compatibility unless live code proves otherwise.
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
