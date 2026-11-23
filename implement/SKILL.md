---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

<!-- wingman-matt-overlay:v1 -->
## Wingman routing takes precedence

When this work is in Wingman/NStack/Flight Deck/Ambulando context, read [wingman-matt-adapter](../wingman-matt-adapter/SKILL.md) before following any tracker, file-saving or output instructions below or in linked resources. Its routing explicitly supersedes conflicting upstream saving defaults inside Wingman. Outside Wingman, retain the standalone instructions below.

Inside Wingman: Fetch the canonical task/spec and fresh comments, retain source links, write validation on the task, and leave completion for the manager review contract; source code/Git follows repository instructions.

<!-- /wingman-matt-overlay:v1 -->

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Call the Skill tool with "tdd" where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, call the Skill tool with "code-review" to review the work.

Commit your work to the current branch.
