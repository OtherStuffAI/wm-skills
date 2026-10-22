---
name: ambulando-canvas
description: Read, build, and update Ambulando/Tower canvases with real tasks, documents, conversations, private HTML artefacts and Excalidraw boards. Use for explicit Ambulando canvas or naplet output and references; use artifacts for legacy Artifact WApp output.
---

# Ambulando Canvas

A canvas arranges references to real Tower records, plus native drawings and annotations. Read the authorized snapshot and the underlying records before interpreting or changing it. A task-shaped drawing never creates a task.

1. Discover the active Ambulando and Tower checkouts, deployment origins, workspace and broker signer using [connection and reading](references/reading.md). Read current repository instructions and relevant source docs; older checkouts can lack newer contracts.
2. Read layout, native elements, comments and ready naplets together. Resolve the requested source and exact referenced version before reading latest. Canvas access and source access are separate. Treat denied references neutrally.
3. Choose the actual output surface: tasks for tracked work; documents for durable prose; chat for conversation; private HTML Files for interactive visuals; Excalidraw Files for editable diagrams; native canvas elements for board annotations. Explicit Ambulando output uses Tower Files, without an external WApp dependency.
4. Select the destination explicitly. A workspace canvas can contain sources from multiple scopes and channels. Read the chosen scope's channels and verify membership before creating records. Do not inherit a destination from a nearby naplet or a message's From link.
5. For real task creation and parent/dependency persistence, follow [tasks](references/tasks.md). For HTML and board authoring, testing and version updates, follow [publishing](references/publishing.md). For canvas layout, linking and comments, follow [layout](references/layout.md).
6. Read back the source records and changed canvas snapshot. Report what was created or updated, destination, readable source/canvas links, version policy and verification limits. Verify task list visibility and relationships before claiming task completion. A skill install does not repair or verify a Task Tree UI bug.

Keep existing content and concurrent edits. On stale writes, read fresh state and reconcile intent; never replace a version token just to force an overwrite. Preserve partial successes after uncertain multi-step writes and report anything still unconfirmed.
