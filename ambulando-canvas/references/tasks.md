# Real tasks and Task Tree

## Select and verify destination

Read `GET /scopes`, then `GET /scopes/<scope-id>/channels`. Select the user's scope and channel, verifying that channel belongs to that scope in this workspace. Canvas location, chat origin and other naplets do not supply a default. The server derives a new task's scope from its channel; sending an arbitrary scope ID cannot override it.

Use `POST /channels/<channel-id>/tasks`, with current `task.create` permission. Example request body (replace placeholders; keep one stable request ID per intended creation):

```json
{
  "title": "Prepare release",
  "description": "Confirm release readiness and record evidence.",
  "client_request_id": "<unique-request-key>",
  "metadata": {
    "parent_task_id": "<parent-task-id>",
    "predecessor_task_ids": ["<predecessor-task-id>"]
  }
}
```

For a root, omit the parent or use null and use an empty predecessor array. Create parents/predecessors first, then use their returned IDs. Children store `metadata.parent_task_id`. Successors store the predecessor IDs in `metadata.predecessor_task_ids`; there is no separate successor array to invent. A next task in the same branch retains its predecessor's parent. Parallel successors each reference the same predecessor; multiple predecessors represent a join. State/assignment/dispatch are independent: do not add them merely because a graph is created.

The current create route writes task and relationship metadata atomically, under a workspace graph lock. It validates related task access, self-links, duplicate predecessors, parent cycles and dependency cycles. Related tasks can be in other authorized channels, but new records must still be created in the explicitly selected destination.

## Retry and concurrency

`client_request_id` is optional in the API, 1–240 characters when supplied; use it for uncertain retries. Identity is derived from workspace + actor + request key. Exact same channel and body retry returns the original task (`200`, `replayed: true`); first creation returns `201`. Reusing that key for a different destination/body gives `409 idempotency_conflict`. Preserve the exact request after an uncertain response, not just the title. Do not rotate the key to bypass a conflict or assume a timeout means no task exists. Without a key, creation has no such deduplication guarantee. Older deployed servers may not implement this contract: establish support before relying on retry safety.

Relationship edits use `PATCH /tasks/<task-id>` with the last read **`row_version`**, plus changed relationship metadata. This differs from canvas `expected_row_version`. Read and merge current metadata, preserve unrelated fields, and re-read after a stale `409`. Do not submit a new row version without reconciling competing graph changes. Report unresolved validation/authority failures rather than claiming the links were saved.

## Verify persistence and visibility

Before reporting success:

1. `GET /tasks/<task-id>` for every created/changed task. Check returned workspace, `scope_id`, `channel_id`, title, parent and predecessor IDs against the request.
2. `GET /tasks/<task-id>/relationships` for relevant parents/predecessors. It returns the source `task`, direct child/outgoing successor `tasks`, `has_more`, `next_cursor`, and `unavailable`. Follow all pages needed for the claim. Track visited IDs for graph walks, retain a frontier if bounded, and do not infer absence from an incomplete or unavailable projection.
3. `GET /channels/<channel-id>/tasks` and follow its returned paging to verify the same IDs appear in the ordinary channel task list. This establishes record/list visibility; a browser Tasks view claim requires a browser check too.
4. Add a view of those same records. A `task_tree` naplet uses `source: {type: "task_tree", id: "<channel-id>"}`. `layout.task_tree` holds `root_task_id`, `collapsed`, `upstream`, `instance_id`, and `viewport: {x, y, scale}`. Read current normalizer for allowed values; preserve existing view fields. A `task_list` uses the same channel source and ordinary list presentation.
5. Read the resulting snapshot and verify the source channel, root and layout. Report task/source links and saved relationship evidence separately from the visual view.

Changing a tree destination uses naplet PATCH `tree_channel_id` plus `expected_row_version`; Tower reauthorizes it and clears root/branch/viewport state. It does not move existing tasks. Removing or duplicating a view does not delete or duplicate tasks. Native cards/arrows and Excalidraw drawings are never substitutes for these real records.

If the deployed Task Tree cannot create or display them, keep the verified task IDs and report the UI/activation gap. Skill delivery alone does not establish that the observed Task Tree bug is fixed.
