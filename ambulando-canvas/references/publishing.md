# Private HTML artefacts and Excalidraw boards

Run helpers from the discovered Ambulando root. Use local authoring folders, not the legacy Artifact WApp directory. Select and verify workspace/scope/channel before creating Files.

## HTML authoring and real sandbox test

Build a folder containing `index.html` plus local CSS, JavaScript and images. Reuse the existing publisher:

```bash
bun scripts/publish-html-artifact.mjs '<local-folder>' --dry-run
bun scripts/publish-html-artifact.mjs '<local-folder>' --dry-run --out '<local-preview-dir>' --smoke
```

`--out` writes packaged HTML, a browser preview and assets. `--smoke` uses Playwright and the actual canvas sandbox builder, failing for CSP violations, script errors or failed images. Exercise important controls too; packaging success alone does not verify behavior. Keep preview/evidence folders outside tracked software or verify ignore/untracked status before writing operational evidence.

Local styles/scripts are inlined. Module imports, remote scripts/styles/fonts/images, escaping paths/symlinks, `srcset`, CSS imports and missing/mismatched image files are rejected. Limits: HTML 2 MiB, 64 images, 8 MiB each, 32 MiB total; local CSS image data is capped at 256 KiB. Use `data-asset-background="<asset-name>"` for image backgrounds or `window.wingmanAssets.url(name)` after `wingman:assets-ready`. Read the live packaging docs for supported inputs rather than bypassing validation.

Publish a new private File, optionally adding a follow-latest naplet:

```bash
bun scripts/publish-html-artifact.mjs '<local-folder>' \
  --tower '<tower-origin>' --workspace '<workspace-id>' --channel '<channel-id>' \
  --title 'Release dashboard' --canvas '<canvas-id>'
```

Update the **same File**:

```bash
bun scripts/publish-html-artifact.mjs '<local-folder>' \
  --tower '<tower-origin>' --workspace '<workspace-id>' --file '<existing-html-file-id>'
```

Omitting `--file` creates a separate File. The helper uploads private storage objects, creates File versions and a manifest naming private sibling image File/version/sha256 entries; unchanged image bytes reuse their versions. No Blossom/public URL or external WApp is required. Reading needs channel `file.read`; publishing needs `file.write`, and adding a naplet also needs canvas manage authority.

The helper uses `base_version_id`; a stale head is rejected. Inspect the competing version and reconcile intent before rerunning. Assets, HTML version and naplet binding are separate writes, not one transaction: after a timeout or failure inspect returned IDs, File head/history and snapshot before retrying. Do not claim whole-publication idempotency or blindly repeat a new-File publish. Preserve successful source writes even if linking failed.

Null HTML `source.version_id` follows latest. A pinned naplet stays on its exact version until a manager changes `source_version_id` using naplet CAS. Browsing history does not change the shared pin. Read back File/version metadata, expected assets and naplet policy before reporting success.

## Persistence and sandbox limits

The durable deliverable is the Tower File/version plus its private assets. DOM changes, JS memory, controls and browser-local state do not become shared Tower records or a durable database. The opaque credentialless iframe has scripts, data/blob assets and no ordinary network access; it cannot use host credentials, Tower APIs or a WApp backend. For durable data, create/update real supported source records through the agent or normal app surface. Do not promise offline or hard-reload recovery for an interactive draft.

Publish trusted-author code only: `connect-src 'none'` blocks ordinary requests but script can still navigate its own frame and put data in that URL before the host detects and replaces it. This is not a confinement guarantee for hostile scripts. Verify bytes/digests and source ACLs; do not embed credentials or private service URLs in HTML.

## Excalidraw

A board is a File with immutable `application/vnd.excalidraw+json` versions. Inspect text, shapes, geometry, arrow points/bindings and embedded image `files` alongside a render when images or layout matter.

```bash
bun scripts/excalidraw-board.mjs versions --workspace '<workspace-id>' --file '<file-id>'
bun scripts/excalidraw-board.mjs read --workspace '<workspace-id>' --file '<file-id>' --out '<scene.excalidraw>'
bun scripts/excalidraw-board.mjs check --scene '<scene.excalidraw>'
bun scripts/excalidraw-board.mjs publish --workspace '<workspace-id>' --file '<file-id>' \
  --scene '<scene.excalidraw>' --summary 'Add release lane' --dry-run
```

For historical reading add `--version '<version-id>'`. Read writes a sidecar recording the base. Remove `--dry-run` only for the authorized save. New boards use `create --workspace '<workspace-id>' --channel '<channel-id>' --title 'Release plan'`, optionally `--scene '<scene.excalidraw>' --canvas '<canvas-id>' --x 80 --y 80`.

Preserve element IDs and unrelated fields. Changed elements increment `version` and get a fresh random integer `versionNonce`. Delete with `isDeleted: true` plus a version bump; retain tombstones. New elements need unique IDs and complete native fields. Preserve image `fileId` bindings and `files` data URLs (PNG/JPEG/GIF/WebP/AVIF/SVG, 6 MiB each, 200 images, 24 MiB per scene). Only supported nondefault background/grid appState fields persist; viewport/selection are local.

Publish requires the base recorded by read or explicit `--base` you actually started from. Stale save exits 3 (`409 stale_base_version`) and preserves the local scene. Read latest into a different file, merge by element ID including tombstones/images, and publish against the reconciled base. Never relabel an old scene with a new base to force a save. `export` produces a lossy public copy without tombstones; never publish that copy back to the board. Canvas visibility does not grant board access.
