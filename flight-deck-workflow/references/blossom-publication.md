# Publish an existing file version to Blossom

Use this operation only when the user authorizes making the selected bytes
anonymously public. An existing hash link for a private file does not itself
publish it. Ordinary uploads and channel attachments remain private according
to their existing permissions.

From the active Autopilot checkout, inspect publication status and version IDs:

```bash
bun clis/wingman.ts flightdeck file blossom <file-id> --workspace <workspace-id> --json
```

Select the intended `version_id` from that response, then publish explicitly:

```bash
bun clis/wingman.ts flightdeck file publish <file-id> --workspace <workspace-id> \
  --version <version-id> --public --json
```

`--public` acknowledges anonymous downloading and copying. Return the verified
`blossom_url` for that selected version; do not construct URLs from unverified
metadata. The original bytes remain in Tower's S3 store. New versions are not
published automatically. The Files tab's Publish to Blossom panel performs the
same operation and offers version selection, status and URL copying.

Publishing requires workspace membership and `file.write` or `channel.write`
on the file's channel; read access or uploader identity alone is insufficient.
The completed storage object must belong to that workspace owner. Inside an
agent session use existing brokered identity/capability conventions. Do not
export keys or replace the actor with the human owner when permission is denied.

Remove only your actor's publication reference when requested:

```bash
bun clis/wingman.ts flightdeck file unpublish <file-id> --workspace <workspace-id> \
  --version <version-id> --json
```

Publish/unpublish repeats are idempotent (`changed: false`). Other actors' or
files' independent references to identical bytes, and previously public storage
objects, remain available. External copies cannot be recalled. Deleting the
file withdraws its references; retaining an older version keeps its independent
publication. Normal file and workspace permissions are unchanged.

Use structured CLI errors: 400 means invalid IDs or missing explicit version;
401 means signing/authentication failed; 403 means insufficient membership or
file/channel permission; 404 means missing/deleted/inaccessible file or selected
version; 409 means incomplete upload, missing/unverifiable bytes or a changed
immutable publication hash. Fix the cause before retrying. Changed stored bytes
require a new upload/version; never silently republish under another hash.
If a capability blocks the exact route, report it or request the narrow supported
capability through the existing workflow. A 404 from an older Tower can mean
activation is pending; check its OpenAPI before claiming the file is missing.

Supported Tower routes:

- `GET /api/v4/flightdeck-pg/workspaces/:workspaceId/files/:fileId/blossom`
- `PUT /api/v4/flightdeck-pg/workspaces/:workspaceId/files/:fileId/versions/:versionId/blossom`
- `DELETE` at the same version route

No remote destination, replication, relay announcement, or Blossom upload API is
provided by this slice. Podcast links serve local Tower bytes through anonymous
GET/HEAD and single byte ranges while an eligible publication remains.
