---
name: context-exploration
description: Explore Wingman scope component trees and selected authoritative references to locate work, or manage components and links through typed Context Tree tools.
---

# Context exploration

Use context trees to orient work without loading every document. Tower owns structure and permissions; referenced records own their content. Components have titles and parent pointers, with any number of roots. There is no required definition or vision document.

## Find the work

Resolve the authorized workspace and relevant scope using current dispatch context and scope listings. Pass workspace and scope explicitly to every context operation. If several scopes or roots could fit, inspect their titles and choose the relevant component; ask only when the choice would materially change the work.

Use `flightdeck_context_tree_list`, then `flightdeck_context_tree_path` to inspect ancestors, useful siblings and direct children. Lists recover every page; `limit` is page size, not a total cap. A missing ancestor, pagination error or access denial is not an empty tree: surface it and reload or resolve the missing authority before continuing.

List the selected component's direct references with `flightdeck_context_tree_references`. Read only the sources useful to the assignment with `flightdeck_context_tree_reference`; doc/file/task reads use their normal target ACLs. A structure link never grants target access. Treat unavailable targets neutrally without guessing their titles or contents. `doc` is the typed Tower target name; clients may call its viewer `document`.

Artifacts return a validated descriptor and the supported unversioned `/artifacts/<project>/<artifact>/` navigation URL. Follow-latest is live context: use the WApp's normal authenticated navigation, never bypass target ACLs or fetch a private cross-origin catalog. Capture the resolved numbered version in evidence when reproducibility matters. Keep deliberately versioned links pinned.

State the workspace/scope and component path being worked on, the selected sources and any availability gaps. Inspect additional relatives or references only as the task needs them.

## Manage structure within the request

Use create/update/link/unlink only when the user's request authorizes that edit. Visibility (`scope.read` or current scope-channel visibility) permits exploration; every edit requires existing `scope.manage`. An agent identity acquires no extra authority. References may address accessible records elsewhere in the same workspace; components can move only within their current scope.

Preserve the latest `expected_row_version` for update and unlink. On conflict, reread and reconcile intent instead of inventing a version or silently retrying. Unlink removes a link; source content remains.

Deletion needs actual user authorization to delete the named subtree. Scope management authority alone is not deletion intent. Obtain `flightdeck_context_tree_delete_preview`, present its component/descendant/reference counts and that linked content survives, then use that exact token with `confirmed: true` in `flightdeck_context_tree_confirmed_delete` after explicit confirmation. Never synthesize a token, auto-confirm a refreshed preview, or queue offline destructive work. A changed-preview conflict requires a fresh preview and renewed confirmation.

## CLI alternative

Run `bun clis/wingman.ts flightdeck context-tree help` from the active Autopilot checkout. For example:

```sh
bun clis/wingman.ts flightdeck context-tree list --workspace <workspace-id> --scope <scope-id> --json
bun clis/wingman.ts flightdeck context-tree path <component-id> --workspace <workspace-id> --scope <scope-id> --json
```

Use the current broker capability and exact URL/method/body NIP-98 transport. Missing registration, delegation or signing allowlist is a surfaced boundary, never a reason to find keys or use SQL. Source installation does not prove loaded tools or live human/agent convergence; record activation gaps separately.
