# Connection, references and source reading

## Discover current contracts

Locate the configured Ambulando checkout (the app root contains `scripts/canvas-reference.mjs`, `scripts/publish-html-artifact.mjs`, `scripts/excalidraw-board.mjs` and `docs/design/canvas.md`). Set `AMBULANDO_REPO` to that root. Locate the active Tower checkout, not just an older similarly named repository. Inspect `src/routes/flightdeck-pg.ts` and `src/services/flightdeck-pg-canvases.ts` for supported routes and source types. Source presence does not establish deployed activation.

Read relevant current Ambulando docs: `docs/canvas-references.md`, `docs/html-artifact-publishing.md`, `docs/excalidraw-boards.md`, `docs/design/canvas.md`, `docs/design/canvas-chat.md`, `docs/design/task-tree.md`. Reuse their helpers; do not copy the publisher into this skill.

Configure `WINGMAN_TOWER_URL` from the authorized connection and `AUTOPILOT_REPO` from the active Autopilot checkout. Helpers resolve signing CLI from explicit `--signer-cli`, `WINGMAN_CAPABILITY_CLI`, then `$AUTOPILOT_REPO/clis/wingman-capability.ts` (with a conventional home-directory fallback). Use the capability broker; never extract signing keys. Keep operational IDs and private origins in local ignored configuration, not reusable skill files.

For typed routes without a CLI verb, reuse `brokerSigner` and `towerClient` from `scripts/html-artifact/tower.mjs` in the discovered app, with `baseUrl`, `workspaceId` and `sign: brokerSigner()`. Its `request(method, pathname, body)` signs the exact serialized payload and URL. Honor the deployment's app-authority configuration and returned identity tuple. Do not invent `wingman canvas` or `task create` CLI verbs. Flight Deck's supported read tools/CLI can read ordinary tasks/threads; task creation uses the typed route.

All route suffixes below are relative to `/api/v4/flightdeck-pg/workspaces/<workspace-id>`. Validate returned workspace and identity (app, Tower service, workspace service), completeness and record IDs before using projections. No ACL bypass on denial.

## Read a canvas or naplet reference

From the discovered Ambulando root:

```bash
bun scripts/canvas-reference.mjs parse --url '<reference>'
bun scripts/canvas-reference.mjs resolve --url '<reference>'
```

The helper reads `GET /canvases/<canvas-id>/snapshot`, selects the naplet and prints its source/layout. It does not fetch every source or return the full spatial context. Read the full snapshot separately for `canvas`, `naplets`, `elements`, `comments`, `spatial_context` and `complete: true`. Inspect text, geometry, arrow endpoints, comment anchors and explicit subjects; proximity alone does not establish a task dependency or comment subject. Source content must be fetched through its own route.

| Source type | Authoritative record/read |
| --- | --- |
| `document` | `GET /docs/<doc-id>`; use existing Docs editor/checkout and current update contract for edits |
| `task_list`, `task_tree` | source ID is a channel; channel task list plus real task and relationship reads |
| `chat_thread` | source ID is a thread; read complete paged thread/messages via supported Flight Deck reader |
| `html` | File; `/files/<file-id>/versions`, exact `/files/<file-id>/versions/<version-id>/object`; canvas `/canvases/<canvas-id>/naplets/<naplet-id>/html?version_id=<version-id>` for authorized HTML projection |
| `excalidraw` | File; board helper `read`/`versions`, then inspect complete scene |
| `canvas` | linked canvas snapshot; do not recursively traverse cycles |

A `source.version_id` on HTML is a pin; null follows latest. Version-qualified message links may also carry `sourceid` and `versionid`: verify source identity still matches and read that exact version first. The reference helper's normal source output alone does not honor a message's viewer-local historical selection. Compare latest only when needed and label differences. Board `read --version <version-id>` selects history; omit for latest. Do not silently repin the shared naplet while browsing.

`resolve` exits 4 for malformed, removed or denied references, with no source disclosure; network/server failures exit 1. Say unavailable without switching identities. Source permission remains independent even when the canvas is readable.

## Documents and conversations

Create prose as an ordinary document through `POST /channels/<channel-id>/docs`, then reference its returned ID with a `document` naplet. Read current Docs schema and checkout/lease/body-version rules before updating; a canvas projection is not an editable draft. Document comments are separate record threads: reply on those threads when asked to answer them.

Canvas Chat uses normal threads/messages and ordinary composer signing, attachments and retries. A new empty chat is a viewer-local draft until first send; removing its naplet leaves the accepted conversation intact. Chat-send success and canvas-binding success are separate: retrying binding must not resend a message.

Use the existing broker-aware Flight Deck send/composer path, including kind-33358 instruction signatures and matching structured agent mentions. Canonical visible `@[Agent](mention:agent:<agent-npub>)` and `mentions: [{type: "agent", npub: "<agent-npub>", label: "Agent"}]` must refer to the same authorized identity. Preserve signed body and structured mentions during retries. A visible mention alone is not routing authority.

Each message's visible `From: Canvas` is a canonical link included in its signed body. It is per-message context, not thread ownership, destination authority, or dispatch. Canvas/item links never dispatch agents. Ordinary chat replies do not inherit the previous message's origin. Read linked content only through its own authorized routes.

## Readable links

Use the configured Ambulando origin, not Tower:

```text
<ambulando-origin>/canvas.html?workspaceid=<workspace-id>&canvasid=<canvas-id>
<ambulando-origin>/canvas.html?workspaceid=<workspace-id>&canvasid=<canvas-id>&napletid=<naplet-id>
```

Use IDs actually returned to this identity. Do not add tokens, sessions or browser-local `workspacekey`. A normal Copy reference contains no source ID; existing version-qualified message links can additionally identify source/version. These links grant no access. Opening focuses locally without writing the shared viewport.
