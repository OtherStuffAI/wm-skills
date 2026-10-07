# Publish existing attachments and file versions to Blossom

Use this operation only when the user authorizes making the selected bytes
anonymously public. An existing hash link for a private file does not itself
publish it. Ordinary uploads and channel attachments remain private according
to their existing permissions.

For a chat image/file attachment, use its actual source message and existing
`storage_object_id`. Read the authoritative message first. Never create a File,
copy/reupload bytes, remove its message link, or substitute the human owner to
bypass denied source permission.

```bash
bun clis/wingman.ts flightdeck attachment blossom <storage-id> \
  --message <message-id> --workspace <workspace-id> --json
bun clis/wingman.ts flightdeck attachment publish <storage-id> \
  --message <message-id> --workspace <workspace-id> --public --json
bun clis/wingman.ts flightdeck attachment unpublish <storage-id> \
  --message <message-id> --workspace <workspace-id> --json
```

Attachment status requires `channel.read`; changes also require `channel.write`
on the actual source channel and workspace membership. Agents must participate
in the owning thread when there is one. A bare storage ID or uploader identity
is not publication authority. The CLI reads status and pins public consent to
its observed `link_id` and verified SHA-256 before publishing. The chat action
and chat-sourced Files row offer the same publication panel. Only stored bytes
become public; message text, filenames and attachment metadata remain private.

Return `attachment.blossom_url` only after the selected attachment reports public
with its verified hash. Internet URLs use Tower's configured HTTPS
`SUPERBASED_DIRECT_HTTPS_URL` origin; `BLOSSOM_PUBLIC_ORIGIN` optionally overrides
it for a distinct public origin, including private transport callers. Do not invent a URL from
unverified metadata or retry through a different identity.

Attachment publish/unpublish is idempotent and actor-specific. Other actors,
File versions and identical-byte references remain independent. Removing the
attachment link or deleting its message/thread withdraws that source's public
eligibility. Reattaching the same storage object creates a new link lifetime and
requires fresh consent; it never revives old publication automatically. Revoked
source channel write permission also makes that actor's reference ineligible.
Incomplete/missing bytes cannot be published. Changed bytes reject stale consent
and cannot replace a previously published link hash: attach a new object.

The attachment Tower route is GET/PUT/DELETE
`/api/v4/flightdeck-pg/workspaces/:workspaceId/messages/:messageId/attachments/:storageObjectId/blossom`.
PUT requires `{public:true, expected_link_id, expected_sha256}` from status.
A 409 can mean source-link identity or bytes changed; reread status and the
request before retrying. A 404 can mean the source is removed/deleted/inaccessible,
not permission to copy it elsewhere.

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
