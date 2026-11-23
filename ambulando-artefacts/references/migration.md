# Controlled templates and selected-version import

Read `docs/artefact-templates-and-migration.md` in the authorized Ambulando checkout, then inspect `scripts/migrate-artefact.mjs`, `scripts/artefact-migration.mjs`, `src/artefact-templates.js`, `src/system-flow-schema.js` and `src/system-flow.js`. These are existing source contracts, not evidence of deployment or new native support. Use existing NStack private Files/storage and File revision CAS; there is no separate migration backend route.

## Templates and editable flow

Controlled starters currently include blank/working-brief Docs, Excalidraw whiteboard, interactive HTML explorer and System Flow; styles are `default` and `paper`. Templates initialize content only and never rewrite existing work. File `metadata.artefact` uses `schema_version: 1`, `type`, `format_version: 1`, `editor_id`, with optional template/style IDs and versions. Unsupported descriptors fail closed. Discover IDs in source rather than inventing them. Future plugins need an approved type/editor/format contract, validator, source/asset/ACL adapters, rollback and host compatibility tests; no open remote installation is implied.

System Flow is a File with MIME `application/vnd.ambulando.system-flow+json`, type `system-flow`, editor `builtin.system-flow`. Its editable JSON retains legacy `flow.json` schemaVersion 1–3; schema 3 requires the complete hydrated `scenes` map. Preserve diagrams, IDs, container relationships, positions, typed nodes/arrows, owners, descriptions, decisions, retries, images and linked detail-flow/whiteboard references. Never substitute generated HTML or a screenshot for source.

The bounded web editor supports diagram selection, node fields/position, edge endpoints/labels and validated JSON edits. Its SVG overview simplifies legacy handles/routing. Linked whiteboard scenes are preserved; replacement is rejected here, so edit those scenes in the legacy editor. Feedback and legacy sharing/unlock codes stay at the original URL. Native flow editing remains unsupported. Save against the captured `base_version_id`; keep drafts on conflict, reconcile current source, and inspect history after an uncertain save. Restore by an explicitly reviewed new revision, never changing history.

## Prepare and verify audience

Migration must be explicitly approved for the selected source and destination. Read the legacy catalogue/index, exact saved source, scenes/assets and access; resolve the latest meaningful published version from lineage, not timestamps alone. Keep drafts distinct. Read/render the original when layout matters. Existing originals, history, comments and drafts remain accessible in the legacy app.

Compare all effective readers and relevant edit authority: source ACL, explicit destination grants, inherited groups and administrators. Verify workspace/scope/channel from authoritative context and retain access evidence in ignored operational records. `--audience-verified` only acknowledges this human/agent check; the importer does not prove audience equivalence. A private label or successful broker read is insufficient. If destination access is broader or unclear, ask the manager and continue independent work; do not change grants to make import succeed.

Run from the authorized checkout with an already inspected local source folder:

```sh
bun scripts/migrate-artefact.mjs --folder '<selected-version-folder>' \
  --type system-flow --source-url '<canonical-version-url>' \
  --source-version '<version>' --title '<original title>' --dry-run
```

Supported types are `system-flow`, `excalidraw`, `html`. The source URL must omit credentials, query access codes and fragments. Flow imports read `flow.json`, `index.html` and schema-3 `scenes/*.json`; boards read `excalidraw-scene.json` and `index.html`. Missing/unreferenced scenes, invalid source, unsafe paths or unsupported content stop import. HTML packaging validates local authoring files/assets; review warnings rather than bypassing them. Only separately reviewed known history/external navigation limitations may use `--legacy-navigation-reviewed`; this preserves a provenance limitation and original link, without enabling iframe networking/navigation.

Dry-run validates/packages source and reports hashes/manifest/assets; it performs no destination ACL or existing-mapping verification. After audience proof and reviewing dry-run output:

```sh
bun scripts/migrate-artefact.mjs --folder '<selected-version-folder>' \
  --type system-flow --source-url '<canonical-version-url>' \
  --source-version '<version>' --title '<original title>' \
  --tower '<authorized-nstack-origin>' --workspace '<workspace-id>' --channel '<channel-id>' \
  --audience-verified --receipt '<new-ignored-receipt-path>'
```

The receipt must not already exist. Source exports, previews and receipts require verified ignored/untracked locations. Do not put private source bytes or access evidence in reusable guidance.

## Provenance, retry and readback

The importer writes a private sibling source archive first, then private HTML image Files where needed, then the editable primary File. The archive preserves the selected authoring bytes and per-file hashes: it is not a whole legacy app backup. Board normalization can omit viewer-local state and HTML packaging can inline styles/scripts; runtime caches, drafts/comments and earlier history remain legacy. Primary metadata includes `original_source` File/version. `metadata.migration` records canonical `source_url`, `source_version`, source-manifest `source_sha256_hex`, role and `history_policy: latest-selected-only`.

Destination discovery currently requests Files with `limit=200` and fails closed at 200 entries, a cursor, `has_more` or `partial`; it does not follow pagination itself. Obtain complete discovery/reconciliation before proceeding, not a guessed absence or forced duplicate. Matching URL/version mappings reuse verified Files; changed bytes or duplicate role mappings require review. The first immutable primary revision is compared to imported bytes; newer destination edits are retained, not overwritten by a repeat import.

Writes are sequential and not transactional or server-unique. Never run competing imports for one source. After interruption or unconfirmed creation, inspect complete destination provenance, accepted File IDs/heads, exact versions and hashes before retrying. Retain successful partial Files; do not delete them as cleanup or blindly replay creation. A storage upload can precede File creation, so a failed command alone does not establish that nothing was saved.

Read back archive, primary and assets with exact hashes; compare original/import rendering, exercise important controls and typed edit/save/reopen, verify read-only/denied behavior, and restore initial source through a reviewed new revision. Distinguish local/synthetic tests, real NStack writes using local web source, deployed web checks and native/device checks. HTML forms remain blocked without `allow-forms`; do not expand sandbox permissions for a signup preview or report it as a working signup flow. Report unverified image/ACL/HTML behavior as pending, not success. Latest-only import does not authorize full-history migration, bulk moves, deletion, redirects or retirement.
