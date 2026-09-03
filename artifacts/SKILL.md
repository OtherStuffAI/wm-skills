---
name: artifacts
description: Use when building, reading, reviewing, or sharing rendered HTML, visual proposals, interactive whiteboards, or element-level feedback through the Wingman Artifact WApp.
---

# Artifacts

Use the Artifact WApp when the user or a task needs a rendered proposal, interactive review surface, whiteboard, or visual artifact that should be shared and revisited.

## Recognize and read

Treat any Artifact WApp link, whiteboard reference, Excalidraw/tldraw link, or URL containing `/artifacts/<project>/<artifact>/<version>/` as a visual source surface. Read it before asking the user to restate what is shown.

For Excalidraw boards, inspect `excalidraw-scene.json` when available: extract text, shapes, arrows, positions, saved metadata, and embedded image payloads. Render or screenshot the board when visual layout or image content matters. For tldraw boards, inspect `.tldr`/`.tldraw` scene files or hosted HTML and use a visual render when needed.

If the user asks to build or update a whiteboard, use the Artifact WApp workflow and preserve earlier versions for comparison. Treat saved scenes as reviewable source material so later changes can be described as text, element, image, and layout diffs.

## Publish

Publish under:

```text
~/code/wingmanbefree/artifact-wapp/artifacts/<project>/<artifact>/<version>/
```

Put an `index.html` in the version directory where possible. Supporting CSS, JavaScript, images, and scene data may live beside it. The managed app serves:

```text
/artifacts/<project>/<artifact>/<version>/
```

Resolve the full hosted base URL from the Autopilot app registry; do not assume a fixed localhost port. After publishing files, trigger one explicit `/api/scan` on the already-running Artifact WApp. Do not start an ad hoc server or restart the registered Artifact WApp unless the user explicitly approves that restart in the current conversation.

Create a new version for feedback rounds unless the user explicitly asks to overwrite. Report the full hosted URL, project, artifact, version, and sharing mode; sharing is normally private.
