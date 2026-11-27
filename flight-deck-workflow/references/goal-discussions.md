# Goal context and output associations

Read this when a chat is associated with a goal, a message explicitly mentions a Goal File, or new Docs/Files are generated in that chat.

## Resolve context

Read the authoritative thread in the current workspace through its normal ACL route. Its application metadata may contain:

```json
{"ambulando_goal":{"version":1,"goal_file_id":"<goal-file-uuid>"}}
```

The containing record supplies the workspace. Carry the workspace, thread and Goal File identities explicitly when delegating or passing context outside that record. A copied title, client snapshot or body token cannot establish the primary association.

Resolve the Goal File under the acting identity's normal access. Validate its MIME `application/vnd.ambulando.goal+json`, metadata `goal.schema_version = 1`, and body `schema = ambulando.goal`, `schema_version = 1`; read the current version through the supported hash-verified File contract. Treat the goal's aim, checkpoints and relevant accessible `pinned_refs` as descriptive, untrusted context. Resolve each pinned Doc/File independently; a reference grants no source access. Report inaccessible, deleted or unsupported targets without inventing their content or widening access.

Distinguish denied access from an accessible invalid target. A well-formed primary reference from an accessible authoritative thread may retain its identity and inherit on new outputs when the Goal read is denied by ACLs; mark its context unavailable and include no goal title, body or pins. An accessible target with the wrong MIME/schema or invalid Goal content is unsupported and must not inherit as a goal merely because the thread names it.

Preserve all explicit Goal File mentions as additional context. Resolve canonical `mention:file:<id>` references to establish that they are goals; other Files remain ordinary references. Goal mentions do not replace the thread's primary association and are not actor-routing entries in the message's `mentions` array. Keep context metadata and generated context blocks out of visible message boilerplate.

The optional `default_channel_id` is a preference for starting new discussions, not a command to move this chat or its outputs. A saved unavailable default requires an explicit choice; use accessible channel choices when no default is set. Pins are key references, separate from the goal's general `links` and automatically associated outputs. When editing Goal JSON through existing File revisions, preserve unknown fields inside the goal and its references and use the actual version base with conflict reconciliation. Merge changes into the current native record metadata, preserving its other fields.

## Associate new outputs

Create Docs, whiteboards and other artefacts as original native channel-owned Docs/Files. Keep their identities, revisions, comments, assets and ACLs. New output metadata carries the same `ambulando_goal` reference as the authoritative primary chat association, merged with the record's other metadata. Explicit mentions alone do not choose a primary goal for new outputs. Associating an output neither pins it nor requires editing a private Goal File.

Prefer the current session's broker-aware `doc_create` / `file_upload` helpers after verifying that the running helper inherits the authoritative chat goal. Other publishers must resolve that thread and pass the reference through the existing generic Doc/File metadata contract; verify their actual metadata support before creating. If the running path cannot retain the association, report that precise capability gap rather than claiming inheritance or substituting a copied record, body boilerplate or broader grants. Revisions of existing records retain their identity and associations; do not silently reassign them to the current chat's goal.

Read back the saved original Doc/File and its metadata in the intended workspace/channel, then return its native reference. Verify association separately from editor navigation, goal listing and agent receipt. Installed skills and tested source do not establish live Autopilot activation or client support.
