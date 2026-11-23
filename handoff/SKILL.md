---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

<!-- wingman-matt-overlay:v1 -->
## Wingman routing takes precedence

When this work is in Wingman/NStack/Flight Deck/Ambulando context, read [wingman-matt-adapter](../wingman-matt-adapter/SKILL.md) before following any tracker, file-saving or output instructions below or in linked resources. Its routing explicitly supersedes conflicting upstream saving defaults inside Wingman. Outside Wingman, retain the standalone instructions below.

Inside Wingman: Save operational handoffs only to verified ignored tmp/docs/handoffs or the authorized task/file surface, with durable record pointers and manager reporting context.

<!-- /wingman-matt-overlay:v1 -->

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
