# Canvas layout, linking and annotations

Read the complete authorized snapshot before changing layout. Coordinates `x`, `y`, `width`, `height`, `z` are canvas world coordinates, not screen pixels; account for viewport pan/zoom when interpreting screenshots. Preserve positions, unknown fields, native elements, comments and unrelated naplets. Use actual bounding boxes to place new content without covering existing content; do not rewrite the whole canvas for a local request.

All suffixes use the workspace prefix documented in reading.md. Existing typed routes:

| Operation | Contract |
| --- | --- |
| Read | `GET /canvases/<canvas-id>/snapshot` |
| Add reference | `POST /canvases/<canvas-id>/naplets` with `source: {type, id, version_id?}`, `layout`, optional display `title` |
| Move/resize/title/pin | `PATCH /canvases/<canvas-id>/naplets/<naplet-id>` with `expected_row_version` and changed fields |
| Remove view | `DELETE /canvases/<canvas-id>/naplets/<naplet-id>` with `expected_row_version` |
| Native drawing/text | `POST /canvases/<canvas-id>/elements`; element PATCH/DELETE use `expected_row_version`; inspect live type/data schema first |
| Annotations | `GET/POST /canvases/<canvas-id>/comments`; inspect anchor/body and current permissions before writing |

Naplet layout updates normalize the supplied object: merge the current layout before sending a partial spatial change so view state survives. Re-read after every mutation. Stale CAS requires fresh state and an intent merge; a timeout requires read-back before any repeated create. Naplet POST is not documented as idempotent. Preserve partial successes rather than duplicating source records or views.

A native arrow is visual geometry. Inspect its layout-relative `start`, `end`, optional quadratic `curve`, styles and arrowheads with its world-space layout; it does not create a Tower task dependency. Unknown data fields survive edits. Use the current native-element schema, not Excalidraw JSON.

Comments have canvas-coordinate or naplet anchors. Native elements cannot be explicit comment subjects in the current contract. Explicit anchors/subjects take precedence over proximity. Read `can_delete`, `can_resolve`, `can_retarget` and `retarget_preserves_position` capability projections. Comment PATCH uses row-version CAS for resolving/reopening/retargeting. Deleting a confirmed root/reply set requires the unchanged `expected_reply_versions` plus root `expected_row_version`; concurrent replies require fresh review/confirmation. Source denial must not disclose a hidden subject's identity.

Linking a document, task list/tree, chat, HTML File or board adds a view of that record. Moving/resizing changes only that view. Removing it leaves its source record intact; do not delete the source unless separately requested. Display-title changes do not rename the source. A `canvas` source links another authorized canvas in the workspace; self-links are rejected, cycles allowed, and a link grants no access. Do not recursively expand cycles.

Read back both source and view. Completion evidence should identify the destination and readable source/canvas links, what changed and was preserved, exact/pinned/latest versions, and which checks were local, simulated or authenticated live. Report unavailable sources or incomplete pagination honestly.
