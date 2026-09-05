# Wingman Component Map

Read this reference when locating code or deciding where a feature and its state belong.

## Tower

Typical repo: `~/code/wm/tower` or `~/code/wingmanbefree/wingman-tower`.

Owns workspaces, membership, group UUIDs and epochs, NIP-98 verification, typed Flight Deck PG APIs, storage metadata, allowlisted Nostr OIDC authentication for Forgejo, OpenAPI, migrations, and graph routes.

Start with:

- `README.md`
- repository `AGENTS.md`/`agents.md`
- `src/types.ts`
- `src/openapi.ts`
- `src/server.ts`
- `src/routes/`
- `src/services/`
- `src/schema/`

Use Tower Postgres for shared platform records. Do not give ordinary agents raw database credentials.

## Flight Deck

Typical repo: `~/code/wm/flightdeck` or `~/code/wingmanbefree/wm-fd-2`.

Owns the browser materialized view and human workflows. Current shared state should use Tower's typed PG routes and local Dexie materialization. Resolve scope/channel/thread context explicitly; do not use stale UI selection as an implicit write target.

Start with repository instructions plus `src/api.js`, PG hydrators/adapters, translators, sync manager, and task/channel state modules.

## Autopilot

Typical repo: `~/code/wm/autopilot` or `~/code/wingmanbefree/autopilot`.

Owns sessions, Agent Direct, dispatch, pipelines, triggers, app registry, WApp lifecycle, and capability brokerage. Prefer its CLI and APIs over editing runtime JSON or SQLite directly.

Useful entrypoints:

```bash
cd "${AUTOPILOT_REPO:-$HOME/code/wm/autopilot}"
bun clis/wingman.ts flightdeck ...
bun clis/wingman.ts dispatch ...
bun clis/wingman.ts ...
```

Inspect `$WINGMAN_URL`, env, and app registry before assuming a port. Do not start an ad hoc Flight Deck/WApp server when the app is managed by Autopilot.

## Forgejo

Forgejo runs inside Tower's Docker stack. It stores Git objects and provides the repository, issue, pull-request, review, and optional Actions UI. Tower authenticates allowlisted Nostr identities only. Forgejo owns native accounts, usernames, organizations, teams, collaborators, all repository permissions, OAuth credentials, Git and API operations. No Tower Git grant or permission reconciliation applies.

Use the `forgejo-tower` skill for all Forgejo setup and collaboration work.

## WApps and data placement

- Shared workspace/platform data: Tower Postgres.
- Business-specific app state: WApp database, commonly SQLite for single-node apps.
- Graph/memory relationships: Tower graph API and graph Postgres.
- Files: Tower storage or the WApp's explicit storage boundary.

Do not add another data store until these boundaries have been evaluated.

## Validation shape

Always prefer the repository's own instructions. Common checks are:

```bash
cd "${TOWER_REPO:-$HOME/code/wm/tower}"
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --build
curl http://127.0.0.1:3100/health

cd "${FLIGHTDECK_REPO:-$HOME/code/wm/flightdeck}"
bun test
bun run build

cd "${AUTOPILOT_REPO:-$HOME/code/wm/autopilot}"
bun test
```

A successful build does not prove a managed app is running the new version. Verify the runtime only when that mutation/check is in scope.
